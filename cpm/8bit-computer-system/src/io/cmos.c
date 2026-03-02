/*
 * CMOS/RTC Implementation
 * Battery-backed configuration storage and real-time clock
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "io.h"

uint8_t bcd_to_bin(uint8_t bcd) {
    return (bcd >> 4) * 10 + (bcd & 0x0F);
}

uint8_t bin_to_bcd(uint8_t bin) {
    return ((bin / 10) << 4) | (bin % 10);
}

void cmos_init(CMOS *cm) {
    memset(cm, 0, sizeof(CMOS));
    cm->address = 0;
    cm->last_update = time(NULL);
    
    /* Set default configuration values */
    cm->ram[CMOS_CONFIG] = 0x01;      /* Default config */
    cm->ram[CMOS_BOOTDEV] = 0x00;     /* Boot from drive A */
    cm->ram[CMOS_MEMSIZE] = 64;       /* 64KB RAM */
    
    cmos_update_rtc(cm);
}

void cmos_reset(CMOS *cm) {
    /* Preserve RTC and configuration, clear rest */
    uint8_t config = cm->ram[CMOS_CONFIG];
    uint8_t bootdev = cm->ram[CMOS_BOOTDEV];
    uint8_t memsize = cm->ram[CMOS_MEMSIZE];
    
    memset(cm->ram + 0x10, 0, CMOS_SIZE - 0x10);
    
    cm->ram[CMOS_CONFIG] = config;
    cm->ram[CMOS_BOOTDEV] = bootdev;
    cm->ram[CMOS_MEMSIZE] = memsize;
}

void cmos_update_rtc(CMOS *cm) {
    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    
    if (!tm_info) return;
    
    cm->ram[CMOS_RTC_SEC] = bin_to_bcd(tm_info->tm_sec);
    cm->ram[CMOS_RTC_MIN] = bin_to_bcd(tm_info->tm_min);
    cm->ram[CMOS_RTC_HOUR] = bin_to_bcd(tm_info->tm_hour);
    cm->ram[CMOS_RTC_DAY] = bin_to_bcd(tm_info->tm_mday);
    cm->ram[CMOS_RTC_MONTH] = bin_to_bcd(tm_info->tm_mon + 1);
    cm->ram[CMOS_RTC_YEAR] = bin_to_bcd(tm_info->tm_year % 100);
    
    cm->last_update = now;
}

uint8_t cmos_read(CMOS *cm, uint8_t addr) {
    if (addr >= CMOS_SIZE) return 0xFF;
    
    /* Update RTC before reading time values */
    if (addr <= CMOS_RTC_YEAR) {
        cmos_update_rtc(cm);
    }
    
    return cm->ram[addr];
}

void cmos_write(CMOS *cm, uint8_t addr, uint8_t value) {
    if (addr >= CMOS_SIZE) return;
    
    /* Protect RTC registers from direct writes */
    if (addr <= CMOS_RTC_YEAR) {
        return;
    }
    
    cm->ram[addr] = value;
}

void cmos_save(CMOS *cm, const char *filename) {
    FILE *f = fopen(filename, "wb");
    if (!f) {
        fprintf(stderr, "Error: Cannot save CMOS to %s\n", filename);
        return;
    }
    
    fwrite(cm->ram, 1, CMOS_SIZE, f);
    fclose(f);
}

void cmos_load(CMOS *cm, const char *filename) {
    FILE *f = fopen(filename, "rb");
    if (!f) {
        fprintf(stderr, "Warning: Cannot load CMOS from %s\n", filename);
        return;
    }
    
    fread(cm->ram, 1, CMOS_SIZE, f);
    fclose(f);
    
    cmos_update_rtc(cm);
}
