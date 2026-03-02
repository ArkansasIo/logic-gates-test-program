/*
 * Main Emulator Entry Point
 * 8-Bit Computer System Emulator
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "z80.h"
#include "memory.h"
#include "gpu.h"
#include "io.h"
#include "cpm.h"

/* Emulator state */
typedef struct {
    Z80_CPU cpu;
    bool running;
    bool debug_mode;
    bool cpm_mode;
    uint64_t total_cycles;
    double clock_speed;  /* MHz */
} Emulator;

Emulator emulator;

/* Function prototypes */
void emulator_init(void);
void emulator_reset(void);
void emulator_run(void);
void emulator_step(void);
void emulator_load_rom(const char *filename);
void emulator_load_program(const char *filename, uint16_t address);
void print_usage(const char *progname);
void debug_prompt(void);

int main(int argc, char *argv[]) {
    printf("8-Bit Computer System Emulator v1.0\n");
    printf("Z80 CPU with GPU, BIOS, and CP/M support\n");
    printf("========================================\n\n");
    
    /* Initialize emulator */
    emulator_init();
    
    /* Parse command line arguments */
    bool load_bios = true;
    char *program_file = NULL;
    char *disk_image = NULL;
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            print_usage(argv[0]);
            return 0;
        } else if (strcmp(argv[i], "--debug") == 0 || strcmp(argv[i], "-d") == 0) {
            emulator.debug_mode = true;
        } else if (strcmp(argv[i], "--cpm") == 0) {
            emulator.cpm_mode = true;
            if (i + 1 < argc) {
                disk_image = argv[++i];
            }
        } else if (strcmp(argv[i], "--nobios") == 0) {
            load_bios = false;
        } else if (strcmp(argv[i], "--rom") == 0) {
            if (i + 1 < argc) {
                emulator_load_rom(argv[++i]);
                load_bios = false;
            }
        } else {
            program_file = argv[i];
        }
    }
    
    /* Load BIOS */
    if (load_bios) {
        printf("Loading BIOS from bios/bios.bin...\n");
        emulator_load_rom("bios/bios.bin");
    }
    
    /* Setup CP/M if requested */
    if (emulator.cpm_mode) {
        printf("Initializing CP/M mode...\n");
        cpm_init(&cpm_state);
        if (disk_image) {
            printf("Mounting disk image: %s\n", disk_image);
            cpm_mount_disk(&cpm_state, 0, disk_image);
        }
        cpm_boot(&cpm_state);
    }
    
    /* Load program if specified */
    if (program_file) {
        printf("Loading program: %s\n", program_file);
        if (emulator.cpm_mode) {
            cpm_load_program(&cpm_state, program_file);
        } else {
            emulator_load_program(program_file, 0x8000);
            emulator.cpu.PC = 0x8000;
        }
    }
    
    printf("\nStarting emulator...\n");
    printf("Clock speed: %.2f MHz\n", emulator.clock_speed);
    printf("Debug mode: %s\n", emulator.debug_mode ? "ON" : "OFF");
    printf("CP/M mode: %s\n\n", emulator.cpm_mode ? "ON" : "OFF");
    
    /* Run emulator */
    if (emulator.debug_mode) {
        printf("Debug mode - type 'h' for help\n");
        debug_prompt();
    } else {
        emulator_run();
    }
    
    printf("\nEmulator stopped.\n");
    printf("Total cycles executed: %llu\n", emulator.total_cycles);
    
    return 0;
}

void emulator_init(void) {
    memset(&emulator, 0, sizeof(Emulator));
    emulator.clock_speed = 4.0;  /* 4 MHz */
    emulator.running = true;
    
    /* Initialize all subsystems */
    z80_init(&emulator.cpu);
    memory_init(&memory);
    gpu_init(&gpu);
    io_init();
    
    printf("Emulator initialized.\n");
}

void emulator_reset(void) {
    z80_reset(&emulator.cpu);
    memory_reset(&memory);
    gpu_reset(&gpu);
    io_reset();
    emulator.total_cycles = 0;
    printf("System reset.\n");
}

void emulator_run(void) {
    while (emulator.running && !emulator.cpu.halted) {
        /* Execute one instruction */
        int cycles = z80_execute(&emulator.cpu);
        emulator.total_cycles += cycles;
        
        /* Update peripherals */
        if (emulator.total_cycles % 1000 == 0) {
            io_update();
            gpu_update(&gpu);
        }
        
        /* Simple CPU throttling (not precise) */
        if (emulator.total_cycles % 100000 == 0) {
            /* Could add timing control here */
        }
    }
}

void emulator_step(void) {
    if (!emulator.cpu.halted) {
        int cycles = z80_execute(&emulator.cpu);
        emulator.total_cycles += cycles;
        io_update();
    }
}

void emulator_load_rom(const char *filename) {
    memory_load_rom(&memory, filename);
}

void emulator_load_program(const char *filename, uint16_t address) {
    FILE *f = fopen(filename, "rb");
    if (!f) {
        fprintf(stderr, "Error: Cannot open file %s\n", filename);
        return;
    }
    
    fseek(f, 0, SEEK_END);
    size_t size = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    uint8_t *data = malloc(size);
    fread(data, 1, size, f);
    fclose(f);
    
    memory_load_program(&memory, address, data, size);
    free(data);
    
    printf("Loaded %zu bytes to address 0x%04X\n", size, address);
}

void print_usage(const char *progname) {
    printf("Usage: %s [options] [program.bin]\n\n", progname);
    printf("Options:\n");
    printf("  -h, --help        Show this help message\n");
    printf("  -d, --debug       Enable debug mode\n");
    printf("  --cpm <disk.img>  Run in CP/M mode with disk image\n");
    printf("  --rom <file>      Load custom ROM file\n");
    printf("  --nobios          Don't load BIOS\n\n");
    printf("Examples:\n");
    printf("  %s                    # Run with BIOS\n", progname);
    printf("  %s program.bin        # Load and run program\n", progname);
    printf("  %s --cpm disk.img     # Run CP/M with disk\n", progname);
    printf("  %s --debug prog.bin   # Debug mode\n\n", progname);
}

void debug_prompt(void) {
    char cmd[256];
    
    while (emulator.running) {
        z80_dump_registers(&emulator.cpu);
        printf("\n[DBG] > ");
        
        if (!fgets(cmd, sizeof(cmd), stdin)) break;
        
        switch (cmd[0]) {
            case 's': /* Step */
            case 'n':
                emulator_step();
                break;
                
            case 'c': /* Continue */
                emulator.debug_mode = false;
                emulator_run();
                emulator.debug_mode = true;
                break;
                
            case 'r': /* Reset */
                emulator_reset();
                break;
                
            case 'm': /* Memory dump */
                {
                    uint16_t addr;
                    if (sscanf(cmd + 1, "%hx", &addr) == 1) {
                        memory_dump(addr, addr + 0xFF);
                    }
                }
                break;
                
            case 'g': /* Go to address */
                {
                    uint16_t addr;
                    if (sscanf(cmd + 1, "%hx", &addr) == 1) {
                        emulator.cpu.PC = addr;
                        printf("PC set to 0x%04X\n", addr);
                    }
                }
                break;
                
            case 'q': /* Quit */
                emulator.running = false;
                break;
                
            case 'h': /* Help */
            case '?':
                printf("Debug commands:\n");
                printf("  s/n       - Step one instruction\n");
                printf("  c         - Continue execution\n");
                printf("  r         - Reset system\n");
                printf("  m <addr>  - Dump memory\n");
                printf("  g <addr>  - Set PC to address\n");
                printf("  q         - Quit\n");
                printf("  h/?       - Show this help\n");
                break;
                
            default:
                printf("Unknown command. Type 'h' for help.\n");
        }
    }
}
