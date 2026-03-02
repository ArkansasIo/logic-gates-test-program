"""
Character and Number Logic Gate Operations
Maps A-Z, a-z, and 0-9 to logic gate operations
Includes arrays, subarrays, types, and subtypes
"""

from typing import List, Dict, Tuple, Any
from logic_gates import *
from dataclasses import dataclass, field
from enum import Enum
import string

# ============================================================================
# CHARACTER TO BINARY MAPPING (ASCII-based)
# ============================================================================

class CharacterBinaryMapper:
    """Maps characters to 8-bit binary representations"""
    
    @staticmethod
    def char_to_binary(char: str) -> List[int]:
        """Convert character to 8-bit binary array"""
        if len(char) != 1:
            raise ValueError("Input must be a single character")
        
        ascii_val = ord(char)
        return BinaryOperations.int_to_8bit(ascii_val)
    
    @staticmethod
    def binary_to_char(binary: List[int]) -> str:
        """Convert 8-bit binary array to character"""
        ascii_val = BinaryOperations.bit_to_int(binary)
        return chr(ascii_val)
    
    @staticmethod
    def string_to_binary_array(text: str) -> List[List[int]]:
        """Convert string to array of binary arrays"""
        return [CharacterBinaryMapper.char_to_binary(char) for char in text]
    
    @staticmethod
    def binary_array_to_string(binary_array: List[List[int]]) -> str:
        """Convert array of binary arrays to string"""
        return ''.join([CharacterBinaryMapper.binary_to_char(b) for b in binary_array])

# ============================================================================
# CHARACTER LOGIC GATE OPERATIONS
# ============================================================================

class CharacterLogicOperations:
    """Logic gate operations on characters"""
    
    @staticmethod
    def char_AND(char1: str, char2: str) -> str:
        """Bitwise AND on two characters"""
        bin1 = CharacterBinaryMapper.char_to_binary(char1)
        bin2 = CharacterBinaryMapper.char_to_binary(char2)
        result = BinaryOperations.bitwise_and_8bit(bin1, bin2)
        return CharacterBinaryMapper.binary_to_char(result)
    
    @staticmethod
    def char_OR(char1: str, char2: str) -> str:
        """Bitwise OR on two characters"""
        bin1 = CharacterBinaryMapper.char_to_binary(char1)
        bin2 = CharacterBinaryMapper.char_to_binary(char2)
        result = BinaryOperations.bitwise_or_8bit(bin1, bin2)
        return CharacterBinaryMapper.binary_to_char(result)
    
    @staticmethod
    def char_XOR(char1: str, char2: str) -> str:
        """Bitwise XOR on two characters"""
        bin1 = CharacterBinaryMapper.char_to_binary(char1)
        bin2 = CharacterBinaryMapper.char_to_binary(char2)
        result = BinaryOperations.bitwise_xor_8bit(bin1, bin2)
        return CharacterBinaryMapper.binary_to_char(result)
    
    @staticmethod
    def char_NOT(char: str) -> str:
        """Bitwise NOT on character"""
        binary = CharacterBinaryMapper.char_to_binary(char)
        result = BinaryOperations.bitwise_not_8bit(binary)
        return CharacterBinaryMapper.binary_to_char(result)

# ============================================================================
# ARRAYS AND SUBARRAYS
# ============================================================================

@dataclass
class LogicGateArray:
    """Array structure for logic gate operations"""
    name: str
    data: List[int]
    gate_type: GateType
    
    def apply_gate(self, other: 'LogicGateArray') -> 'LogicGateArray':
        """Apply gate operation between two arrays"""
        if len(self.data) != len(other.data):
            raise ValueError("Arrays must be same length")
        
        gate = LogicGate(self.gate_type)
        result = []
        for i in range(len(self.data)):
            result.append(gate.execute(self.data[i], other.data[i]))
        
        return LogicGateArray(
            name=f"{self.name}_{self.gate_type.value}_{other.name}",
            data=result,
            gate_type=self.gate_type
        )
    
    def apply_unary_gate(self, gate_type: GateType) -> 'LogicGateArray':
        """Apply unary gate to array"""
        gate = LogicGate(gate_type)
        result = [gate.execute(bit) for bit in self.data]
        return LogicGateArray(
            name=f"{gate_type.value}_{self.name}",
            data=result,
            gate_type=gate_type
        )

@dataclass
class LogicGateSubArray:
    """Subarray with hierarchical structure"""
    parent: str
    index: int
    data: List[int]
    metadata: Dict[str, Any] = field(default_factory=dict)

class ArrayHierarchy:
    """Manages arrays and subarrays hierarchically"""
    
    def __init__(self):
        self.arrays: Dict[str, LogicGateArray] = {}
        self.subarrays: Dict[str, List[LogicGateSubArray]] = {}
    
    def create_array(self, name: str, data: List[int], gate_type: GateType):
        """Create main array"""
        self.arrays[name] = LogicGateArray(name, data, gate_type)
    
    def create_subarray(self, parent: str, index: int, data: List[int]):
        """Create subarray from parent"""
        if parent not in self.subarrays:
            self.subarrays[parent] = []
        
        subarray = LogicGateSubArray(parent, index, data)
        self.subarrays[parent].append(subarray)
    
    def split_into_subarrays(self, array_name: str, chunk_size: int):
        """Split array into subarrays"""
        if array_name not in self.arrays:
            raise ValueError(f"Array {array_name} not found")
        
        array = self.arrays[array_name]
        for i in range(0, len(array.data), chunk_size):
            chunk = array.data[i:i+chunk_size]
            self.create_subarray(array_name, i // chunk_size, chunk)

# ============================================================================
# CHARACTER SET MAPPINGS
# ============================================================================

class CharacterSet:
    """Complete character set with logic gate operations"""
    
    UPPERCASE = list(string.ascii_uppercase)  # A-Z
    LOWERCASE = list(string.ascii_lowercase)  # a-z
    DIGITS = list(string.digits)              # 0-9
    ALL_CHARS = UPPERCASE + LOWERCASE + DIGITS
    
    @staticmethod
    def get_char_table(gate_type: str) -> Dict[Tuple[str, str], str]:
        """Generate truth table for characters and gate"""
        table = {}
        
        # Sample with digits for demonstration
        for char1 in CharacterSet.DIGITS:
            for char2 in CharacterSet.DIGITS:
                if gate_type == 'AND':
                    result = CharacterLogicOperations.char_AND(char1, char2)
                elif gate_type == 'OR':
                    result = CharacterLogicOperations.char_OR(char1, char2)
                elif gate_type == 'XOR':
                    result = CharacterLogicOperations.char_XOR(char1, char2)
                else:
                    continue
                
                table[(char1, char2)] = result
        
        return table
    
    @staticmethod
    def print_digit_gate_table(gate_type: str):
        """Print truth table for digits"""
        print(f"\n{gate_type} Gate - Digit Operations (ASCII)")
        print("=" * 60)
        
        digits = '0123456789'
        print("\n    ", end="")
        for d in digits:
            print(f" {d} ", end="")
        print("\n" + "-" * 60)
        
        for d1 in digits:
            print(f" {d1} |", end="")
            for d2 in digits:
                if gate_type == 'AND':
                    result = CharacterLogicOperations.char_AND(d1, d2)
                elif gate_type == 'OR':
                    result = CharacterLogicOperations.char_OR(d1, d2)
                elif gate_type == 'XOR':
                    result = CharacterLogicOperations.char_XOR(d1, d2)
                else:
                    result = '?'
                
                # Show ASCII code
                print(f"{ord(result):3d}", end="")
            print()

# ============================================================================
# TYPE AND SUBTYPE SYSTEM
# ============================================================================

class DataType(Enum):
    """Data type enumeration"""
    BIT = "bit"
    NIBBLE = "nibble"
    BYTE = "byte"
    WORD = "word"
    DWORD = "dword"
    CHAR = "char"
    STRING = "string"
    ARRAY = "array"

class DataSubType(Enum):
    """Data subtype enumeration"""
    UNSIGNED = "unsigned"
    SIGNED = "signed"
    FLOAT = "float"
    ASCII = "ascii"
    UNICODE = "unicode"
    BINARY = "binary"
    HEXADECIMAL = "hexadecimal"

@dataclass
class TypedData:
    """Data with type and subtype"""
    value: Any
    data_type: DataType
    data_subtype: DataSubType
    bit_width: int
    
    def to_binary(self) -> List[int]:
        """Convert to binary representation"""
        if isinstance(self.value, int):
            return BinaryOperations.int_to_8bit(self.value)
        elif isinstance(self.value, str):
            return CharacterBinaryMapper.char_to_binary(self.value)
        elif isinstance(self.value, list):
            return self.value
        return []

class TypeSystem:
    """Manages type hierarchy"""
    
    def __init__(self):
        self.types: Dict[str, TypedData] = {}
    
    def register_type(self, name: str, typed_data: TypedData):
        """Register a new typed data"""
        self.types[name] = typed_data
    
    def apply_gate_typed(self, name1: str, name2: str, gate_type: GateType) -> TypedData:
        """Apply gate operation on typed data"""
        data1 = self.types[name1]
        data2 = self.types[name2]
        
        bin1 = data1.to_binary()
        bin2 = data2.to_binary()
        
        gate = LogicGate(gate_type)
        
        if len(bin1) == len(bin2):
            result = [gate.execute(bin1[i], bin2[i]) for i in range(len(bin1))]
        else:
            raise ValueError("Binary representations must be same length")
        
        return TypedData(
            value=result,
            data_type=DataType.ARRAY,
            data_subtype=DataSubType.BINARY,
            bit_width=len(result)
        )

# ============================================================================
# CLASS AND SUBCLASS HIERARCHY
# ============================================================================

class LogicGateBase:
    """Base class for all logic gates"""
    
    def __init__(self, name: str):
        self.name = name
        self.input_count = 2
        self.output_count = 1
    
    def execute(self, *inputs):
        raise NotImplementedError("Subclass must implement execute()")
    
    def get_info(self) -> Dict:
        return {
            'name': self.name,
            'inputs': self.input_count,
            'outputs': self.output_count
        }

class ANDGateClass(LogicGateBase):
    """AND gate class"""
    def __init__(self):
        super().__init__("AND")
    
    def execute(self, a: int, b: int) -> int:
        return AND(a, b)

class ORGateClass(LogicGateBase):
    """OR gate class"""
    def __init__(self):
        super().__init__("OR")
    
    def execute(self, a: int, b: int) -> int:
        return OR(a, b)

class XORGateClass(LogicGateBase):
    """XOR gate class"""
    def __init__(self):
        super().__init__("XOR")
    
    def execute(self, a: int, b: int) -> int:
        return XOR(a, b)

class NOTGateClass(LogicGateBase):
    """NOT gate class"""
    def __init__(self):
        super().__init__("NOT")
        self.input_count = 1
    
    def execute(self, a: int) -> int:
        return NOT(a)

# Subclasses for specialized gates

class MultiBitANDGate(ANDGateClass):
    """Multi-bit AND gate subclass"""
    def __init__(self, bit_width: int = 8):
        super().__init__()
        self.bit_width = bit_width
        self.name = f"{bit_width}-bit AND"
    
    def execute_multi(self, a: List[int], b: List[int]) -> List[int]:
        return BinaryOperations.bitwise_and_8bit(a, b)

class MultiBitORGate(ORGateClass):
    """Multi-bit OR gate subclass"""
    def __init__(self, bit_width: int = 8):
        super().__init__()
        self.bit_width = bit_width
        self.name = f"{bit_width}-bit OR"
    
    def execute_multi(self, a: List[int], b: List[int]) -> List[int]:
        return BinaryOperations.bitwise_or_8bit(a, b)

# ============================================================================
# STRUCTURE AND SUB-STRUCTURE
# ============================================================================

@dataclass
class GateStructure:
    """Main gate structure"""
    gate_id: int
    gate_name: str
    inputs: List[int]
    outputs: List[int]
    gate_type: GateType
    
    def __post_init__(self):
        self.substructures: List[GateSubStructure] = []
    
    def add_substructure(self, sub: 'GateSubStructure'):
        """Add a sub-structure"""
        self.substructures.append(sub)

@dataclass
class GateSubStructure:
    """Sub-structure for gate components"""
    parent_id: int
    component_name: str
    component_type: str
    connections: List[Tuple[int, int]]
    properties: Dict[str, Any] = field(default_factory=dict)

class StructureHierarchy:
    """Manages structures and sub-structures"""
    
    def __init__(self):
        self.structures: Dict[int, GateStructure] = {}
        self.next_id = 1
    
    def create_structure(self, name: str, gate_type: GateType) -> int:
        """Create new structure"""
        gate_id = self.next_id
        self.next_id += 1
        
        structure = GateStructure(
            gate_id=gate_id,
            gate_name=name,
            inputs=[],
            outputs=[],
            gate_type=gate_type
        )
        
        self.structures[gate_id] = structure
        return gate_id
    
    def add_substructure(self, parent_id: int, component_name: str, 
                        component_type: str, connections: List[Tuple[int, int]]):
        """Add sub-structure to parent"""
        if parent_id not in self.structures:
            raise ValueError(f"Structure {parent_id} not found")
        
        sub = GateSubStructure(
            parent_id=parent_id,
            component_name=component_name,
            component_type=component_type,
            connections=connections
        )
        
        self.structures[parent_id].add_substructure(sub)

# ============================================================================
# MODULE AND SUB-MODULE SYSTEM
# ============================================================================

class LogicModule:
    """Base module class"""
    
    def __init__(self, name: str):
        self.name = name
        self.submodules: List['LogicSubModule'] = []
        self.gates: List[LogicGateBase] = []
    
    def add_submodule(self, submodule: 'LogicSubModule'):
        """Add sub-module"""
        self.submodules.append(submodule)
    
    def add_gate(self, gate: LogicGateBase):
        """Add gate to module"""
        self.gates.append(gate)
    
    def execute_module(self, inputs: List[int]) -> List[int]:
        """Execute all gates in module"""
        results = []
        for gate in self.gates:
            if gate.input_count == 2 and len(inputs) >= 2:
                results.append(gate.execute(inputs[0], inputs[1]))
            elif gate.input_count == 1 and len(inputs) >= 1:
                results.append(gate.execute(inputs[0]))
        return results

class LogicSubModule:
    """Sub-module class"""
    
    def __init__(self, name: str, parent: str):
        self.name = name
        self.parent = parent
        self.operations: List[Dict] = []
    
    def add_operation(self, operation: Dict):
        """Add operation to sub-module"""
        self.operations.append(operation)

class ModuleHierarchy:
    """Manages modules and sub-modules"""
    
    def __init__(self):
        self.modules: Dict[str, LogicModule] = {}
    
    def create_module(self, name: str) -> LogicModule:
        """Create new module"""
        module = LogicModule(name)
        self.modules[name] = module
        return module
    
    def create_submodule(self, parent_name: str, submodule_name: str) -> LogicSubModule:
        """Create sub-module"""
        if parent_name not in self.modules:
            raise ValueError(f"Module {parent_name} not found")
        
        submodule = LogicSubModule(submodule_name, parent_name)
        self.modules[parent_name].add_submodule(submodule)
        return submodule

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_all():
    """Demonstrate all features"""
    
    print("=" * 70)
    print("CHARACTER AND NUMBER LOGIC GATE OPERATIONS")
    print("=" * 70)
    
    # Character operations
    print("\n1. CHARACTER LOGIC OPERATIONS")
    print("-" * 70)
    char1, char2 = 'A', 'B'
    print(f"char1 = '{char1}' (ASCII {ord(char1):3d}, binary: {CharacterBinaryMapper.char_to_binary(char1)})")
    print(f"char2 = '{char2}' (ASCII {ord(char2):3d}, binary: {CharacterBinaryMapper.char_to_binary(char2)})")
    
    result_and = CharacterLogicOperations.char_AND(char1, char2)
    result_or = CharacterLogicOperations.char_OR(char1, char2)
    result_xor = CharacterLogicOperations.char_XOR(char1, char2)
    
    print(f"\nchar1 AND char2 = '{result_and}' (ASCII {ord(result_and):3d})")
    print(f"char1 OR  char2 = '{result_or}' (ASCII {ord(result_or):3d})")
    print(f"char1 XOR char2 = '{result_xor}' (ASCII {ord(result_xor):3d})")
    
    # Digit operations
    CharacterSet.print_digit_gate_table('XOR')
    
    # Arrays
    print("\n\n2. ARRAY OPERATIONS")
    print("-" * 70)
    array1 = LogicGateArray("Array1", [1, 0, 1, 1, 0, 1, 0, 1], GateType.AND)
    array2 = LogicGateArray("Array2", [1, 1, 0, 1, 1, 0, 1, 0], GateType.AND)
    
    result_array = array1.apply_gate(array2)
    print(f"Array1: {array1.data}")
    print(f"Array2: {array2.data}")
    print(f"Result: {result_array.data}")
    
    # Type system
    print("\n\n3. TYPE SYSTEM")
    print("-" * 70)
    type_sys = TypeSystem()
    
    data1 = TypedData(65, DataType.BYTE, DataSubType.UNSIGNED, 8)
    data2 = TypedData(66, DataType.BYTE, DataSubType.UNSIGNED, 8)
    
    type_sys.register_type("data1", data1)
    type_sys.register_type("data2", data2)
    
    result = type_sys.apply_gate_typed("data1", "data2", GateType.XOR)
    print(f"Data1 (type: {data1.data_type.value}, subtype: {data1.data_subtype.value}): {data1.value}")
    print(f"Data2 (type: {data2.data_type.value}, subtype: {data2.data_subtype.value}): {data2.value}")
    print(f"XOR Result: {result.value}")
    
    # Classes
    print("\n\n4. CLASS HIERARCHY")
    print("-" * 70)
    and_gate = ANDGateClass()
    or_gate = ORGateClass()
    multibit_and = MultiBitANDGate(8)
    
    print(f"{and_gate.name}: {and_gate.execute(1, 1)}")
    print(f"{or_gate.name}: {or_gate.execute(0, 1)}")
    print(f"{multibit_and.name}: {multibit_and.execute_multi([1,0,1,0,1,0,1,0], [1,1,1,1,0,0,0,0])}")
    
    # Modules
    print("\n\n5. MODULE HIERARCHY")
    print("-" * 70)
    mod_hierarchy = ModuleHierarchy()
    
    main_module = mod_hierarchy.create_module("LogicUnit")
    main_module.add_gate(ANDGateClass())
    main_module.add_gate(ORGateClass())
    main_module.add_gate(XORGateClass())
    
    sub1 = mod_hierarchy.create_submodule("LogicUnit", "ArithmeticSubUnit")
    sub2 = mod_hierarchy.create_submodule("LogicUnit", "ComparisonSubUnit")
    
    print(f"Module: {main_module.name}")
    print(f"  Gates: {len(main_module.gates)}")
    print(f"  Submodules: {len(main_module.submodules)}")
    for sub in main_module.submodules:
        print(f"    - {sub.name}")

if __name__ == "__main__":
    demonstrate_all()
