/*
 * CP/M Compatibility Layer Implementation
 * Provides CP/M 2.2 BDOS emulation for running CP/M programs
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "cpm.h"
#include "memory.h"
#include "io.h"

CPM_State cpm_state;

void cpm_init(CPM_State *cpm) {
    memset(cpm, 0, sizeof(CPM_State));
    cpm->enabled = true;
    cpm->current_drive = 0;
    cpm->dma_address = 0x0080;
    cpm->user_code = 0;
    
    for (int i = 0; i < 16; i++) {
        cpm->disk_files[i] = NULL;
    }
    
    printf("CP/M 2.2 compatibility layer initialized\n");
}

void cpm_reset(CPM_State *cpm) {
    /* Close all open files */
    for (int i = 0; i < 16; i++) {
        if (cpm->disk_files[i]) {
            fclose(cpm->disk_files[i]);
            cpm->disk_files[i] = NULL;
        }
    }
    
    cpm->current_drive = 0;
    cpm->dma_address = 0x0080;
    cpm->user_code = 0;
}

void cpm_boot(CPM_State *cpm) {
    /* Setup CP/M environment in memory */
    printf("Booting CP/M 2.2...\n");
    
    /* Set up BDOS jump at 0x0005 */
    mem_write(0x0005, 0xC3);  /* JP */
    mem_write(0x0006, 0x00);
    mem_write(0x0007, 0xDC);  /* BDOS address */
    
    /* Setup default FCB at 0x005C */
    for (int i = 0; i < 36; i++) {
        mem_write(0x005C + i, 0);
    }
    
    /* Setup default DMA buffer at 0x0080 */
    cpm->dma_address = 0x0080;
}

bool cpm_load_program(CPM_State *cpm __attribute__((unused)), const char *filename) {
    FILE *f = fopen(filename, "rb");
    if (!f) {
        fprintf(stderr, "Error: Cannot open CP/M program %s\n", filename);
        return false;
    }
    
    /* Load program at TPA (0x0100) */
    uint8_t buffer[CPM_TPA_SIZE];
    size_t size = fread(buffer, 1, CPM_TPA_SIZE, f);
    fclose(f);
    
    if (size == 0) {
        fprintf(stderr, "Error: Empty file %s\n", filename);
        return false;
    }
    
    /* Load into memory */
    for (size_t i = 0; i < size; i++) {
        mem_write(CPM_TPA_START + i, buffer[i]);
    }
    
    printf("Loaded CP/M program: %zu bytes\n", size);
    return true;
}

void cpm_mount_disk(CPM_State *cpm, uint8_t drive, const char *image_path) {
    if (drive >= 16) return;
    
    strncpy(cpm->disk_images[drive], image_path, 255);
    cpm->disk_images[drive][255] = '\0';
    
    printf("Mounted disk %c: -> %s\n", 'A' + drive, image_path);
}

uint8_t cpm_bdos_call(CPM_State *cpm, uint8_t function, uint16_t param) {
    switch (function) {
        case CPM_BOOT:
            cpm_boot(cpm);
            return 0;
            
        case CPM_CONIN:
            return cpm_conin();
            
        case CPM_CONOUT:
            cpm_conout(param & 0xFF);
            return 0;
            
        case CPM_PRTSTR:
            cpm_prtstr(param);
            return 0;
            
        case CPM_CONST:
            return cpm_const();
            
        case CPM_VERSION:
            return 0x22;  /* CP/M 2.2 */
            
        case CPM_SELDSK:
            cpm_select_disk(param & 0xFF);
            return 0;
            
        case CPM_SETDMA:
            cpm_set_dma(param);
            return 0;
            
        case CPM_CURRDISK:
            return cpm->current_drive;
            
        case CPM_USERCODE:
            if (param == 0xFF) {
                return cpm->user_code;
            } else {
                cpm->user_code = param & 0x0F;
                return 0;
            }
            
        default:
            printf("CP/M BDOS function %d not implemented\n", function);
            return 0;
    }
}

uint8_t cpm_conin(void) {
    /* Read from keyboard */
    return kbd_get_key(&keyboard);
}

void cpm_conout(uint8_t c) {
    /* Output to console */
    serial_write_char(c);
    /* GPU output would go here if needed */
}

uint8_t cpm_const(void) {
    /* Check console status */
    return kbd_key_available(&keyboard) ? 0xFF : 0x00;
}

void cpm_prtstr(uint16_t addr) {
    /* Print string terminated by '$' */
    while (1) {
        uint8_t c = mem_read(addr++);
        if (c == '$') break;
        cpm_conout(c);
    }
}

void cpm_select_disk(uint8_t drive) {
    if (drive < 16) {
        cpm_state.current_drive = drive;
    }
}

void cpm_set_dma(uint16_t address) {
    cpm_state.dma_address = address;
}

uint8_t cpm_open_file(CPM_FCB *fcb __attribute__((unused))) {
    /* Simplified file open */
    return 0;  /* Success */
}

uint8_t cpm_close_file(CPM_FCB *fcb __attribute__((unused))) {
    return 0;  /* Success */
}

uint8_t cpm_read_seq(CPM_FCB *fcb __attribute__((unused))) {
    return 0;  /* Success */
}

uint8_t cpm_write_seq(CPM_FCB *fcb __attribute__((unused))) {
    return 0;  /* Success */
}

uint8_t cpm_make_file(CPM_FCB *fcb __attribute__((unused))) {
    return 0;  /* Success */
}

uint8_t cpm_delete_file(CPM_FCB *fcb __attribute__((unused))) {
    return 0;  /* Success */
}

void cpm_read_sector(uint8_t drive __attribute__((unused)), uint16_t track __attribute__((unused)), uint16_t sector __attribute__((unused))) {
    /* Read sector to DMA buffer */
}

void cpm_write_sector(uint8_t drive __attribute__((unused)), uint16_t track __attribute__((unused)), uint16_t sector __attribute__((unused))) {
    /* Write sector from DMA buffer */
}
