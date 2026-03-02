/*
 * Memory System Implementation
 * RAM, ROM, and Video Memory management
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include "memory.h"

Memory memory;

void memory_init(Memory *mem) {
    memset(mem, 0, sizeof(Memory));
    mem->rom_enabled = true;
    mem->write_protect = false;
    printf("Memory initialized: ROM=%dKB, RAM=%dKB, VRAM=%dKB\n",
           ROM_SIZE / 1024, MAIN_RAM / 1024, VRAM_SIZE / 1024);
}

void memory_reset(Memory *mem) {
    memset(mem->ram, 0, MAIN_RAM);
    memset(mem->vram, 0, VRAM_SIZE);
    mem->rom_enabled = true;
    mem->write_protect = false;
}

void memory_load_rom(Memory *mem, const char *filename) {
    FILE *f = fopen(filename, "rb");
    if (!f) {
        fprintf(stderr, "Warning: Cannot open ROM file %s, using empty ROM\n", filename);
        memset(mem->rom, 0, ROM_SIZE);
        
        /* Create a simple boot ROM that jumps to 0x8000 */
        mem->rom[0] = 0xC3;  /* JP */
        mem->rom[1] = 0x00;
        mem->rom[2] = 0x80;  /* 0x8000 */
        return;
    }
    
    size_t read = fread(mem->rom, 1, ROM_SIZE, f);
    fclose(f);
    
    printf("Loaded %zu bytes into ROM\n", read);
    
    if (read < ROM_SIZE) {
        memset(mem->rom + read, 0, ROM_SIZE - read);
    }
}

void memory_load_program(Memory *mem __attribute__((unused)), uint16_t address, const uint8_t *data, size_t size) {
    for (size_t i = 0; i < size; i++) {
        mem_write(address + i, data[i]);
    }
}

uint8_t mem_read(uint16_t address) {
    /* ROM area (0x0000 - 0x1FFF) */
    if (address <= ROM_END && memory.rom_enabled) {
        return memory.rom[address];
    }
    /* Main RAM (0x2000 - 0xDFFF) */
    else if (address >= RAM_START && address <= RAM_END) {
        return memory.ram[address - RAM_START];
    }
    /* Video RAM (0xE000 - 0xFFFF) */
    else if (address >= VRAM_START) {
        return memory.vram[address - VRAM_START];
    }
    /* ROM disabled, map RAM to low memory */
    else {
        if (address < RAM_START) {
            /* When ROM is disabled, low memory is RAM */
            return memory.ram[address];
        }
        return memory.ram[address - RAM_START];
    }
}

void mem_write(uint16_t address, uint8_t value) {
    /* ROM area - ignore writes if ROM is enabled */
    if (address <= ROM_END) {
        if (memory.rom_enabled || memory.write_protect) {
            /* Silently ignore writes to ROM */
            return;
        }
        /* ROM disabled, write to RAM */
        memory.ram[address] = value;
        return;
    }
    /* Main RAM (0x2000 - 0xDFFF) */
    else if (address >= RAM_START && address <= RAM_END) {
        memory.ram[address - RAM_START] = value;
    }
    /* Video RAM (0xE000 - 0xFFFF) */
    else if (address >= VRAM_START) {
        memory.vram[address - VRAM_START] = value;
    }
}

void memory_enable_rom(bool enable) {
    memory.rom_enabled = enable;
}

void memory_write_protect(bool enable) {
    memory.write_protect = enable;
}

void memory_dump(uint16_t start, uint16_t end) {
    printf("Memory dump from 0x%04X to 0x%04X:\n", start, end);
    
    for (uint16_t addr = start; addr <= end; addr += 16) {
        printf("%04X: ", addr);
        
        /* Hex dump */
        for (int i = 0; i < 16 && (addr + i) <= end; i++) {
            printf("%02X ", mem_read(addr + i));
        }
        
        /* ASCII dump */
        printf(" | ");
        for (int i = 0; i < 16 && (addr + i) <= end; i++) {
            uint8_t byte = mem_read(addr + i);
            printf("%c", (byte >= 32 && byte < 127) ? byte : '.');
        }
        printf("\n");
    }
}

void memory_dump_page(uint16_t page) {
    uint16_t start = page * 256;
    uint16_t end = start + 255;
    memory_dump(start, end);
}
