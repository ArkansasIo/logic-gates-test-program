/*
 * Z80 CPU Emulator Header
 * 8-bit Z80 processor with full instruction set
 */

#ifndef Z80_H
#define Z80_H

#include <stdint.h>
#include <stdbool.h>

/* Z80 Registers */
typedef struct {
    /* Main register set */
    union {
        struct { uint8_t F, A; };  /* Accumulator and Flags */
        uint16_t AF;
    };
    union {
        struct { uint8_t C, B; };
        uint16_t BC;
    };
    union {
        struct { uint8_t E, D; };
        uint16_t DE;
    };
    union {
        struct { uint8_t L, H; };
        uint16_t HL;
    };
    
    /* Alternate register set */
    uint16_t AF_alt;
    uint16_t BC_alt;
    uint16_t DE_alt;
    uint16_t HL_alt;
    
    /* Index registers */
    uint16_t IX;
    uint16_t IY;
    
    /* Special registers */
    uint16_t SP;  /* Stack Pointer */
    uint16_t PC;  /* Program Counter */
    uint8_t I;    /* Interrupt Vector */
    uint8_t R;    /* Memory Refresh */
    
    /* Flags */
    bool IFF1;    /* Interrupt Enable Flag 1 */
    bool IFF2;    /* Interrupt Enable Flag 2 */
    uint8_t IM;   /* Interrupt Mode (0, 1, 2) */
    
    /* State */
    bool halted;
    uint64_t cycles;  /* Total CPU cycles executed */
} Z80_CPU;

/* Flag bits in F register */
#define FLAG_C  0x01  /* Carry */
#define FLAG_N  0x02  /* Add/Subtract */
#define FLAG_PV 0x04  /* Parity/Overflow */
#define FLAG_3  0x08  /* Undocumented */
#define FLAG_H  0x10  /* Half Carry */
#define FLAG_5  0x20  /* Undocumented */
#define FLAG_Z  0x40  /* Zero */
#define FLAG_S  0x80  /* Sign */

/* CPU Functions */
void z80_init(Z80_CPU *cpu);
void z80_reset(Z80_CPU *cpu);
int z80_execute(Z80_CPU *cpu);
void z80_interrupt(Z80_CPU *cpu, bool maskable);
void z80_dump_registers(Z80_CPU *cpu);

/* Instruction execution */
int z80_execute_instruction(Z80_CPU *cpu);

/* Flag manipulation */
void z80_set_flag(Z80_CPU *cpu, uint8_t flag);
void z80_clear_flag(Z80_CPU *cpu, uint8_t flag);
bool z80_get_flag(Z80_CPU *cpu, uint8_t flag);
void z80_update_flags_zsp(Z80_CPU *cpu, uint8_t result);

/* Memory access (implemented in memory.c) */
extern uint8_t mem_read(uint16_t address);
extern void mem_write(uint16_t address, uint8_t value);
extern uint8_t io_read(uint8_t port);
extern void io_write(uint8_t port, uint8_t value);

#endif /* Z80_H */
