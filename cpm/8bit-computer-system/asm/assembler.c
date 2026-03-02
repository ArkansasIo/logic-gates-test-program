/*
 * Z80 Assembler
 * Simple two-pass assembler for Z80 assembly language
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <stdint.h>
#include <stdbool.h>

#define MAX_LABELS 1000
#define MAX_LINE_LEN 256
#define MAX_OUTPUT_SIZE 65536

/* Label structure */
typedef struct {
    char name[64];
    uint16_t address;
} Label;

/* Assembler state */
typedef struct {
    Label labels[MAX_LABELS];
    int label_count;
    uint8_t output[MAX_OUTPUT_SIZE];
    uint16_t pc;                /* Program counter */
    uint16_t org;               /* Origin address */
    int pass;                   /* 1 or 2 */
    int errors;
    int line_num;
} Assembler;

Assembler assembler;

/* Function prototypes */
void asm_init(void);
int asm_pass(FILE *input);
void asm_process_line(char *line);
void asm_add_label(const char *name, uint16_t address);
int asm_find_label(const char *name, uint16_t *address);
void asm_emit_byte(uint8_t byte);
void asm_emit_word(uint16_t word);
int asm_parse_instruction(char *line);
void asm_write_output(const char *filename);
void strip_comments(char *line);
void trim(char *str);

int main(int argc, char *argv[]) {
    printf("Z80 Assembler v1.0\n");
    
    if (argc < 2) {
        printf("Usage: %s <input.asm> [-o output.bin]\n", argv[0]);
        return 1;
    }
    
    const char *input_file = argv[1];
    const char *output_file = "out.bin";
    
    /* Parse command line arguments */
    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "-o") == 0 && i + 1 < argc) {
            output_file = argv[++i];
        }
    }
    
    /* Initialize assembler */
    asm_init();
    
    /* Pass 1: Collect labels */
    printf("Pass 1: Collecting labels...\n");
    assembler.pass = 1;
    FILE *f = fopen(input_file, "r");
    if (!f) {
        fprintf(stderr, "Error: Cannot open input file %s\n", input_file);
        return 1;
    }
    asm_pass(f);
    fclose(f);
    
    printf("Found %d labels\n", assembler.label_count);
    
    /* Pass 2: Generate code */
    printf("Pass 2: Generating code...\n");
    assembler.pass = 2;
    assembler.pc = assembler.org;
    f = fopen(input_file, "r");
    asm_pass(f);
    fclose(f);
    
    if (assembler.errors > 0) {
        fprintf(stderr, "Assembly failed with %d errors\n", assembler.errors);
        return 1;
    }
    
    /* Write output */
    asm_write_output(output_file);
    
    printf("Assembly successful: %d bytes written to %s\n",
           assembler.pc - assembler.org, output_file);
    
    return 0;
}

void asm_init(void) {
    memset(&assembler, 0, sizeof(Assembler));
    assembler.org = 0;
    assembler.pc = 0;
}

int asm_pass(FILE *input) {
    char line[MAX_LINE_LEN];
    assembler.line_num = 0;
    assembler.pc = assembler.org;
    
    while (fgets(line, sizeof(line), input)) {
        assembler.line_num++;
        asm_process_line(line);
    }
    
    return 0;
}

void asm_process_line(char *line) {
    strip_comments(line);
    trim(line);
    
    if (strlen(line) == 0) return;
    
    /* Check for label */
    char *colon = strchr(line, ':');
    if (colon) {
        *colon = '\0';
        trim(line);
        if (assembler.pass == 1) {
            asm_add_label(line, assembler.pc);
        }
        line = colon + 1;
        trim(line);
    }
    
    if (strlen(line) == 0) return;
    
    /* Parse instruction */
    asm_parse_instruction(line);
}

void asm_add_label(const char *name, uint16_t address) {
    if (assembler.label_count >= MAX_LABELS) {
        fprintf(stderr, "Error: Too many labels\n");
        assembler.errors++;
        return;
    }
    
    strncpy(assembler.labels[assembler.label_count].name, name, 63);
    assembler.labels[assembler.label_count].address = address;
    assembler.label_count++;
}

int asm_find_label(const char *name, uint16_t *address) {
    for (int i = 0; i < assembler.label_count; i++) {
        if (strcmp(assembler.labels[i].name, name) == 0) {
            *address = assembler.labels[i].address;
            return 1;
        }
    }
    return 0;
}

void asm_emit_byte(uint8_t byte) {
    if (assembler.pass == 2) {
        assembler.output[assembler.pc - assembler.org] = byte;
    }
    assembler.pc++;
}

void asm_emit_word(uint16_t word) {
    asm_emit_byte(word & 0xFF);
    asm_emit_byte(word >> 8);
}

int asm_parse_instruction(char *line) {
    char inst[16], arg1[64], arg2[64];
    memset(arg1, 0, sizeof(arg1));
    memset(arg2, 0, sizeof(arg2));
    
    int n = sscanf(line, "%15s %63s %63s", inst, arg1, arg2);
    
    if (n < 1) return 0;
    
    /* Remove trailing commas from arguments */
    if (arg1[strlen(arg1) - 1] == ',') arg1[strlen(arg1) - 1] = '\0';
    if (arg2[strlen(arg2) - 1] == ',') arg2[strlen(arg2) - 1] = '\0';
    
    /* Convert instruction to uppercase */
    for (char *p = inst; *p; p++) *p = toupper(*p);
    
    /* Parse directives */
    if (strcmp(inst, "ORG") == 0) {
        uint16_t addr;
        if (sscanf(arg1, "%hx", &addr) == 1 || sscanf(arg1, "%hu", &addr) == 1) {
            assembler.org = addr;
            assembler.pc = addr;
        }
        return 0;
    }
    
    if (strcmp(inst, "DB") == 0) {
        /* Data byte */
        uint8_t val;
        if (arg1[0] == '"') {
            /* String */
            for (char *p = arg1 + 1; *p && *p != '"'; p++) {
                asm_emit_byte(*p);
            }
        } else if (sscanf(arg1, "%hhx", &val) == 1 || sscanf(arg1, "%hhu", &val) == 1) {
            asm_emit_byte(val);
        }
        return 0;
    }
    
    if (strcmp(inst, "DW") == 0) {
        uint16_t val;
        if (sscanf(arg1, "%hx", &val) == 1 || sscanf(arg1, "%hu", &val) == 1) {
            asm_emit_word(val);
        }
        return 0;
    }
    
    if (strcmp(inst, "DS") == 0) {
        uint16_t size;
        if (sscanf(arg1, "%hu", &size) == 1) {
            for (int i = 0; i < size; i++) {
                asm_emit_byte(0);
            }
        }
        return 0;
    }
    
    /* Parse Z80 instructions */
    if (strcmp(inst, "NOP") == 0) {
        asm_emit_byte(0x00);
    }
    else if (strcmp(inst, "HALT") == 0) {
        asm_emit_byte(0x76);
    }
    else if (strcmp(inst, "DI") == 0) {
        asm_emit_byte(0xF3);
    }
    else if (strcmp(inst, "EI") == 0) {
        asm_emit_byte(0xFB);
    }
    else if (strcmp(inst, "RET") == 0) {
        asm_emit_byte(0xC9);
    }
    else if (strcmp(inst, "LD") == 0 && n >= 2) {
        /* Simplified LD instruction parsing */
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        for (char *p = arg2; *p; p++) *p = toupper(*p);
        
        if (strcmp(arg1, "A") == 0 && arg2[0] == '(') {
            /* LD A, (nn) */
            uint16_t addr;
            if (sscanf(arg2 + 1, "%hx", &addr) == 1) {
                asm_emit_byte(0x3A);
                asm_emit_word(addr);
            }
        }
        else if (strcmp(arg1, "HL") == 0) {
            uint16_t val;
            if (sscanf(arg2, "%hx", &val) == 1 || sscanf(arg2, "%hu", &val) == 1) {
                asm_emit_byte(0x21);
                asm_emit_word(val);
            }
        }
        else if (strcmp(arg1, "BC") == 0) {
            uint16_t val;
            if (sscanf(arg2, "%hx", &val) == 1) {
                asm_emit_byte(0x01);
                asm_emit_word(val);
            }
        }
        else if (strcmp(arg1, "SP") == 0) {
            uint16_t val;
            if (sscanf(arg2, "%hx", &val) == 1) {
                asm_emit_byte(0x31);
                asm_emit_word(val);
            }
        }
    }
    else if (strcmp(inst, "JP") == 0 || strcmp(inst, "JMP") == 0) {
        /* Handle indirect jump JP (HL) */
        if (strcmp(arg1, "(HL)") == 0 || strcmp(arg1, "(hl)") == 0) {
            asm_emit_byte(0xE9);  /* JP (HL) */
        } else {
            uint16_t addr;
            if (sscanf(arg1, "%hx", &addr) == 1) {
                asm_emit_byte(0xC3);
                asm_emit_word(addr);
            } else if (asm_find_label(arg1, &addr)) {
                asm_emit_byte(0xC3);
                asm_emit_word(addr);
            } else if (assembler.pass == 2) {
                fprintf(stderr, "Error line %d: Undefined label '%s'\n",
                        assembler.line_num, arg1);
                assembler.errors++;
            } else {
                asm_emit_byte(0xC3);
                asm_emit_word(0);
            }
        }
    }
    else if (strcmp(inst, "JR") == 0) {
        /* Check if conditional or unconditional */
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        
        uint8_t opcode = 0x18;  /* Default unconditional JR */
        char *target = arg1;
        
        /* Check for conditional JR */
        if (strcmp(arg1, "Z") == 0) {
            opcode = 0x28;
            target = arg2;
        } else if (strcmp(arg1, "NZ") == 0) {
            opcode = 0x20;
            target = arg2;
        } else if (strcmp(arg1, "C") == 0) {
            opcode = 0x38;
            target = arg2;
        } else if (strcmp(arg1, "NC") == 0) {
            opcode = 0x30;
            target = arg2;
        }
        
        asm_emit_byte(opcode);
        
        /* Calculate relative offset */
        uint16_t target_addr;
        if (asm_find_label(target, &target_addr)) {
            int16_t offset = target_addr - (assembler.pc + 1);
            if (offset < -128 || offset > 127) {
                if (assembler.pass == 2) {
                    fprintf(stderr, "Error line %d: JR offset out of range (%d bytes)\n",
                            assembler.line_num, offset);
                    assembler.errors++;
                }
            }
            asm_emit_byte((uint8_t)(offset & 0xFF));
        } else {
            asm_emit_byte(0x00);  /* Placeholder */
            if (assembler.pass == 2) {
                fprintf(stderr, "Error line %d: Undefined label '%s'\n",
                        assembler.line_num, target);
                assembler.errors++;
            }
        }
    }
    else if (strcmp(inst, "CALL") == 0) {
        uint16_t addr;
        if (sscanf(arg1, "%hx", &addr) == 1) {
            asm_emit_byte(0xCD);
            asm_emit_word(addr);
        } else if (asm_find_label(arg1, &addr)) {
            asm_emit_byte(0xCD);
            asm_emit_word(addr);
        }
    }
    else if (strcmp(inst, "OUT") == 0) {
        /* OUT (n), A */
        uint8_t port;
        if (sscanf(arg1 + 1, "%hhx", &port) == 1) {
            asm_emit_byte(0xD3);
            asm_emit_byte(port);
        }
    }
    else if (strcmp(inst, "IN") == 0) {
        /* IN A, (n) */
        uint8_t port;
        if (sscanf(arg2 + 1, "%hhx", &port) == 1) {
            asm_emit_byte(0xDB);
            asm_emit_byte(port);
        }
    }
    else if (strcmp(inst, "INC") == 0) {
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        if (strcmp(arg1, "HL") == 0) asm_emit_byte(0x23);
        else if (strcmp(arg1, "BC") == 0) asm_emit_byte(0x03);
        else if (strcmp(arg1, "B") == 0) asm_emit_byte(0x04);
    }
    else if (strcmp(inst, "DEC") == 0) {
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        if (strcmp(arg1, "B") == 0) asm_emit_byte(0x05);
    }
    else if (strcmp(inst, "AND") == 0) {
        /* AND A, r or AND n */
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        if (strcmp(arg1, "B") == 0) asm_emit_byte(0xA0);
        else if (strcmp(arg1, "C") == 0) asm_emit_byte(0xA1);
        else if (strcmp(arg1, "D") == 0) asm_emit_byte(0xA2);
        else if (strcmp(arg1, "E") == 0) asm_emit_byte(0xA3);
        else if (strcmp(arg1, "H") == 0) asm_emit_byte(0xA4);
        else if (strcmp(arg1, "L") == 0) asm_emit_byte(0xA5);
        else if (strcmp(arg1, "A") == 0) asm_emit_byte(0xA7);
        else {
            uint8_t val;
            if (sscanf(arg1, "%hhx", &val) == 1) {
                asm_emit_byte(0xE6);
                asm_emit_byte(val);
            }
        }
    }
    else if (strcmp(inst, "OR") == 0) {
        /* OR A, r or OR n */
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        if (strcmp(arg1, "B") == 0) asm_emit_byte(0xB0);
        else if (strcmp(arg1, "C") == 0) asm_emit_byte(0xB1);
        else if (strcmp(arg1, "D") == 0) asm_emit_byte(0xB2);
        else if (strcmp(arg1, "E") == 0) asm_emit_byte(0xB3);
        else if (strcmp(arg1, "H") == 0) asm_emit_byte(0xB4);
        else if (strcmp(arg1, "L") == 0) asm_emit_byte(0xB5);
        else if (strcmp(arg1, "A") == 0) asm_emit_byte(0xB7);
        else {
            uint8_t val;
            if (sscanf(arg1, "%hhx", &val) == 1) {
                asm_emit_byte(0xF6);
                asm_emit_byte(val);
            }
        }
    }
    else if (strcmp(inst, "XOR") == 0) {
        /* XOR A, r or XOR n */
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        if (strcmp(arg1, "B") == 0) asm_emit_byte(0xA8);
        else if (strcmp(arg1, "C") == 0) asm_emit_byte(0xA9);
        else if (strcmp(arg1, "D") == 0) asm_emit_byte(0xAA);
        else if (strcmp(arg1, "E") == 0) asm_emit_byte(0xAB);
        else if (strcmp(arg1, "H") == 0) asm_emit_byte(0xAC);
        else if (strcmp(arg1, "L") == 0) asm_emit_byte(0xAD);
        else if (strcmp(arg1, "A") == 0) asm_emit_byte(0xAF);
        else {
            uint8_t val;
            if (sscanf(arg1, "%hhx", &val) == 1) {
                asm_emit_byte(0xEE);
                asm_emit_byte(val);
            }
        }
    }
    else if (strcmp(inst, "PUSH") == 0) {
        /* PUSH rr */
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        if (strcmp(arg1, "BC") == 0) asm_emit_byte(0xC5);
        else if (strcmp(arg1, "DE") == 0) asm_emit_byte(0xD5);
        else if (strcmp(arg1, "HL") == 0) asm_emit_byte(0xE5);
        else if (strcmp(arg1, "AF") == 0) asm_emit_byte(0xF5);
    }
    else if (strcmp(inst, "POP") == 0) {
        /* POP rr */
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        if (strcmp(arg1, "BC") == 0) asm_emit_byte(0xC1);
        else if (strcmp(arg1, "DE") == 0) asm_emit_byte(0xD1);
        else if (strcmp(arg1, "HL") == 0) asm_emit_byte(0xE1);
        else if (strcmp(arg1, "AF") == 0) asm_emit_byte(0xF1);
    }
    else if (strcmp(inst, "CP") == 0 || strcmp(inst, "CMP") == 0) {
        /* CP A, r or CP n (Compare) */
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        if (strcmp(arg1, "B") == 0) asm_emit_byte(0xB8);
        else if (strcmp(arg1, "C") == 0) asm_emit_byte(0xB9);
        else if (strcmp(arg1, "D") == 0) asm_emit_byte(0xBA);
        else if (strcmp(arg1, "E") == 0) asm_emit_byte(0xBB);
        else if (strcmp(arg1, "H") == 0) asm_emit_byte(0xBC);
        else if (strcmp(arg1, "L") == 0) asm_emit_byte(0xBD);
        else if (strcmp(arg1, "A") == 0) asm_emit_byte(0xBF);
        else {
            uint8_t val;
            if (sscanf(arg1, "%hhx", &val) == 1) {
                asm_emit_byte(0xFE);
                asm_emit_byte(val);
            }
        }
    }
    else if (strcmp(inst, "IM") == 0) {
        /* Set interrupt mode IM 0, IM 1, or IM 2 */
        int mode;
        if (sscanf(arg1, "%d", &mode) == 1) {
            if (mode == 0) {
                asm_emit_byte(0xED);
                asm_emit_byte(0x46);
            } else if (mode == 1) {
                asm_emit_byte(0xED);
                asm_emit_byte(0x56);
            } else if (mode == 2) {
                asm_emit_byte(0xED);
                asm_emit_byte(0x5E);
            }
        }
    }
    else if (strcmp(inst, "SUB") == 0) {
        /* SUB A, r or SUB n */
        for (char *p = arg1; *p; p++) *p = toupper(*p);
        if (strcmp(arg1, "B") == 0) asm_emit_byte(0x90);
        else if (strcmp(arg1, "C") == 0) asm_emit_byte(0x91);
        else if (strcmp(arg1, "D") == 0) asm_emit_byte(0x92);
        else if (strcmp(arg1, "E") == 0) asm_emit_byte(0x93);
        else if (strcmp(arg1, "H") == 0) asm_emit_byte(0x94);
        else if (strcmp(arg1, "L") == 0) asm_emit_byte(0x95);
        else if (strcmp(arg1, "A") == 0) asm_emit_byte(0x97);
        else {
            uint8_t val;
            if (sscanf(arg1, "%hhx", &val) == 1) {
                asm_emit_byte(0xD6);
                asm_emit_byte(val);
            }
        }
    }
    else {
        if (assembler.pass == 2) {
            fprintf(stderr, "Warning line %d: Unknown instruction '%s'\n",
                    assembler.line_num, inst);
        }
    }
    
    return 0;
}

void asm_write_output(const char *filename) {
    FILE *f = fopen(filename, "wb");
    if (!f) {
        fprintf(stderr, "Error: Cannot write output file %s\n", filename);
        return;
    }
    
    fwrite(assembler.output, 1, assembler.pc - assembler.org, f);
    fclose(f);
}

void strip_comments(char *line) {
    char *comment = strchr(line, ';');
    if (comment) *comment = '\0';
}

void trim(char *str) {
    /* Trim leading whitespace */
    char *start = str;
    while (*start && isspace(*start)) start++;
    
    if (start != str) {
        memmove(str, start, strlen(start) + 1);
    }
    
    /* Trim trailing whitespace */
    char *end = str + strlen(str) - 1;
    while (end > str && isspace(*end)) {
        *end = '\0';
        end--;
    }
}
