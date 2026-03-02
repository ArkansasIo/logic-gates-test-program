; BIOS - Basic Input/Output System
; 8-Bit Computer System
; Z80 Assembly

    ORG 0x0000

; BIOS Entry Points
BOOT:
    JP COLD_BOOT
WBOOT:
    JP WARM_BOOT
CONST:
    JP CONSOLE_STATUS
CONIN:
    JP CONSOLE_INPUT
CONOUT:
    JP CONSOLE_OUTPUT
LIST:
    JP LIST_OUTPUT
PUNCH:
    JP PUNCH_OUTPUT
READER:
    JP READER_INPUT

; System Variables
IOBYTE:
    DB 0x00
CDISK:
    DB 0x00
DMAADDR:
    DW 0x0080

; Cold Boot - System Initialization
COLD_BOOT:
    DI
    LD SP, 0xFFFF
    CALL INIT_GPU
    CALL INIT_CMOS
    LD HL, BOOT_MSG
    CALL PRINT_STRING
    JP OS_START

; Warm Boot - Restart
WARM_BOOT:
    DI
    LD SP, 0xFFFF
    JP OS_START

; Console Status - Check if character available
CONSOLE_STATUS:
    IN A, (0x11)
    AND 0x01
    RET

; Console Input - Read character
CONSOLE_INPUT:
    CALL CONSOLE_STATUS
    JR Z, CONSOLE_INPUT
    IN A, (0x10)
    RET

; Console Output - Write character
CONSOLE_OUTPUT:
    LD A, C
    OUT (0x09), A
    OUT (0x20), A
    RET

; Print String (HL = string address, 0 terminated)
PRINT_STRING:
    LD A, (HL)
    OR A
    RET Z
    LD C, A
    CALL CONSOLE_OUTPUT
    INC HL
    JR PRINT_STRING

; List Output
LIST_OUTPUT:
    RET

; Punch Output  
PUNCH_OUTPUT:
    RET

; Reader Input
READER_INPUT:
    LD A, 0x1A
    RET

; Initialize GPU
INIT_GPU:
    LD A, 0x03
    OUT (0x00), A
    LD A, 0
    OUT (0x02), A
    OUT (0x03), A
    LD A, 7
    OUT (0x04), A
    RET

; Initialize CMOS
INIT_CMOS:
    LD A, 0x10
    OUT (0x40), A
    IN A, (0x41)
    RET

; Boot Message
BOOT_MSG:
    DB "8-Bit Computer System v1.0", 13, 10
    DB "Z80 CPU @ 4MHz", 13, 10
    DB "64KB RAM, 8KB ROM", 13, 10
    DB 13, 10
    DB "BIOS Ready", 13, 10, 0

; OS Entry Point (will be loaded later)
OS_START:
    LD HL, OS_LOAD_MSG
    CALL PRINT_STRING
    
    ; Attempt to load OS from disk
    ; For now, jump to user program at 0x8000
    LD HL, 0x8000
    JP (HL)

OS_LOAD_MSG:
    DB "Loading OS...", 13, 10, 0

; Fill rest of ROM
    ORG 0x1FFF
    DB 0xFF
