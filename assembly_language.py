"""
8-bit Assembly Language Programs and Assembler
Converts assembly mnemonics to machine code
"""

from typing import List, Dict, Tuple
from computer_components import Opcode

# ============================================================================
# ASSEMBLER
# ============================================================================

class Assembler:
    """Simple 8-bit assembler"""
    
    # Instruction set mapping
    INSTRUCTIONS = {
        'NOP': 0x00,
        'LDA': 0x01,
        'LDB': 0x02,
        'STA': 0x03,
        'STB': 0x04,
        'ADD': 0x10,
        'SUB': 0x11,
        'AND': 0x12,
        'OR': 0x13,
        'XOR': 0x14,
        'NOT': 0x15,
        'SHL': 0x16,
        'SHR': 0x17,
        'JMP': 0x20,
        'JZ': 0x21,
        'JNZ': 0x22,
        'CALL': 0x30,
        'RET': 0x31,
        'PUSH': 0x40,
        'POP': 0x41,
        'HLT': 0xFF
    }
    
    def __init__(self):
        self.labels = {}
        self.machine_code = []
        self.address = 0
    
    def parse_line(self, line: str) -> Tuple[str, List[str]]:
        """Parse assembly line into instruction and operands"""
        # Remove comments
        if ';' in line:
            line = line[:line.index(';')]
        
        line = line.strip()
        if not line:
            return None, []
        
        # Check for label
        if ':' in line:
            label, line = line.split(':', 1)
            self.labels[label.strip()] = self.address
            line = line.strip()
            if not line:
                return None, []
        
        parts = line.split()
        instruction = parts[0].upper()
        operands = parts[1:] if len(parts) > 1 else []
        
        return instruction, operands
    
    def parse_operand(self, operand: str) -> int:
        """Parse operand (immediate value, label, or address)"""
        operand = operand.strip(',')
        
        # Check if it's a label
        if operand in self.labels:
            return self.labels[operand]
        
        # Check if it's hex
        if operand.startswith('0x') or operand.startswith('0X'):
            return int(operand, 16)
        
        # Check if it's binary
        if operand.startswith('0b') or operand.startswith('0B'):
            return int(operand, 2)
        
        # Assume decimal
        return int(operand)
    
    def assemble(self, assembly_code: str) -> List[int]:
        """Assemble code into machine code"""
        lines = assembly_code.split('\n')
        
        # First pass: collect labels
        self.address = 0
        for line in lines:
            instruction, operands = self.parse_line(line)
            if instruction and instruction in self.INSTRUCTIONS:
                self.address += 1
                if len(operands) > 0:
                    self.address += len(operands)
        
        # Second pass: generate machine code
        self.address = 0
        self.machine_code = []
        
        for line in lines:
            instruction, operands = self.parse_line(line)
            if instruction and instruction in self.INSTRUCTIONS:
                opcode = self.INSTRUCTIONS[instruction]
                self.machine_code.append(opcode)
                self.address += 1
                
                for operand in operands:
                    value = self.parse_operand(operand)
                    self.machine_code.append(value & 0xFF)
                    self.address += 1
        
        return self.machine_code
    
    def disassemble(self, machine_code: List[int]) -> str:
        """Disassemble machine code to assembly"""
        output = []
        reverse_instructions = {v: k for k, v in self.INSTRUCTIONS.items()}
        i = 0
        
        while i < len(machine_code):
            opcode = machine_code[i]
            if opcode in reverse_instructions:
                mnemonic = reverse_instructions[opcode]
                line = f"{i:04X}: {opcode:02X}  {mnemonic}"
                i += 1
                
                # Instructions with operands
                if mnemonic in ['LDA', 'LDB', 'STA', 'STB', 'JMP', 'JZ', 'JNZ', 'CALL']:
                    if i < len(machine_code):
                        operand = machine_code[i]
                        line += f" 0x{operand:02X}"
                        i += 1
                
                output.append(line)
            else:
                output.append(f"{i:04X}: {opcode:02X}  ???")
                i += 1
        
        return '\n'.join(output)

# ============================================================================
# SAMPLE ASSEMBLY PROGRAMS
# ============================================================================

# Program 1: Add two numbers
PROGRAM_ADD = """
; Add two numbers
; Result: A = 5 + 3 = 8

    LDA 0x10    ; Load value from address 0x10 into A
    LDB 0x11    ; Load value from address 0x11 into B
    ADD         ; A = A + B
    STA 0x12    ; Store result at address 0x12
    HLT         ; Halt
"""

# Program 2: Count from 0 to 10
PROGRAM_COUNTER = """
; Counter from 0 to 10

start:
    LDA 0x20    ; Load counter
    LDB 0x21    ; Load constant 1
    ADD         ; Increment counter
    STA 0x20    ; Store counter
    LDB 0x22    ; Load limit (10)
    SUB         ; Compare (A - 10)
    JZ end      ; If zero, exit
    JMP start   ; Loop
end:
    HLT         ; Halt
"""

# Program 3: Logic operations
PROGRAM_LOGIC = """
; Logic gate operations

    LDA 0x30    ; Load first value
    LDB 0x31    ; Load second value
    
    AND         ; A = A AND B
    STA 0x40    ; Store AND result
    
    LDA 0x30    ; Reload first value
    LDB 0x31    ; Reload second value
    OR          ; A = A OR B
    STA 0x41    ; Store OR result
    
    LDA 0x30    ; Reload first value
    LDB 0x31    ; Reload second value
    XOR         ; A = A XOR B
    STA 0x42    ; Store XOR result
    
    LDA 0x30    ; Load first value
    NOT         ; A = NOT A
    STA 0x43    ; Store NOT result
    
    HLT         ; Halt
"""

# Program 4: Multiply by 2 using shift
PROGRAM_SHIFT = """
; Multiply by 2 using left shift

    LDA 0x50    ; Load value
    SHL         ; Shift left (multiply by 2)
    STA 0x51    ; Store result
    HLT         ; Halt
"""

# Program 5: Sum array
PROGRAM_SUM_ARRAY = """
; Sum array of numbers

    LDA 0x60    ; Load array[0]
    LDB 0x61    ; Load array[1]
    ADD         ; Sum
    LDB 0x62    ; Load array[2]
    ADD         ; Sum
    LDB 0x63    ; Load array[3]
    ADD         ; Sum
    STA 0x70    ; Store total
    HLT         ; Halt
"""

# Program 6: Max of two numbers
PROGRAM_MAX = """
; Find max of two numbers

    LDA 0x80    ; Load first number
    LDB 0x81    ; Load second number
    SUB         ; A = A - B
    JZ equal    ; If equal
    ; If positive, first is larger
    LDA 0x80    ; Load first
    STA 0x82    ; Store as max
    JMP done
equal:
    LDA 0x80    ; Load first (they're equal)
    STA 0x82    ; Store as max
done:
    HLT         ; Halt
"""

# Program 7: Bitwise operations demo
PROGRAM_BITWISE = """
; Bitwise operations demonstration
; Using logic gates on 8-bit values

    ; AND operation (both bits must be 1)
    LDA 0xF0    ; 11110000
    LDB 0x0F    ; 00001111
    AND         ; 00000000
    STA 0x90    ; Store AND result
    
    ; OR operation (at least one bit is 1)
    LDA 0xF0    ; 11110000
    LDB 0x0F    ; 00001111
    OR          ; 11111111
    STA 0x91    ; Store OR result
    
    ; XOR operation (bits are different)
    LDA 0xAA    ; 10101010
    LDB 0x55    ; 01010101
    XOR         ; 11111111
    STA 0x92    ; Store XOR result
    
    ; NOT operation (invert all bits)
    LDA 0xAA    ; 10101010
    NOT         ; 01010101
    STA 0x93    ; Store NOT result
    
    HLT         ; Halt
"""

def demo_assembler():
    """Demonstrate assembler functionality"""
    print("=" * 60)
    print("8-BIT ASSEMBLER DEMONSTRATION")
    print("=" * 60)
    
    assembler = Assembler()
    
    # Assemble program
    print("\nAssembling: Simple Addition Program")
    print("=" * 60)
    print(PROGRAM_ADD)
    
    machine_code = assembler.assemble(PROGRAM_ADD)
    
    print("\nMachine Code (Hex):")
    print(" ".join(f"{byte:02X}" for byte in machine_code))
    
    print("\nMachine Code (Binary):")
    for byte in machine_code:
        print(f"{byte:02X}: {byte:08b}")
    
    print("\n" + "=" * 60)
    print("DISASSEMBLY")
    print("=" * 60)
    disassembled = assembler.disassemble(machine_code)
    print(disassembled)
    
    # Assemble all programs
    print("\n" + "=" * 60)
    print("ALL SAMPLE PROGRAMS")
    print("=" * 60)
    
    programs = [
        ("Addition", PROGRAM_ADD),
        ("Counter", PROGRAM_COUNTER),
        ("Logic Operations", PROGRAM_LOGIC),
        ("Shift (Multiply by 2)", PROGRAM_SHIFT),
        ("Array Sum", PROGRAM_SUM_ARRAY),
        ("Max of Two", PROGRAM_MAX),
        ("Bitwise Operations", PROGRAM_BITWISE)
    ]
    
    for name, code in programs:
        assembler = Assembler()
        machine_code = assembler.assemble(code)
        print(f"\n{name}: {len(machine_code)} bytes")

if __name__ == "__main__":
    demo_assembler()
