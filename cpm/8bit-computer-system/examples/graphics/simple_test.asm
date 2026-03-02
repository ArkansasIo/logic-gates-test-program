; Simple Graphics Test
    ORG 0x8000

START:
    ; Initialize GPU to graphics mode
    LD A, 0x05
    OUT (0x00), A
    
    ; Set pixel at (10,10) to color 4 (red)
    LD A, 10
    OUT (0x02), A
    LD A, 10
    OUT (0x03), A
    LD A, 4
    OUT (0x04), A
    
    ; Switch to text mode
    LD A, 0x03
    OUT (0x00), A
    
    ; Print message
    LD HL, MESSAGE
PRINT_LOOP:
    LD A, (HL)
    OR A
    JR Z, DONE
    OUT (0x09), A
    INC HL
    JR PRINT_LOOP

DONE:
    HALT

MESSAGE:
    DB "Graphics Test OK", 0
