; Operating System Kernel
; Simple multitasking OS for 8-bit computer

    ORG 0x2000

; Kernel Entry Point
KERNEL_START:
    DI
    LD SP, 0xF000               ; Kernel stack
    
    CALL INIT_KERNEL
    CALL PRINT_BANNER
    
    EI                          ; Enable interrupts
    JMP SHELL                   ; Start command shell

; Initialize Kernel
INIT_KERNEL:
    ; Setup interrupt vector
    LD A, 0x20
    LD I, A
    IM 2
    
    ; Initialize memory manager
    CALL INIT_MEMORY
    
    ; Initialize file system
    CALL INIT_FS
    
    RET

; Print OS Banner
PRINT_BANNER:
    LD HL, BANNER
    CALL BIOS_PRINT
    RET

BANNER:
    DB "========================================", 13, 10
    DB "  8-Bit Computer OS v1.0", 13, 10
    DB "  Copyright 2026", 13, 10
    DB "========================================", 13, 10
    DB 13, 10, 0

; Command Shell
SHELL:
    LD HL, PROMPT
    CALL BIOS_PRINT
    
    ; Read command
    LD HL, CMD_BUFFER
    CALL READ_LINE
    
    ; Parse and execute command
    CALL PARSE_CMD
    CALL EXEC_CMD
    
    JR SHELL

PROMPT:
    DB "> ", 0

CMD_BUFFER:
    DS 128                      ; Command buffer

; Read line from console
READ_LINE:
    LD B, 0                     ; Character count
.loop:
    CALL BIOS_CONIN             ; Read character
    CP 13                       ; Enter?
    JR Z, .done
    CP 8                        ; Backspace?
    JR Z, .backspace
    
    ; Store character
    LD (HL), A
    INC HL
    INC B
    
    ; Echo character
    LD C, A
    CALL BIOS_CONOUT
    
    JR .loop

.backspace:
    LD A, B
    OR A
    JR Z, .loop                 ; Nothing to delete
    DEC HL
    DEC B
    LD C, 8
    CALL BIOS_CONOUT
    JR .loop

.done:
    LD (HL), 0                  ; Null terminate
    LD C, 13
    CALL BIOS_CONOUT
    LD C, 10
    CALL BIOS_CONOUT
    RET

; Parse command
PARSE_CMD:
    ; TODO: Parse command and arguments
    RET

; Execute command
EXEC_CMD:
    ; Check for built-in commands
    LD HL, CMD_BUFFER
    LD DE, CMD_HELP
    CALL STR_COMPARE
    JR Z, HELP_CMD
    
    LD HL, CMD_BUFFER
    LD DE, CMD_DIR
    CALL STR_COMPARE
    JR Z, DIR_CMD
    
    LD HL, CMD_BUFFER
    LD DE, CMD_CLS
    CALL STR_COMPARE
    JR Z, CLS_CMD
    
    ; Unknown command
    LD HL, UNKNOWN_MSG
    CALL BIOS_PRINT
    RET

; Built-in Commands
HELP_CMD:
    LD HL, HELP_MSG
    CALL BIOS_PRINT
    RET

DIR_CMD:
    LD HL, DIR_MSG
    CALL BIOS_PRINT
    RET

CLS_CMD:
    LD A, 12                    ; Form feed
    OUT (0x09), A
    RET

; Command strings
CMD_HELP:   DB "help", 0
CMD_DIR:    DB "dir", 0
CMD_CLS:    DB "cls", 0

HELP_MSG:
    DB "Available commands:", 13, 10
    DB "  help  - Show this help", 13, 10
    DB "  dir   - List files", 13, 10
    DB "  cls   - Clear screen", 13, 10
    DB "  ver   - Show version", 13, 10
    DB 0

DIR_MSG:
    DB "Directory listing:", 13, 10
    DB "  No files", 13, 10, 0

UNKNOWN_MSG:
    DB "Unknown command. Type 'help' for help.", 13, 10, 0

; String compare (HL, DE)
STR_COMPARE:
    LD A, (DE)
    CP (HL)
    RET NZ
    OR A
    RET Z
    INC HL
    INC DE
    JR STR_COMPARE

; Memory Manager
INIT_MEMORY:
    ; TODO: Initialize memory management
    RET

; File System
INIT_FS:
    ; TODO: Initialize file system
    RET

; BIOS Wrappers
BIOS_PRINT:
    LD A, (HL)
    OR A
    RET Z
    LD C, A
    CALL BIOS_CONOUT
    INC HL
    JR BIOS_PRINT

BIOS_CONIN:
    CALL 0x0009                 ; BIOS CONIN
    RET

BIOS_CONOUT:
    CALL 0x000C                 ; BIOS CONOUT
    RET
