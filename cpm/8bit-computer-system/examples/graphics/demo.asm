; Graphics Demo
; Demonstrates GPU drawing capabilities

    ORG 0x8000

START:
    ; Initialize GPU
    LD A, 0x05                  ; Enable display + graphics mode
    OUT (0x00), A
    
    ; Clear screen to black
    LD A, 0
    CALL CLEAR_SCREEN
    
    ; Draw some rectangles
    LD B, 10                    ; X position
    LD C, 10                    ; Y position
    LD D, 50                    ; Width
    LD E, 50                    ; Height
    LD A, 4                     ; Red color
    CALL DRAW_RECT
    
    LD B, 70
    LD C, 10
    LD D, 50
    LD E, 50
    LD A, 2                     ; Green color
    CALL DRAW_RECT
    
    LD B, 130
    LD C, 10
    LD D, 50
    LD E, 50
    LD A, 1                     ; Blue color
    CALL DRAW_RECT
    
    ; Display message
    LD A, 0x03                  ; Enable text mode
    OUT (0x00), A
    
    LD HL, MESSAGE
    CALL PRINT_STRING
    
    HALT

; Clear screen
; A = color
CLEAR_SCREEN:
    PUSH BC
    PUSH HL
    
    LD HL, 0xE000               ; Video RAM start
    LD BC, 0x2000               ; 8KB video RAM
.loop:
    LD (HL), A
    INC HL
    DEC BC
    LD A, B
    OR C
    JR NZ, .loop
    
    POP HL
    POP BC
    RET

; Draw rectangle (simplified)
; B = X, C = Y, D = Width, E = Height, A = Color
DRAW_RECT:
    PUSH AF
    PUSH BC
    PUSH DE
    
    LD A, B
    OUT (0x02), A               ; Set X
    LD A, C
    OUT (0x03), A               ; Set Y
    
    POP DE
    POP BC
    POP AF
    
    OUT (0x04), A               ; Set color
    
    ; Note: Real implementation would draw pixels
    ; This is simplified for demonstration
    
    RET

; Print string
PRINT_STRING:
    LD A, (HL)
    OR A
    RET Z
    OUT (0x09), A
    INC HL
    JR PRINT_STRING

MESSAGE:
    DB "Graphics Demo - Press any key", 13, 10, 0
