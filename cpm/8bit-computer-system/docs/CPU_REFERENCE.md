# Z80 CPU Instruction Set Reference

## Overview
The Z80 CPU is an 8-bit microprocessor with:
- 8-bit data bus
- 16-bit address bus (64KB address space)
- 158 instructions
- 4 MHz clock speed (in this emulator)

## Register Set

### Main Registers
- **A** - Accumulator (8-bit)
- **F** - Flags (8-bit): S Z X H X P/V N C
- **B, C** - BC register pair (16-bit)
- **D, E** - DE register pair (16-bit)
- **H, L** - HL register pair (16-bit)

### Special Registers
- **PC** - Program Counter (16-bit)
- **SP** - Stack Pointer (16-bit)
- **IX, IY** - Index registers (16-bit)
- **I** - Interrupt vector (8-bit)
- **R** - Memory refresh (8-bit)

### Alternate Registers
- **A', F'** - Alternate accumulator and flags
- **BC', DE', HL'** - Alternate register pairs

## Flags
- **S** (Sign) - Set if result is negative
- **Z** (Zero) - Set if result is zero
- **H** (Half Carry) - Carry from bit 3 to bit 4
- **P/V** (Parity/Overflow) - Parity or overflow
- **N** (Add/Subtract) - Last operation was subtraction
- **C** (Carry) - Carry from bit 7

## Instruction Groups

### Load Instructions
```
LD r, n         ; Load immediate
LD r, r'        ; Load register to register
LD r, (HL)      ; Load from memory
LD (HL), r      ; Store to memory
LD A, (nn)      ; Load from address
LD (nn), A      ; Store to address
LD rr, nn       ; Load 16-bit immediate
PUSH rr         ; Push to stack
POP rr          ; Pop from stack
```

### Arithmetic Instructions
```
ADD A, r        ; Add
ADC A, r        ; Add with carry
SUB r           ; Subtract
SBC A, r        ; Subtract with carry
AND r           ; Logical AND
OR r            ; Logical OR
XOR r           ; Logical XOR
CP r            ; Compare
INC r           ; Increment
DEC r           ; Decrement
```

### Jump/Call Instructions
```
JP nn           ; Jump unconditional
JP cc, nn       ; Jump conditional
JR e            ; Jump relative
CALL nn         ; Call subroutine
RET             ; Return
RST p           ; Restart
```

### I/O Instructions
```
IN A, (n)       ; Input from port
OUT (n), A      ; Output to port
```

### Control Instructions
```
NOP             ; No operation
HALT            ; Halt CPU
DI              ; Disable interrupts
EI              ; Enable interrupts
IM 0/1/2        ; Set interrupt mode
```

## Addressing Modes

1. **Immediate**: `LD A, 5`
2. **Register**: `LD A, B`
3. **Direct**: `LD A, (0x8000)`
4. **Indirect**: `LD A, (HL)`
5. **Indexed**: `LD A, (IX+5)`

## Example Programs

### Hello World
```asm
    ORG 0x8000
    LD HL, message
loop:
    LD A, (HL)
    OR A
    RET Z
    OUT (0x09), A
    INC HL
    JR loop
message:
    DB "Hello!", 0
```

### Loop Counter
```asm
    LD B, 10
loop:
    ; Do something
    DEC B
    JR NZ, loop
    RET
```

### Stack Usage
```asm
    LD HL, 0x1234
    PUSH HL
    ; Do something
    POP DE
    RET
```

## Timing
Most instructions take 4-7 cycles. Some examples:
- NOP: 4 cycles
- LD r, n: 7 cycles
- ADD A, r: 4 cycles
- JP nn: 10 cycles
- CALL nn: 17 cycles

## References
- Z80 CPU User Manual
- Zilog Z80 Programming Manual
- http://www.z80.info/
