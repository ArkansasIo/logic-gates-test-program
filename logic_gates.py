"""
Logic Gates Module - All Basic Logic Gate Functions
Implements logic gates using 0 and 1 (binary)
"""

from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum

# ============================================================================
# BASIC LOGIC GATE FUNCTIONS
# ============================================================================

def AND(a: int, b: int) -> int:
    """AND Gate: Returns 1 only if both inputs are 1"""
    return 1 if (a == 1 and b == 1) else 0

def OR(a: int, b: int) -> int:
    """OR Gate: Returns 1 if at least one input is 1"""
    return 1 if (a == 1 or b == 1) else 0

def NOT(a: int) -> int:
    """NOT Gate: Inverts the input"""
    return 1 if a == 0 else 0

def NAND(a: int, b: int) -> int:
    """NAND Gate: NOT-AND, returns 0 only if both inputs are 1"""
    return NOT(AND(a, b))

def NOR(a: int, b: int) -> int:
    """NOR Gate: NOT-OR, returns 1 only if both inputs are 0"""
    return NOT(OR(a, b))

def XOR(a: int, b: int) -> int:
    """XOR Gate: Returns 1 if inputs are different"""
    return 1 if a != b else 0

def XNOR(a: int, b: int) -> int:
    """XNOR Gate: Returns 1 if inputs are the same"""
    return NOT(XOR(a, b))

def BUFFER(a: int) -> int:
    """BUFFER Gate: Passes input unchanged"""
    return a

# ============================================================================
# LOGIC GATE ENUM
# ============================================================================

class GateType(Enum):
    """Enumeration of all logic gate types"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    NAND = "NAND"
    NOR = "NOR"
    XOR = "XOR"
    XNOR = "XNOR"
    BUFFER = "BUFFER"

# ============================================================================
# LOGIC GATE CLASS
# ============================================================================

class LogicGate:
    """Class representation of a logic gate"""
    
    def __init__(self, gate_type: GateType):
        self.gate_type = gate_type
        self.operations_count = 0
    
    def execute(self, a: int, b: int = None) -> int:
        """Execute the gate operation"""
        self.operations_count += 1
        
        if self.gate_type == GateType.AND:
            return AND(a, b)
        elif self.gate_type == GateType.OR:
            return OR(a, b)
        elif self.gate_type == GateType.NOT:
            return NOT(a)
        elif self.gate_type == GateType.NAND:
            return NAND(a, b)
        elif self.gate_type == GateType.NOR:
            return NOR(a, b)
        elif self.gate_type == GateType.XOR:
            return XOR(a, b)
        elif self.gate_type == GateType.XNOR:
            return XNOR(a, b)
        elif self.gate_type == GateType.BUFFER:
            return BUFFER(a)
        else:
            raise ValueError(f"Unknown gate type: {self.gate_type}")
    
    def get_truth_table(self) -> List[Tuple]:
        """Generate truth table for the gate"""
        if self.gate_type in [GateType.NOT, GateType.BUFFER]:
            return [(a, self.execute(a)) for a in [0, 1]]
        else:
            return [(a, b, self.execute(a, b)) for a in [0, 1] for b in [0, 1]]
    
    def __str__(self):
        return f"LogicGate({self.gate_type.value})"

# ============================================================================
# LOGIC GATE STRUCTURE (Dataclass)
# ============================================================================

@dataclass
class GateStructure:
    """Structure representation of a logic gate using dataclass"""
    gate_name: str
    input_a: int
    input_b: int
    output: int
    
    def __str__(self):
        return f"{self.gate_name}: {self.input_a} & {self.input_b} -> {self.output}"

# ============================================================================
# COMPOUND LOGIC GATES (Built from Basic Gates)
# ============================================================================

class CompoundGates:
    """Complex gates built from basic logic gates"""
    
    @staticmethod
    def HALF_ADDER(a: int, b: int) -> Tuple[int, int]:
        """Half Adder: Returns (sum, carry)"""
        sum_bit = XOR(a, b)
        carry = AND(a, b)
        return (sum_bit, carry)
    
    @staticmethod
    def FULL_ADDER(a: int, b: int, carry_in: int) -> Tuple[int, int]:
        """Full Adder: Returns (sum, carry_out)"""
        sum1, carry1 = CompoundGates.HALF_ADDER(a, b)
        sum_bit, carry2 = CompoundGates.HALF_ADDER(sum1, carry_in)
        carry_out = OR(carry1, carry2)
        return (sum_bit, carry_out)
    
    @staticmethod
    def MULTIPLEXER_2to1(a: int, b: int, select: int) -> int:
        """2-to-1 Multiplexer: Select between two inputs"""
        # If select = 0, output a; if select = 1, output b
        not_select = NOT(select)
        output_a = AND(a, not_select)
        output_b = AND(b, select)
        return OR(output_a, output_b)
    
    @staticmethod
    def DEMULTIPLEXER_1to2(input_val: int, select: int) -> Tuple[int, int]:
        """1-to-2 Demultiplexer: Route input to one of two outputs"""
        not_select = NOT(select)
        output_a = AND(input_val, not_select)
        output_b = AND(input_val, select)
        return (output_a, output_b)
    
    @staticmethod
    def DECODER_2to4(a: int, b: int) -> Tuple[int, int, int, int]:
        """2-to-4 Decoder"""
        not_a = NOT(a)
        not_b = NOT(b)
        
        out0 = AND(not_a, not_b)
        out1 = AND(not_a, b)
        out2 = AND(a, not_b)
        out3 = AND(a, b)
        
        return (out0, out1, out2, out3)
    
    @staticmethod
    def ENCODER_4to2(i0: int, i1: int, i2: int, i3: int) -> Tuple[int, int]:
        """4-to-2 Priority Encoder"""
        a = OR(i2, i3)
        b = OR(i1, i3)
        return (a, b)

# ============================================================================
# BINARY OPERATIONS MODULE
# ============================================================================

class BinaryOperations:
    """Operations on binary numbers (8-bit)"""
    
    @staticmethod
    def add_8bit(a: List[int], b: List[int]) -> List[int]:
        """Add two 8-bit binary numbers"""
        result = [0] * 8
        carry = 0
        
        for i in range(7, -1, -1):
            sum_bit, carry = CompoundGates.FULL_ADDER(a[i], b[i], carry)
            result[i] = sum_bit
        
        return result
    
    @staticmethod
    def bitwise_and_8bit(a: List[int], b: List[int]) -> List[int]:
        """Bitwise AND of two 8-bit numbers"""
        return [AND(a[i], b[i]) for i in range(8)]
    
    @staticmethod
    def bitwise_or_8bit(a: List[int], b: List[int]) -> List[int]:
        """Bitwise OR of two 8-bit numbers"""
        return [OR(a[i], b[i]) for i in range(8)]
    
    @staticmethod
    def bitwise_xor_8bit(a: List[int], b: List[int]) -> List[int]:
        """Bitwise XOR of two 8-bit numbers"""
        return [XOR(a[i], b[i]) for i in range(8)]
    
    @staticmethod
    def bitwise_not_8bit(a: List[int]) -> List[int]:
        """Bitwise NOT of an 8-bit number"""
        return [NOT(bit) for bit in a]
    
    @staticmethod
    def int_to_8bit(value: int) -> List[int]:
        """Convert integer to 8-bit binary list"""
        return [int(bit) for bit in format(value & 0xFF, '08b')]
    
    @staticmethod
    def bit_to_int(bits: List[int]) -> int:
        """Convert 8-bit binary list to integer"""
        return int(''.join(map(str, bits)), 2)
    
    @staticmethod
    def shift_left(bits: List[int], positions: int = 1) -> List[int]:
        """Logical shift left"""
        result = bits[positions:] + [0] * positions
        return result[:8]
    
    @staticmethod
    def shift_right(bits: List[int], positions: int = 1) -> List[int]:
        """Logical shift right"""
        result = [0] * positions + bits[:-positions]
        return result[:8]

# ============================================================================
# TESTING AND DEMONSTRATION
# ============================================================================

def print_truth_tables():
    """Print truth tables for all basic logic gates"""
    gates = [GateType.AND, GateType.OR, GateType.NAND, GateType.NOR, 
             GateType.XOR, GateType.XNOR]
    
    print("=" * 60)
    print("TRUTH TABLES FOR ALL LOGIC GATES")
    print("=" * 60)
    
    # Two-input gates
    for gate_type in gates:
        gate = LogicGate(gate_type)
        print(f"\n{gate_type.value} Gate:")
        print("A | B | Output")
        print("-" * 15)
        for a, b, output in gate.get_truth_table():
            print(f"{a} | {b} |   {output}")
    
    # Single-input gates
    for gate_type in [GateType.NOT, GateType.BUFFER]:
        gate = LogicGate(gate_type)
        print(f"\n{gate_type.value} Gate:")
        print("A | Output")
        print("-" * 10)
        for a, output in gate.get_truth_table():
            print(f"{a} |   {output}")

if __name__ == "__main__":
    print_truth_tables()
    
    print("\n" + "=" * 60)
    print("COMPOUND GATES DEMONSTRATION")
    print("=" * 60)
    
    # Half Adder
    print("\nHalf Adder (1 + 1):")
    sum_bit, carry = CompoundGates.HALF_ADDER(1, 1)
    print(f"Sum: {sum_bit}, Carry: {carry}")
    
    # Full Adder
    print("\nFull Adder (1 + 1 + 1):")
    sum_bit, carry = CompoundGates.FULL_ADDER(1, 1, 1)
    print(f"Sum: {sum_bit}, Carry: {carry}")
    
    # 8-bit Addition
    print("\n8-bit Addition (5 + 3):")
    a = BinaryOperations.int_to_8bit(5)
    b = BinaryOperations.int_to_8bit(3)
    result = BinaryOperations.add_8bit(a, b)
    print(f"5:  {a}")
    print(f"3:  {b}")
    print(f"8:  {result}")
    print(f"Result: {BinaryOperations.bit_to_int(result)}")
