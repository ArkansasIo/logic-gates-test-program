/*
 * Memory System Header
 * RAM, ROM, and Video Memory management
 */

#ifndef MEMORY_H
#define MEMORY_H

#include <stdint.h>
#include <stdbool.h>

/* Memory configuration */
#define RAM_SIZE    0x10000   /* 64KB total address space */
#define ROM_SIZE    0x2000    /* 8KB ROM (BIOS) */
#define VRAM_SIZE   0x2000    /* 8KB Video RAM */
#define MAIN_RAM    0xC000    /* 48KB main RAM */

/* Memory map */
#define ROM_START   0x0000
#define ROM_END     0x1FFF
#define RAM_START   0x2000
#define RAM_END     0xDFFF
#define VRAM_START  0xE000
#define VRAM_END    0xFFFF

/* Memory structure */
typedef struct {
    uint8_t rom[ROM_SIZE];      /* BIOS ROM */
    uint8_t ram[MAIN_RAM];      /* Main RAM */
    uint8_t vram[VRAM_SIZE];    /* Video RAM */
    bool rom_enabled;           /* ROM is mapped at 0x0000 */
    bool write_protect;         /* Write protection flag */
} Memory;

/* Global memory instance */
extern Memory memory;

/* Memory functions */
void memory_init(Memory *mem);
void memory_reset(Memory *mem);
void memory_load_rom(Memory *mem, const char *filename);
void memory_load_program(Memory *mem, uint16_t address, const uint8_t *data, size_t size);

/* Memory access */
uint8_t mem_read(uint16_t address);
void mem_write(uint16_t address, uint8_t value);

/* ROM control */
void memory_enable_rom(bool enable);
void memory_write_protect(bool enable);

/* Dump functions for debugging */
void memory_dump(uint16_t start, uint16_t end);
void memory_dump_page(uint16_t page);

#endif /* MEMORY_H */
