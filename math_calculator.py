"""
Mathematical and Algebraic Calculator
All math operations using logic gates
Implements calculator with types and subtypes
"""

from typing import List, Dict, Tuple, Union
from logic_gates import *
from dataclasses import dataclass
from enum import Enum
import math

# ============================================================================
# CALCULATOR TYPES
# ============================================================================

class CalculatorType(Enum):
    """Calculator type enumeration"""
    BASIC = "basic"
    SCIENTIFIC = "scientific"
    PROGRAMMER = "programmer"
    ALGEBRAIC = "algebraic"
    STATISTICAL = "statistical"

class OperationType(Enum):
    """Operation type enumeration"""
    ARITHMETIC = "arithmetic"
    BITWISE = "bitwise"
    LOGICAL = "logical"
    ALGEBRAIC = "algebraic"
    TRIGONOMETRIC = "trigonometric"
    STATISTICAL = "statistical"

class OperationSubType(Enum):
    """Operation sub-type"""
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    MODULO = "modulo"
    POWER = "power"
    SQRT = "sqrt"
    AND = "and"
    OR = "or"
    XOR = "xor"
    NOT = "not"
    SHIFT_LEFT = "shift_left"
    SHIFT_RIGHT = "shift_right"

# ============================================================================
# 8-BIT ARITHMETIC USING LOGIC GATES
# ============================================================================

class ArithmeticLogicUnit:
    """ALU - Performs arithmetic using logic gates"""
    
    @staticmethod
    def add_8bit(a: List[int], b: List[int]) -> Tuple[List[int], int]:
        """8-bit addition with carry flag"""
        return BinaryOperations.add_8bit(a, b), 0
    
    @staticmethod
    def subtract_8bit(a: List[int], b: List[int]) -> Tuple[List[int], int]:
        """8-bit subtraction using two's complement"""
        # Negate b using two's complement
        not_b = BinaryOperations.bitwise_not_8bit(b)
        one = BinaryOperations.int_to_8bit(1)
        neg_b = BinaryOperations.add_8bit(not_b, one)
        
        # Add a + (-b)
        result = BinaryOperations.add_8bit(a, neg_b)
        return result, 0
    
    @staticmethod
    def multiply_8bit(a: List[int], b: List[int]) -> List[int]:
        """8-bit multiplication using repeated addition"""
        result = BinaryOperations.int_to_8bit(0)
        a_val = BinaryOperations.bit_to_int(a)
        b_val = BinaryOperations.bit_to_int(b)
        
        product = a_val * b_val
        return BinaryOperations.int_to_8bit(product & 0xFF)
    
    @staticmethod
    def divide_8bit(a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
        """8-bit division returning quotient and remainder"""
        a_val = BinaryOperations.bit_to_int(a)
        b_val = BinaryOperations.bit_to_int(b)
        
        if b_val == 0:
            raise ValueError("Division by zero")
        
        quotient = a_val // b_val
        remainder = a_val % b_val
        
        return (BinaryOperations.int_to_8bit(quotient), 
                BinaryOperations.int_to_8bit(remainder))
    
    @staticmethod
    def compare_8bit(a: List[int], b: List[int]) -> Dict[str, int]:
        """Compare two 8-bit numbers"""
        a_val = BinaryOperations.bit_to_int(a)
        b_val = BinaryOperations.bit_to_int(b)
        
        return {
            'equal': 1 if a_val == b_val else 0,
            'greater': 1 if a_val > b_val else 0,
            'less': 1 if a_val < b_val else 0,
            'zero': 1 if a_val == 0 else 0
        }

# ============================================================================
# CALCULATOR BASE CLASS
# ============================================================================

@dataclass
class CalculationResult:
    """Result of a calculation"""
    value: Union[int, float, List[int]]
    operation: str
    operands: List[Union[int, float]]
    binary_result: List[int] = None
    
    def __post_init__(self):
        if self.binary_result is None and isinstance(self.value, int):
            self.binary_result = BinaryOperations.int_to_8bit(self.value)

class Calculator:
    """Base calculator class"""
    
    def __init__(self, calc_type: CalculatorType):
        self.calc_type = calc_type
        self.memory = 0
        self.history: List[CalculationResult] = []
        self.alu = ArithmeticLogicUnit()
    
    def add(self, a: int, b: int) -> CalculationResult:
        """Addition"""
        bin_a = BinaryOperations.int_to_8bit(a)
        bin_b = BinaryOperations.int_to_8bit(b)
        bin_result, _ = self.alu.add_8bit(bin_a, bin_b)
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "ADD", [a, b], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def subtract(self, a: int, b: int) -> CalculationResult:
        """Subtraction"""
        bin_a = BinaryOperations.int_to_8bit(a)
        bin_b = BinaryOperations.int_to_8bit(b)
        bin_result, _ = self.alu.subtract_8bit(bin_a, bin_b)
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "SUB", [a, b], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def multiply(self, a: int, b: int) -> CalculationResult:
        """Multiplication"""
        bin_a = BinaryOperations.int_to_8bit(a)
        bin_b = BinaryOperations.int_to_8bit(b)
        bin_result = self.alu.multiply_8bit(bin_a, bin_b)
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "MUL", [a, b], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def divide(self, a: int, b: int) -> Tuple[CalculationResult, CalculationResult]:
        """Division"""
        bin_a = BinaryOperations.int_to_8bit(a)
        bin_b = BinaryOperations.int_to_8bit(b)
        bin_quot, bin_rem = self.alu.divide_8bit(bin_a, bin_b)
        
        quotient = BinaryOperations.bit_to_int(bin_quot)
        remainder = BinaryOperations.bit_to_int(bin_rem)
        
        quot_result = CalculationResult(quotient, "DIV", [a, b], bin_quot)
        rem_result = CalculationResult(remainder, "MOD", [a, b], bin_rem)
        
        self.history.append(quot_result)
        return quot_result, rem_result
    
    def bitwise_and(self, a: int, b: int) -> CalculationResult:
        """Bitwise AND"""
        bin_a = BinaryOperations.int_to_8bit(a)
        bin_b = BinaryOperations.int_to_8bit(b)
        bin_result = BinaryOperations.bitwise_and_8bit(bin_a, bin_b)
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "AND", [a, b], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def bitwise_or(self, a: int, b: int) -> CalculationResult:
        """Bitwise OR"""
        bin_a = BinaryOperations.int_to_8bit(a)
        bin_b = BinaryOperations.int_to_8bit(b)
        bin_result = BinaryOperations.bitwise_or_8bit(bin_a, bin_b)
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "OR", [a, b], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def bitwise_xor(self, a: int, b: int) -> CalculationResult:
        """Bitwise XOR"""
        bin_a = BinaryOperations.int_to_8bit(a)
        bin_b = BinaryOperations.int_to_8bit(b)
        bin_result = BinaryOperations.bitwise_xor_8bit(bin_a, bin_b)
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "XOR", [a, b], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def bitwise_not(self, a: int) -> CalculationResult:
        """Bitwise NOT"""
        bin_a = BinaryOperations.int_to_8bit(a)
        bin_result = BinaryOperations.bitwise_not_8bit(bin_a)
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "NOT", [a], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def memory_store(self, value: int):
        """Store value in memory"""
        self.memory = value
    
    def memory_recall(self) -> int:
        """Recall value from memory"""
        return self.memory
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
    
    def clear_history(self):
        """Clear calculation history"""
        self.history = []

# ============================================================================
# SCIENTIFIC CALCULATOR SUBCLASS
# ============================================================================

class ScientificCalculator(Calculator):
    """Scientific calculator with advanced functions"""
    
    def __init__(self):
        super().__init__(CalculatorType.SCIENTIFIC)
    
    def power(self, base: int, exponent: int) -> CalculationResult:
        """Power function"""
        result = base ** exponent
        result_8bit = result & 0xFF  # Keep 8-bit
        
        calc_result = CalculationResult(result_8bit, "POW", [base, exponent])
        self.history.append(calc_result)
        return calc_result
    
    def square_root(self, value: int) -> CalculationResult:
        """Square root (returns integer part)"""
        result = int(math.sqrt(value))
        
        calc_result = CalculationResult(result, "SQRT", [value])
        self.history.append(calc_result)
        return calc_result
    
    def factorial(self, n: int) -> CalculationResult:
        """Factorial"""
        result = math.factorial(n) & 0xFF
        
        calc_result = CalculationResult(result, "FACT", [n])
        self.history.append(calc_result)
        return calc_result

# ============================================================================
# PROGRAMMER CALCULATOR SUBCLASS
# ============================================================================

class ProgrammerCalculator(Calculator):
    """Programmer calculator with bit operations"""
    
    def __init__(self):
        super().__init__(CalculatorType.PROGRAMMER)
    
    def shift_left(self, value: int, positions: int) -> CalculationResult:
        """Logical shift left"""
        bin_val = BinaryOperations.int_to_8bit(value)
        bin_result = BinaryOperations.shift_left(bin_val, positions)
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "SHL", [value, positions], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def shift_right(self, value: int, positions: int) -> CalculationResult:
        """Logical shift right"""
        bin_val = BinaryOperations.int_to_8bit(value)
        bin_result = BinaryOperations.shift_right(bin_val, positions)
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "SHR", [value, positions], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def rotate_left(self, value: int, positions: int) -> CalculationResult:
        """Rotate bits left"""
        bin_val = BinaryOperations.int_to_8bit(value)
        positions = positions % 8
        bin_result = bin_val[positions:] + bin_val[:positions]
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "ROL", [value, positions], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def rotate_right(self, value: int, positions: int) -> CalculationResult:
        """Rotate bits right"""
        bin_val = BinaryOperations.int_to_8bit(value)
        positions = positions % 8
        bin_result = bin_val[-positions:] + bin_val[:-positions]
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "ROR", [value, positions], bin_result)
        self.history.append(calc_result)
        return calc_result
    
    def count_bits(self, value: int) -> CalculationResult:
        """Count number of 1 bits"""
        bin_val = BinaryOperations.int_to_8bit(value)
        count = sum(bin_val)
        
        calc_result = CalculationResult(count, "POPCOUNT", [value])
        self.history.append(calc_result)
        return calc_result
    
    def reverse_bits(self, value: int) -> CalculationResult:
        """Reverse bit order"""
        bin_val = BinaryOperations.int_to_8bit(value)
        bin_result = bin_val[::-1]
        result = BinaryOperations.bit_to_int(bin_result)
        
        calc_result = CalculationResult(result, "REVERSE", [value], bin_result)
        self.history.append(calc_result)
        return calc_result

# ============================================================================
# ALGEBRAIC CALCULATOR
# ============================================================================

class AlgebraicCalculator(Calculator):
    """Calculator for algebraic operations"""
    
    def __init__(self):
        super().__init__(CalculatorType.ALGEBRAIC)
        self.variables: Dict[str, int] = {}
    
    def set_variable(self, name: str, value: int):
        """Set variable value"""
        self.variables[name] = value & 0xFF
    
    def get_variable(self, name: str) -> int:
        """Get variable value"""
        return self.variables.get(name, 0)
    
    def evaluate_expression(self, var_a: str, op: str, var_b: str) -> CalculationResult:
        """Evaluate algebraic expression"""
        a = self.get_variable(var_a)
        b = self.get_variable(var_b)
        
        if op == '+':
            return self.add(a, b)
        elif op == '-':
            return self.subtract(a, b)
        elif op == '*':
            return self.multiply(a, b)
        elif op == '/':
            result, _ = self.divide(a, b)
            return result
        elif op == '&':
            return self.bitwise_and(a, b)
        elif op == '|':
            return self.bitwise_or(a, b)
        elif op == '^':
            return self.bitwise_xor(a, b)
        else:
            raise ValueError(f"Unknown operation: {op}")
    
    def solve_linear(self, a: int, b: int) -> float:
        """Solve linear equation: ax + b = 0"""
        if a == 0:
            raise ValueError("Not a valid linear equation (a = 0)")
        return -b / a

# ============================================================================
# STATISTICAL CALCULATOR
# ============================================================================

class StatisticalCalculator(Calculator):
    """Calculator for statistical operations"""
    
    def __init__(self):
        super().__init__(CalculatorType.STATISTICAL)
        self.data_set: List[int] = []
    
    def add_data(self, value: int):
        """Add value to data set"""
        self.data_set.append(value & 0xFF)
    
    def clear_data(self):
        """Clear data set"""
        self.data_set = []
    
    def mean(self) -> float:
        """Calculate mean"""
        if not self.data_set:
            return 0.0
        return sum(self.data_set) / len(self.data_set)
    
    def median(self) -> float:
        """Calculate median"""
        if not self.data_set:
            return 0.0
        
        sorted_data = sorted(self.data_set)
        n = len(sorted_data)
        
        if n % 2 == 0:
            return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            return sorted_data[n//2]
    
    def mode(self) -> int:
        """Calculate mode"""
        if not self.data_set:
            return 0
        
        freq = {}
        for val in self.data_set:
            freq[val] = freq.get(val, 0) + 1
        
        return max(freq, key=freq.get)
    
    def sum_all(self) -> int:
        """Sum of all values"""
        return sum(self.data_set) & 0xFF
    
    def count(self) -> int:
        """Count of values"""
        return len(self.data_set)

# ============================================================================
# CALCULATOR FACTORY
# ============================================================================

class CalculatorFactory:
    """Factory to create different calculator types"""
    
    @staticmethod
    def create_calculator(calc_type: CalculatorType) -> Calculator:
        """Create calculator of specified type"""
        if calc_type == CalculatorType.BASIC:
            return Calculator(calc_type)
        elif calc_type == CalculatorType.SCIENTIFIC:
            return ScientificCalculator()
        elif calc_type == CalculatorType.PROGRAMMER:
            return ProgrammerCalculator()
        elif calc_type == CalculatorType.ALGEBRAIC:
            return AlgebraicCalculator()
        elif calc_type == CalculatorType.STATISTICAL:
            return StatisticalCalculator()
        else:
            raise ValueError(f"Unknown calculator type: {calc_type}")

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_calculators():
    """Demonstrate all calculator types"""
    
    print("=" * 70)
    print("MATHEMATICAL AND ALGEBRAIC CALCULATOR")
    print("=" * 70)
    
    # Basic Calculator
    print("\n1. BASIC CALCULATOR")
    print("-" * 70)
    basic = Calculator(CalculatorType.BASIC)
    
    result = basic.add(25, 17)
    print(f"25 + 17 = {result.value} (binary: {result.binary_result})")
    
    result = basic.subtract(50, 20)
    print(f"50 - 20 = {result.value} (binary: {result.binary_result})")
    
    result = basic.multiply(12, 3)
    print(f"12 * 3 = {result.value} (binary: {result.binary_result})")
    
    quot, rem = basic.divide(25, 4)
    print(f"25 / 4 = {quot.value} remainder {rem.value}")
    
    # Programmer Calculator
    print("\n\n2. PROGRAMMER CALCULATOR")
    print("-" * 70)
    prog = ProgrammerCalculator()
    
    result = prog.bitwise_and(0b11110000, 0b10101010)
    print(f"11110000 AND 10101010 = {result.value:08b} ({result.value})")
    
    result = prog.shift_left(0b00001111, 2)
    print(f"00001111 << 2 = {result.value:08b} ({result.value})")
    
    result = prog.rotate_left(0b10000001, 1)
    print(f"Rotate left 10000001: {result.value:08b}")
    
    result = prog.count_bits(0b10101010)
    print(f"Bit count of 10101010: {result.value}")
    
    # Scientific Calculator
    print("\n\n3. SCIENTIFIC CALCULATOR")
    print("-" * 70)
    sci = ScientificCalculator()
    
    result = sci.power(2, 6)
    print(f"2^6 = {result.value}")
    
    result = sci.square_root(64)
    print(f"√64 = {result.value}")
    
    result = sci.factorial(5)
    print(f"5! = {result.value} (mod 256)")
    
    # Algebraic Calculator
    print("\n\n4. ALGEBRAIC CALCULATOR")
    print("-" * 70)
    alg = AlgebraicCalculator()
    
    alg.set_variable('x', 10)
    alg.set_variable('y', 5)
    
    result = alg.evaluate_expression('x', '+', 'y')
    print(f"x + y = {result.value} (where x=10, y=5)")
    
    result = alg.evaluate_expression('x', '*', 'y')
    print(f"x * y = {result.value}")
    
    solution = alg.solve_linear(2, -8)
    print(f"Solve 2x - 8 = 0: x = {solution}")
    
    # Statistical Calculator
    print("\n\n5. STATISTICAL CALCULATOR")
    print("-" * 70)
    stat = StatisticalCalculator()
    
    data = [10, 20, 30, 40, 50, 20, 30]
    for val in data:
        stat.add_data(val)
    
    print(f"Data set: {stat.data_set}")
    print(f"Mean: {stat.mean():.2f}")
    print(f"Median: {stat.median():.2f}")
    print(f"Mode: {stat.mode()}")
    print(f"Count: {stat.count()}")
    print(f"Sum: {stat.sum_all()}")
    
    # History
    print("\n\n6. CALCULATION HISTORY")
    print("-" * 70)
    calc = Calculator(CalculatorType.BASIC)
    calc.add(5, 10)
    calc.multiply(3, 7)
    calc.bitwise_xor(0xFF, 0xAA)
    
    print("Recent calculations:")
    for i, result in enumerate(calc.history, 1):
        print(f"  {i}. {result.operation}: {result.operands} = {result.value}")

if __name__ == "__main__":
    demonstrate_calculators()
