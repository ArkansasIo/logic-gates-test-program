; Hello World Example
; Simple program that displays "Hello, World!" and halts

    ORG 0x8000

START:
    LD HL, MESSAGE              ; Load message address
    CALL PRINT_STRING           ; Print the string
    HALT                        ; Stop execution

; Print string routine
; HL = pointer to null-terminated string
PRINT_STRING:
    LD A, (HL)                  ; Load character
    OR A                        ; Check if zero
    RET Z                       ; Return if end of string
    OUT (0x09), A               ; Output to GPU
    OUT (0x20), A               ; Output to serial
    INC HL                      ; Next character
    JR PRINT_STRING             ; Loop

MESSAGE:
    DB "Hello, World!", 13, 10, 0

; End of program
