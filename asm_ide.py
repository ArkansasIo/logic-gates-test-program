"""
ASSEMBLY (ASM) IDE
==================
Assembly language IDE with syntax highlighting, instruction validation, and debugging
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum

# ============================================================================
# ASM ENUMERATION & DATA CLASSES
# ============================================================================

class ASMArchitecture(Enum):
    """Supported assembly architectures"""
    X86 = "x86"
    X86_64 = "x86_64"
    ARM = "arm"
    ARM64 = "arm64"
    MIPS = "mips"
    CUSTOM = "custom"

class RegisterSize(Enum):
    """Register sizes"""
    BYTE = 8
    WORD = 16
    DWORD = 32
    QWORD = 64

@dataclass
class ASMInstruction:
    """Assembly instruction definition"""
    mnemonic: str
    operands: int = 0  # Number of operands
    description: str = ""
    valid_archs: List[ASMArchitecture] = field(default_factory=lambda: [ASMArchitecture.X86, ASMArchitecture.X86_64])
    execution_cycles: int = 1

@dataclass
class ASMRegister:
    """Register definition"""
    name: str
    size: RegisterSize
    architecture: ASMArchitecture
    aliases: List[str] = field(default_factory=list)

# ============================================================================
# ASM INSTRUCTION DATABASE
# ============================================================================

class ASMInstructionDatabase:
    """Database of assembly instructions"""
    
    def __init__(self, arch: ASMArchitecture):
        self.arch = arch
        self.instructions: Dict[str, ASMInstruction] = {}
        self._load_instructions()
        
    def _load_instructions(self):
        """Load standard instructions"""
        # Data movement
        self.instructions["MOV"] = ASMInstruction("MOV", 2, "Move data", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["LEA"] = ASMInstruction("LEA", 2, "Load effective address", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        self.instructions["PUSH"] = ASMInstruction("PUSH", 1, "Push onto stack", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        self.instructions["POP"] = ASMInstruction("POP", 1, "Pop from stack", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        
        # Arithmetic
        self.instructions["ADD"] = ASMInstruction("ADD", 2, "Add", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["SUB"] = ASMInstruction("SUB", 2, "Subtract", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["MUL"] = ASMInstruction("MUL", 1, "Multiply", [ASMArchitecture.X86, ASMArchitecture.X86_64], 3)
        self.instructions["IMUL"] = ASMInstruction("IMUL", 2, "Signed multiply", [ASMArchitecture.X86, ASMArchitecture.X86_64], 3)
        self.instructions["DIV"] = ASMInstruction("DIV", 1, "Divide", [ASMArchitecture.X86, ASMArchitecture.X86_64], 10)
        self.instructions["IDIV"] = ASMInstruction("IDIV", 1, "Signed divide", [ASMArchitecture.X86, ASMArchitecture.X86_64], 10)
        
        # Bitwise
        self.instructions["AND"] = ASMInstruction("AND", 2, "Bitwise AND", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["OR"] = ASMInstruction("OR", 2, "Bitwise OR", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["XOR"] = ASMInstruction("XOR", 2, "Bitwise XOR", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["NOT"] = ASMInstruction("NOT", 1, "Bitwise NOT", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["SHL"] = ASMInstruction("SHL", 2, "Shift left", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["SHR"] = ASMInstruction("SHR", 2, "Shift right", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        
        # Comparison & jumps
        self.instructions["CMP"] = ASMInstruction("CMP", 2, "Compare", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["JMP"] = ASMInstruction("JMP", 1, "Jump", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        self.instructions["JE"] = ASMInstruction("JE", 1, "Jump if equal", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        self.instructions["JNE"] = ASMInstruction("JNE", 1, "Jump if not equal", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        self.instructions["JG"] = ASMInstruction("JG", 1, "Jump if greater", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        self.instructions["JL"] = ASMInstruction("JL", 1, "Jump if less", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        self.instructions["CALL"] = ASMInstruction("CALL", 1, "Call subroutine", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        self.instructions["RET"] = ASMInstruction("RET", 0, "Return from subroutine", [ASMArchitecture.X86, ASMArchitecture.X86_64], 2)
        
        # Other
        self.instructions["INC"] = ASMInstruction("INC", 1, "Increment", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["DEC"] = ASMInstruction("DEC", 1, "Decrement", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["NOP"] = ASMInstruction("NOP", 0, "No operation", [ASMArchitecture.X86, ASMArchitecture.X86_64], 1)
        self.instructions["SYSCALL"] = ASMInstruction("SYSCALL", 0, "System call", [ASMArchitecture.X86_64], 50)
    
    def is_valid_instruction(self, mnemonic: str) -> bool:
        """Check if instruction exists for architecture"""
        if mnemonic not in self.instructions:
            return False
        instr = self.instructions[mnemonic]
        return self.arch in instr.valid_archs
    
    def get_instruction(self, mnemonic: str) -> Optional[ASMInstruction]:
        """Get instruction details"""
        instr = self.instructions.get(mnemonic.upper())
        if instr and self.arch in instr.valid_archs:
            return instr
        return None

# ============================================================================
# ASM REGISTER DATABASE
# ============================================================================

class ASMRegisterDatabase:
    """Database of registers"""
    
    def __init__(self, arch: ASMArchitecture):
        self.arch = arch
        self.registers: Dict[str, ASMRegister] = {}
        self._load_registers()
        
    def _load_registers(self):
        """Load registers for architecture"""
        if self.arch in [ASMArchitecture.X86, ASMArchitecture.X86_64]:
            # General purpose registers
            self.registers["RAX"] = ASMRegister("RAX", RegisterSize.QWORD, self.arch, ["EAX", "AX", "AL", "AH"])
            self.registers["RBX"] = ASMRegister("RBX", RegisterSize.QWORD, self.arch, ["EBX", "BX", "BL", "BH"])
            self.registers["RCX"] = ASMRegister("RCX", RegisterSize.QWORD, self.arch, ["ECX", "CX", "CL", "CH"])
            self.registers["RDX"] = ASMRegister("RDX", RegisterSize.QWORD, self.arch, ["EDX", "DX", "DL", "DH"])
            self.registers["RSP"] = ASMRegister("RSP", RegisterSize.QWORD, self.arch, ["ESP", "SP"])  # Stack pointer
            self.registers["RBP"] = ASMRegister("RBP", RegisterSize.QWORD, self.arch, ["EBP", "BP"])  # Base pointer
            self.registers["RSI"] = ASMRegister("RSI", RegisterSize.QWORD, self.arch, ["ESI", "SI"])  # Source index
            self.registers["RDI"] = ASMRegister("RDI", RegisterSize.QWORD, self.arch, ["EDI", "DI"])  # Destination index
    
    def is_valid_register(self, name: str) -> bool:
        """Check if register exists"""
        reg_upper = name.upper()
        if reg_upper in self.registers:
            return True
        # Check aliases
        for reg in self.registers.values():
            if reg_upper in [a.upper() for a in reg.aliases]:
                return True
        return False
    
    def get_register(self, name: str) -> Optional[ASMRegister]:
        """Get register details"""
        reg_upper = name.upper()
        if reg_upper in self.registers:
            return self.registers[reg_upper]
        for reg in self.registers.values():
            if reg_upper in [a.upper() for a in reg.aliases]:
                return reg
        return None

# ============================================================================
# ASM LEXER & PARSER
# ============================================================================

@dataclass
class ASMToken:
    """Token from assembly code"""
    type: str  # keyword, register, number, label, comment, etc.
    value: str
    line: int
    column: int

class ASMLexer:
    """Assembly language lexer"""
    
    def __init__(self, arch: ASMArchitecture):
        self.arch = arch
        self.instr_db = ASMInstructionDatabase(arch)
        self.reg_db = ASMRegisterDatabase(arch)
        
    def tokenize(self, code: str) -> List[ASMToken]:
        """Tokenize assembly code"""
        tokens: List[ASMToken] = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines):
            column = 0
            # Remove comments
            if ';' in line:
                comment_pos = line.index(';')
                tokens.append(ASMToken("comment", line[comment_pos:], line_num, comment_pos))
                line = line[:comment_pos]
            
            line = line.strip()
            if not line:
                continue
            
            # Check for label (ends with :)
            if ':' in line:
                label_part = line.split(':')[0].strip()
                tokens.append(ASMToken("label", label_part + ":", line_num, column))
                line = line.split(':', 1)[1].strip()
                if not line:
                    continue
            
            # Parse instruction and operands
            parts = line.replace(',', ' ').split()
            for i, part in enumerate(parts):
                part_upper = part.upper()
                if self.instr_db.is_valid_instruction(part_upper):
                    tokens.append(ASMToken("instruction", part_upper, line_num, column))
                elif self.reg_db.is_valid_register(part):
                    tokens.append(ASMToken("register", part.upper(), line_num, column))
                elif part.startswith('0x') or part.isdigit():
                    tokens.append(ASMToken("number", part, line_num, column))
                elif part.startswith('[') and part.endswith(']'):
                    tokens.append(ASMToken("memory", part, line_num, column))
                elif part.startswith('"') and part.endswith('"'):
                    tokens.append(ASMToken("string", part, line_num, column))
                else:
                    tokens.append(ASMToken("operand", part, line_num, column))
                column += len(part) + 1
        
        return tokens

# ============================================================================
# ASM EDITOR
# ============================================================================

class ASMEditor:
    """Assembly language IDE"""
    
    def __init__(self, arch: ASMArchitecture = ASMArchitecture.X86_64):
        self.arch = arch
        self.filename = ""
        self.code = ""
        self.tokens: List[ASMToken] = []
        self.lexer = ASMLexer(arch)
        self.breakpoints: List[int] = []
        self.errors: List[Tuple[int, str]] = []
        self.total_cycles = 0
        
    def open_file(self, filename: str, code: str = ""):
        """Open/create file"""
        self.filename = filename
        self.code = code
        print(f"📄 Opened: {filename}")
    
    def analyze_syntax(self) -> bool:
        """Analyze syntax"""
        self.errors.clear()
        self.tokens = self.lexer.tokenize(self.code)
        
        for token in self.tokens:
            if token.type == "instruction":
                instr = self.lexer.instr_db.get_instruction(token.value)
                if not instr:
                    self.errors.append((token.line + 1, f"Unknown instruction: {token.value}"))
            elif token.type == "register":
                if not self.lexer.reg_db.is_valid_register(token.value):
                    self.errors.append((token.line + 1, f"Unknown register: {token.value}"))
        
        return len(self.errors) == 0
    
    def calculate_cycles(self) -> int:
        """Calculate execution cycles"""
        self.total_cycles = 0
        for token in self.tokens:
            if token.type == "instruction":
                instr = self.lexer.instr_db.get_instruction(token.value)
                if instr:
                    self.total_cycles += instr.execution_cycles
        return self.total_cycles
    
    def set_breakpoint(self, line: int):
        """Set breakpoint"""
        if line not in self.breakpoints:
            self.breakpoints.append(line)
            print(f"🔴 Breakpoint set at line {line}")
    
    def remove_breakpoint(self, line: int):
        """Remove breakpoint"""
        if line in self.breakpoints:
            self.breakpoints.remove(line)
            print(f"⚪ Breakpoint removed from line {line}")
    
    def syntax_highlight(self) -> Dict[str, List[str]]:
        """Generate syntax highlighting"""
        highlighted = {
            "instructions": [],
            "registers": [],
            "numbers": [],
            "comments": [],
            "labels": [],
            "memory": [],
            "errors": []
        }
        
        for token in self.tokens:
            if token.type == "instruction":
                highlighted["instructions"].append(f"{token.value} (line {token.line + 1})")
            elif token.type == "register":
                highlighted["registers"].append(f"{token.value} (line {token.line + 1})")
            elif token.type == "number":
                highlighted["numbers"].append(f"{token.value} (line {token.line + 1})")
            elif token.type == "comment":
                highlighted["comments"].append(f"{token.value} (line {token.line + 1})")
            elif token.type == "label":
                highlighted["labels"].append(f"{token.value} (line {token.line + 1})")
            elif token.type == "memory":
                highlighted["memory"].append(f"{token.value} (line {token.line + 1})")
        
        for line, error in self.errors:
            highlighted["errors"].append(f"Line {line}: {error}")
        
        return highlighted

# ============================================================================
# DEMONSTRATION FUNCTION
# ============================================================================

def demonstrate_asm_ide():
    """Demonstrate ASM IDE"""
    print("\n" + "=" * 70)
    print("ASSEMBLY (ASM) IDE DEMONSTRATION")
    print("=" * 70)
    
    # Create editor
    editor = ASMEditor(ASMArchitecture.X86_64)
    
    # Sample assembly code
    sample_code = """
; Simple loop - add numbers 1 to 10
    MOV RAX, 0      ; Result in RAX
    MOV RCX, 10     ; Loop counter
    MOV RBX, 1      ; Current number
loop_start:
    ADD RAX, RBX    ; Add to result
    INC RBX         ; Increment counter
    CMP RBX, RCX    ; Compare with limit
    JLE loop_start  ; Jump if less or equal
    SYSCALL         ; Exit
"""
    
    editor.open_file("loop.asm", sample_code)
    
    print("\n📋 Code:")
    for i, line in enumerate(sample_code.strip().split('\n'), 1):
        marker = "🔴" if i in [6] else " "
        print(f"  {marker} {i:2d}: {line}")
    
    # Set breakpoint
    editor.set_breakpoint(6)
    
    # Analyze syntax
    print("\n📝 Syntax Analysis:")
    if editor.analyze_syntax():
        print("  ✅ Syntax OK - No errors found")
    else:
        print("  ❌ Errors found:")
        for line, error in editor.errors:
            print(f"    Line {line}: {error}")
    
    # Calculate cycles
    cycles = editor.calculate_cycles()
    print(f"\n⏱️  Execution cycles: {cycles}")
    
    # Syntax highlighting
    print("\n🎨 Syntax Highlighting:")
    highlighted = editor.syntax_highlight()
    for category, items in highlighted.items():
        if items:
            print(f"  {category.upper()}:")
            for item in items[:3]:  # Show first 3
                print(f"    • {item}")
            if len(items) > 3:
                print(f"    ... and {len(items) - 3} more")
    
    # Test instruction database
    print("\n📚 Instruction Database:")
    test_instrs = ["MOV", "ADD", "JMP", "RET", "NOP", "SYSCALL"]
    for instr in test_instrs:
        info = editor.lexer.instr_db.get_instruction(instr)
        if info:
            print(f"  {instr:8} - {info.description:30} ({info.execution_cycles} cycles)")
    
    print("\n✅ ASM IDE demonstration complete!")

if __name__ == "__main__":
    demonstrate_asm_ide()
