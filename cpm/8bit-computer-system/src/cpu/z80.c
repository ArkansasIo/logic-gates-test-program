/*
 * Z80 CPU Emulator Implementation
 * Core CPU functions and register management
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "z80.h"
#include "memory.h"

void z80_init(Z80_CPU *cpu) {
    memset(cpu, 0, sizeof(Z80_CPU));
    cpu->SP = 0xFFFF;
    cpu->PC = 0x0000;
    cpu->IM = 0;
    printf("Z80 CPU initialized\n");
}

void z80_reset(Z80_CPU *cpu) {
    cpu->PC = 0x0000;
    cpu->SP = 0xFFFF;
    cpu->AF = 0xFFFF;
    cpu->BC = 0xFFFF;
    cpu->DE = 0xFFFF;
    cpu->HL = 0xFFFF;
    cpu->IX = 0xFFFF;
    cpu->IY = 0xFFFF;
    cpu->I = 0;
    cpu->R = 0;
    cpu->IFF1 = false;
    cpu->IFF2 = false;
    cpu->IM = 0;
    cpu->halted = false;
}

void z80_set_flag(Z80_CPU *cpu, uint8_t flag) {
    cpu->F |= flag;
}

void z80_clear_flag(Z80_CPU *cpu, uint8_t flag) {
    cpu->F &= ~flag;
}

bool z80_get_flag(Z80_CPU *cpu, uint8_t flag) {
    return (cpu->F & flag) != 0;
}

void z80_update_flags_zsp(Z80_CPU *cpu, uint8_t result) {
    /* Zero flag */
    if (result == 0) {
        z80_set_flag(cpu, FLAG_Z);
    } else {
        z80_clear_flag(cpu, FLAG_Z);
    }
    
    /* Sign flag */
    if (result & 0x80) {
        z80_set_flag(cpu, FLAG_S);
    } else {
        z80_clear_flag(cpu, FLAG_S);
    }
    
    /* Parity flag */
    int parity = 0;
    for (int i = 0; i < 8; i++) {
        if (result & (1 << i)) parity++;
    }
    if (parity % 2 == 0) {
        z80_set_flag(cpu, FLAG_PV);
    } else {
        z80_clear_flag(cpu, FLAG_PV);
    }
}

int z80_execute(Z80_CPU *cpu) {
    if (cpu->halted) {
        return 4;  /* HALT state takes 4 cycles */
    }
    
    return z80_execute_instruction(cpu);
}

void z80_interrupt(Z80_CPU *cpu, bool maskable) {
    if (maskable && !cpu->IFF1) {
        return;  /* Maskable interrupts disabled */
    }
    
    cpu->halted = false;
    cpu->IFF1 = false;
    cpu->IFF2 = false;
    
    if (cpu->IM == 0) {
        /* Mode 0: Execute instruction on data bus (not implemented) */
        cpu->PC = 0x0038;
    } else if (cpu->IM == 1) {
        /* Mode 1: RST 38h */
        cpu->SP -= 2;
        mem_write(cpu->SP, cpu->PC & 0xFF);
        mem_write(cpu->SP + 1, cpu->PC >> 8);
        cpu->PC = 0x0038;
    } else {
        /* Mode 2: Vectored interrupt */
        uint16_t vector = (cpu->I << 8) | 0xFF;
        uint16_t addr = mem_read(vector) | (mem_read(vector + 1) << 8);
        cpu->SP -= 2;
        mem_write(cpu->SP, cpu->PC & 0xFF);
        mem_write(cpu->SP + 1, cpu->PC >> 8);
        cpu->PC = addr;
    }
}

void z80_dump_registers(Z80_CPU *cpu) {
    printf("PC=%04X SP=%04X AF=%04X BC=%04X DE=%04X HL=%04X\n",
           cpu->PC, cpu->SP, cpu->AF, cpu->BC, cpu->DE, cpu->HL);
    printf("IX=%04X IY=%04X I=%02X R=%02X\n",
           cpu->IX, cpu->IY, cpu->I, cpu->R);
    printf("Flags: S=%d Z=%d H=%d P=%d N=%d C=%d\n",
           z80_get_flag(cpu, FLAG_S) ? 1 : 0,
           z80_get_flag(cpu, FLAG_Z) ? 1 : 0,
           z80_get_flag(cpu, FLAG_H) ? 1 : 0,
           z80_get_flag(cpu, FLAG_PV) ? 1 : 0,
           z80_get_flag(cpu, FLAG_N) ? 1 : 0,
           z80_get_flag(cpu, FLAG_C) ? 1 : 0);
    printf("Cycles: %llu  Halted: %s\n", cpu->cycles, cpu->halted ? "Yes" : "No");
}

/* Helper macros for instruction implementation */
#define FETCH_BYTE() mem_read(cpu->PC++)
#define FETCH_WORD() (FETCH_BYTE() | (FETCH_BYTE() << 8))
#define PUSH_WORD(val) do { \
    cpu->SP -= 2; \
    mem_write(cpu->SP, (val) & 0xFF); \
    mem_write(cpu->SP + 1, (val) >> 8); \
} while(0)
#define POP_WORD() (mem_read(cpu->SP) | (mem_read(cpu->SP + 1) << 8)); cpu->SP += 2

int z80_execute_instruction(Z80_CPU *cpu) {
    uint8_t opcode = FETCH_BYTE();
    int cycles = 4;
    
    switch (opcode) {
        /* NOP */
        case 0x00:
            break;
            
        /* LD BC, nn */
        case 0x01:
            cpu->BC = FETCH_WORD();
            cycles = 10;
            break;
            
        /* LD (BC), A */
        case 0x02:
            mem_write(cpu->BC, cpu->A);
            cycles = 7;
            break;
            
        /* INC BC */
        case 0x03:
            cpu->BC++;
            cycles = 6;
            break;
            
        /* INC B */
        case 0x04:
            cpu->B++;
            z80_update_flags_zsp(cpu, cpu->B);
            z80_clear_flag(cpu, FLAG_N);
            break;
            
        /* DEC B */
        case 0x05:
            cpu->B--;
            z80_update_flags_zsp(cpu, cpu->B);
            z80_set_flag(cpu, FLAG_N);
            break;
            
        /* LD B, n */
        case 0x06:
            cpu->B = FETCH_BYTE();
            cycles = 7;
            break;
        
        /* LD C, n */
        case 0x0E:
            cpu->C = FETCH_BYTE();
            cycles = 7;
            break;
            
        /* LD DE, nn */
        case 0x11:
            cpu->DE = FETCH_WORD();
            cycles = 10;
            break;
            
        /* JR e - Relative jump */
        case 0x18: {
            int8_t offset = (int8_t)FETCH_BYTE();
            cpu->PC += offset;
            cycles = 12;
            break;
        }
        
        /* JR Z,e - Jump relative if zero */
        case 0x28: {
            int8_t offset = (int8_t)FETCH_BYTE();
            if (cpu->F & FLAG_Z) {
                cpu->PC += offset;
                cycles = 12;
            } else {
                cycles = 7;
            }
            break;
        }
        
        /* JR NZ,e - Jump relative if not zero */
        case 0x20: {
            int8_t offset = (int8_t)FETCH_BYTE();
            if (!(cpu->F & FLAG_Z)) {
                cpu->PC += offset;
                cycles = 12;
            } else {
                cycles = 7;
            }
            break;
        }
        
        /* LD HL, nn */
        case 0x21:
            cpu->HL = FETCH_WORD();
            cycles = 10;
            break;
            
        /* LD (nn), HL */
        case 0x22: {
            uint16_t addr = FETCH_WORD();
            mem_write(addr, cpu->L);
            mem_write(addr + 1, cpu->H);
            cycles = 16;
            break;
        }
        
        /* INC HL */
        case 0x23:
            cpu->HL++;
            cycles = 6;
            break;
            
        /* LD SP, nn */
        case 0x31:
            cpu->SP = FETCH_WORD();
            cycles = 10;
            break;
            
        /* LD (nn), A */
        case 0x32: {
            uint16_t addr = FETCH_WORD();
            mem_write(addr, cpu->A);
            cycles = 13;
            break;
        }
        
        /* LD A, (nn) */
        case 0x3A: {
            uint16_t addr = FETCH_WORD();
            cpu->A = mem_read(addr);
            cycles = 13;
            break;
        }
        
        /* LD A, n */
        case 0x3E:
            cpu->A = FETCH_BYTE();
            cycles = 7;
            break;
        
        /* LD B, B through LD A, A (0x40-0x7F) */
        case 0x40: case 0x41: case 0x42: case 0x43: case 0x44: case 0x45: case 0x47:
        case 0x48: case 0x49: case 0x4A: case 0x4B: case 0x4C: case 0x4D: case 0x4F:
        case 0x50: case 0x51: case 0x52: case 0x53: case 0x54: case 0x55: case 0x57:
        case 0x58: case 0x59: case 0x5A: case 0x5B: case 0x5C: case 0x5D: case 0x5F:
        case 0x60: case 0x61: case 0x62: case 0x63: case 0x64: case 0x65: case 0x67:
        case 0x68: case 0x69: case 0x6A: case 0x6B: case 0x6C: case 0x6D: case 0x6F:
        case 0x78: case 0x79: case 0x7A: case 0x7B: case 0x7C: case 0x7D: case 0x7F: {
            uint8_t val;
            
            /* Decode source register */
            switch (opcode & 0x07) {
                case 0: val = cpu->B; break;
                case 1: val = cpu->C; break;
                case 2: val = cpu->D; break;
                case 3: val = cpu->E; break;
                case 4: val = cpu->H; break;
                case 5: val = cpu->L; break;
                case 7: val = cpu->A; break;
            }
            
            /* Decode destination and store */
            switch ((opcode >> 3) & 0x07) {
                case 0: cpu->B = val; break;
                case 1: cpu->C = val; break;
                case 2: cpu->D = val; break;
                case 3: cpu->E = val; break;
                case 4: cpu->H = val; break;
                case 5: cpu->L = val; break;
                case 7: cpu->A = val; break;
            }
            break;
        }
        
        /* LD A,(HL) */
        case 0x7E:
            cpu->A = mem_read(cpu->HL);
            cycles = 7;
            break;
        
        /* LD (HL),A */
        case 0x77:
            mem_write(cpu->HL, cpu->A);
            cycles = 7;
            break;
        
        /* ADD A, r (0x80-0x87) */
        case 0x80: case 0x81: case 0x82: case 0x83:
        case 0x84: case 0x85: case 0x87: {
            uint8_t val;
            switch (opcode & 0x07) {
                case 0: val = cpu->B; break;
                case 1: val = cpu->C; break;
                case 2: val = cpu->D; break;
                case 3: val = cpu->E; break;
                case 4: val = cpu->H; break;
                case 5: val = cpu->L; break;
                case 7: val = cpu->A; break;
            }
            uint16_t result = cpu->A + val;
            if (result > 0xFF) z80_set_flag(cpu, FLAG_C);
            else z80_clear_flag(cpu, FLAG_C);
            cpu->A = result & 0xFF;
            z80_update_flags_zsp(cpu, cpu->A);
            z80_clear_flag(cpu, FLAG_N);
            break;
        }
        
        /* SUB A, r (0x90-0x97) */
        case 0x90: case 0x91: case 0x92: case 0x93:
        case 0x94: case 0x95: case 0x97: {
            uint8_t val;
            switch (opcode & 0x07) {
                case 0: val = cpu->B; break;
                case 1: val = cpu->C; break;
                case 2: val = cpu->D; break;
                case 3: val = cpu->E; break;
                case 4: val = cpu->H; break;
                case 5: val = cpu->L; break;
                case 7: val = cpu->A; break;
            }
            int result = cpu->A - val;
            if (result < 0) z80_set_flag(cpu, FLAG_C);
            else z80_clear_flag(cpu, FLAG_C);
            cpu->A = result & 0xFF;
            z80_update_flags_zsp(cpu, cpu->A);
            z80_set_flag(cpu, FLAG_N);
            break;
        }
        
        /* AND A, r (0xA0-0xA7) */
        case 0xA0: case 0xA1: case 0xA2: case 0xA3:
        case 0xA4: case 0xA5: case 0xA7: {
            uint8_t val;
            switch (opcode & 0x07) {
                case 0: val = cpu->B; break;
                case 1: val = cpu->C; break;
                case 2: val = cpu->D; break;
                case 3: val = cpu->E; break;
                case 4: val = cpu->H; break;
                case 5: val = cpu->L; break;
                case 7: val = cpu->A; break;
            }
            cpu->A &= val;
            z80_update_flags_zsp(cpu, cpu->A);
            z80_set_flag(cpu, FLAG_H);
            z80_clear_flag(cpu, FLAG_N);
            z80_clear_flag(cpu, FLAG_C);
            break;
        }
        
        /* XOR A, r (0xA8-0xAF) */
        case 0xA8: case 0xA9: case 0xAA: case 0xAB:
        case 0xAC: case 0xAD: case 0xAF: {
            uint8_t val;
            switch (opcode & 0x07) {
                case 0: val = cpu->B; break;
                case 1: val = cpu->C; break;
                case 2: val = cpu->D; break;
                case 3: val = cpu->E; break;
                case 4: val = cpu->H; break;
                case 5: val = cpu->L; break;
                case 7: val = cpu->A; break;
            }
            cpu->A ^= val;
            z80_update_flags_zsp(cpu, cpu->A);
            z80_clear_flag(cpu, FLAG_H);
            z80_clear_flag(cpu, FLAG_N);
            z80_clear_flag(cpu, FLAG_C);
            break;
        }
        
        /* OR A, r (0xB0-0xB7) */
        case 0xB0: case 0xB1: case 0xB2: case 0xB3:
        case 0xB4: case 0xB5: case 0xB7: {
            uint8_t val;
            switch (opcode & 0x07) {
                case 0: val = cpu->B; break;
                case 1: val = cpu->C; break;
                case 2: val = cpu->D; break;
                case 3: val = cpu->E; break;
                case 4: val = cpu->H; break;
                case 5: val = cpu->L; break;
                case 7: val = cpu->A; break;
            }
            cpu->A |= val;
            z80_update_flags_zsp(cpu, cpu->A);
            z80_clear_flag(cpu, FLAG_H);
            z80_clear_flag(cpu, FLAG_N);
            z80_clear_flag(cpu, FLAG_C);
            break;
        }
        
        /* CP A, r (0xB8-0xBF) - Compare */
        case 0xB8: case 0xB9: case 0xBA: case 0xBB:
        case 0xBC: case 0xBD: case 0xBF: {
            uint8_t val;
            switch (opcode & 0x07) {
                case 0: val = cpu->B; break;
                case 1: val = cpu->C; break;
                case 2: val = cpu->D; break;
                case 3: val = cpu->E; break;
                case 4: val = cpu->H; break;
                case 5: val = cpu->L; break;
                case 7: val = cpu->A; break;
            }
            int result = cpu->A - val;
            if (result < 0) z80_set_flag(cpu, FLAG_C);
            else z80_clear_flag(cpu, FLAG_C);
            z80_update_flags_zsp(cpu, result & 0xFF);
            z80_set_flag(cpu, FLAG_N);
            break;
        }
        
        /* PUSH BC */
        case 0xC5:
            PUSH_WORD(cpu->BC);
            cycles = 11;
            break;
            
        /* PUSH DE */
        case 0xD5:
            PUSH_WORD(cpu->DE);
            cycles = 11;
            break;
            
        /* PUSH HL */
        case 0xE5:
            PUSH_WORD(cpu->HL);
            cycles = 11;
            break;
            
        /* PUSH AF */
        case 0xF5:
            PUSH_WORD(cpu->AF);
            cycles = 11;
            break;
            
        /* POP BC */
        case 0xC1:
            cpu->BC = POP_WORD();
            cycles = 10;
            break;
            
        /* POP DE */
        case 0xD1:
            cpu->DE = POP_WORD();
            cycles = 10;
            break;
            
        /* POP HL */
        case 0xE1:
            cpu->HL = POP_WORD();
            cycles = 10;
            break;
            
        /* POP AF */
        case 0xF1:
            cpu->AF = POP_WORD();
            cycles = 10;
            break;
        
        /* RET NZ */
        case 0xC0:
            if (!(cpu->F & FLAG_Z)) {
                cpu->PC = POP_WORD();
                cycles = 11;
            } else {
                cycles = 5;
            }
            break;
        
        /* RET Z */
        case 0xC8:
            if (cpu->F & FLAG_Z) {
                cpu->PC = POP_WORD();
                cycles = 11;
            } else {
                cycles = 5;
            }
            break;
        
        /* RET */
        case 0xC9:
            cpu->PC = POP_WORD();
            cycles = 10;
            break;
        
        /* JP NZ,nn */
        case 0xC2: {
            uint16_t addr = FETCH_WORD();
            if (!(cpu->F & FLAG_Z)) {
                cpu->PC = addr;
            }
            cycles = 10;
            break;
        }
        
        /* JP nn */
        case 0xC3: {
            uint16_t addr = FETCH_WORD();
            cpu->PC = addr;
            cycles = 10;
            break;
        }
        
        /* CALL nn */
        case 0xCD: {
            uint16_t addr = FETCH_WORD();
            PUSH_WORD(cpu->PC);
            cpu->PC = addr;
            cycles = 17;
            break;
        }
        
        /* SUB n */
        case 0xD6: {
            uint8_t val = FETCH_BYTE();
            int result = cpu->A - val;
            if (result < 0) z80_set_flag(cpu, FLAG_C);
            else z80_clear_flag(cpu, FLAG_C);
            cpu->A = result & 0xFF;
            z80_update_flags_zsp(cpu, cpu->A);
            z80_set_flag(cpu, FLAG_N);
            cycles = 7;
            break;
        }
        
        /* OUT (n), A */
        case 0xD3: {
            uint8_t port = FETCH_BYTE();
            io_write(port, cpu->A);
            cycles = 11;
            break;
        }
        
        /* IN A, (n) */
        case 0xDB: {
            uint8_t port = FETCH_BYTE();
            cpu->A = io_read(port);
            cycles = 11;
            break;
        }
        
        /* AND n */
        case 0xE6: {
            uint8_t val = FETCH_BYTE();
            cpu->A &= val;
            z80_update_flags_zsp(cpu, cpu->A);
            z80_set_flag(cpu, FLAG_H);
            z80_clear_flag(cpu, FLAG_N);
            z80_clear_flag(cpu, FLAG_C);
            cycles = 7;
            break;
        }
        
        /* JP (HL) */
        case 0xE9:
            cpu->PC = cpu->HL;
            cycles = 4;
            break;
        
        /* XOR n */
        case 0xEE: {
            uint8_t val = FETCH_BYTE();
            cpu->A ^= val;
            z80_update_flags_zsp(cpu, cpu->A);
            z80_clear_flag(cpu, FLAG_H);
            z80_clear_flag(cpu, FLAG_N);
            z80_clear_flag(cpu, FLAG_C);
            cycles = 7;
            break;
        }
        
        /* DI - Disable Interrupts */
        case 0xF3:
            cpu->IFF1 = false;
            cpu->IFF2 = false;
            break;
        
        /* OR n */
        case 0xF6: {
            uint8_t val = FETCH_BYTE();
            cpu->A |= val;
            z80_update_flags_zsp(cpu, cpu->A);
            z80_clear_flag(cpu, FLAG_H);
            z80_clear_flag(cpu, FLAG_N);
            z80_clear_flag(cpu, FLAG_C);
            cycles = 7;
            break;
        }
            
        /* EI - Enable Interrupts */
        case 0xFB:
            cpu->IFF1 = true;
            cpu->IFF2 = true;
            break;
        
        /* CP n */
        case 0xFE: {
            uint8_t val = FETCH_BYTE();
            int result = cpu->A - val;
            if (result < 0) z80_set_flag(cpu, FLAG_C);
            else z80_clear_flag(cpu, FLAG_C);
            z80_update_flags_zsp(cpu, result & 0xFF);
            z80_set_flag(cpu, FLAG_N);
            cycles = 7;
            break;
        }
            
        /* HALT */
        case 0x76:
            cpu->halted = true;
            break;
            
        default:
            printf("Unimplemented opcode: 0x%02X at PC=0x%04X\n", opcode, cpu->PC - 1);
            cpu->halted = true;
            break;
    }
    
    cpu->cycles += cycles;
    cpu->R = (cpu->R & 0x80) | ((cpu->R + 1) & 0x7F);
    
    return cycles;
}
