"""
REST API for Logic Gates and 8-bit Computer
Provides HTTP interface to all system functions
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json
from datetime import datetime

# Try to import Flask, fallback to simple HTTP server if not available
try:
    from flask import Flask, request, jsonify
    USE_FLASK = True
except ImportError:
    USE_FLASK = False
    print("Flask not installed. API will use simple JSON responses.")

from logic_gates import *
from computer_components import *
from assembly_language import *
from math_calculator import *
from character_logic_gates import *

# ============================================================================
# API RESPONSE MODELS
# ============================================================================

@dataclass
class APIResponse:
    """Standard API response format"""
    success: bool
    data: Any
    message: str = ""
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

@dataclass
class LogicGateRequest:
    """Request for logic gate operation"""
    gate_type: str
    input_a: int
    input_b: Optional[int] = None

@dataclass
class AssemblyRequest:
    """Request for assembly operation"""
    code: str
    operation: str  # 'assemble' or 'disassemble'

@dataclass
class CalculatorRequest:
    """Request for calculator operation"""
    operation: str
    operand_a: int
    operand_b: Optional[int] = None
    calculator_type: str = "basic"

# ============================================================================
# API ENDPOINTS CLASS
# ============================================================================

class LogicGatesAPI:
    """Main API class for logic gates system"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.name = "Logic Gates and 8-bit Computer API"
        
        # Initialize components
        self.ram = RAM(256)
        self.cpu = CPU(self.ram)
        self.assembler = Assembler()
        self.calculator = Calculator(CalculatorType.BASIC)
    
    # ========================================================================
    # SYSTEM ENDPOINTS
    # ========================================================================
    
    def get_api_info(self) -> APIResponse:
        """Get API information"""
        info = {
            'name': self.name,
            'version': self.version,
            'endpoints': self.list_endpoints()
        }
        return APIResponse(success=True, data=info, message="API information retrieved")
    
    def list_endpoints(self) -> List[str]:
        """List all available endpoints"""
        return [
            '/api/info',
            '/api/gate/execute',
            '/api/gate/truth_table',
            '/api/calculator/compute',
            '/api/assembly/assemble',
            '/api/assembly/disassemble',
            '/api/cpu/execute',
            '/api/cpu/registers',
            '/api/memory/read',
            '/api/memory/write',
            '/api/character/operate',
            '/api/binary/convert',
        ]
    
    # ========================================================================
    # LOGIC GATE ENDPOINTS
    # ========================================================================
    
    def execute_gate(self, gate_type: str, input_a: int, input_b: int = None) -> APIResponse:
        """Execute logic gate operation"""
        try:
            gate_type_enum = GateType[gate_type.upper()]
            gate = LogicGate(gate_type_enum)
            
            result = gate.execute(input_a, input_b)
            
            data = {
                'gate_type': gate_type,
                'input_a': input_a,
                'input_b': input_b,
                'output': result
            }
            
            return APIResponse(
                success=True,
                data=data,
                message=f"{gate_type} gate executed successfully"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Error executing gate: {str(e)}"
            )
    
    def get_truth_table(self, gate_type: str) -> APIResponse:
        """Get truth table for logic gate"""
        try:
            gate_type_enum = GateType[gate_type.upper()]
            gate = LogicGate(gate_type_enum)
            
            truth_table = gate.get_truth_table()
            
            data = {
                'gate_type': gate_type,
                'truth_table': [
                    {'inputs': list(row[:-1]), 'output': row[-1]}
                    for row in truth_table
                ]
            }
            
            return APIResponse(
                success=True,
                data=data,
                message=f"Truth table for {gate_type} retrieved"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Error getting truth table: {str(e)}"
            )
    
    # ========================================================================
    # CALCULATOR ENDPOINTS
    # ========================================================================
    
    def calculate(self, operation: str, operand_a: int, operand_b: int = None) -> APIResponse:
        """Perform calculator operation"""
        try:
            result = None
            
            if operation == 'add':
                result = self.calculator.add(operand_a, operand_b)
            elif operation == 'subtract':
                result = self.calculator.subtract(operand_a, operand_b)
            elif operation == 'multiply':
                result = self.calculator.multiply(operand_a, operand_b)
            elif operation == 'divide':
                result, remainder = self.calculator.divide(operand_a, operand_b)
                return APIResponse(
                    success=True,
                    data={
                        'quotient': result.value,
                        'remainder': remainder.value,
                        'operation': operation
                    },
                    message="Division completed"
                )
            elif operation == 'and':
                result = self.calculator.bitwise_and(operand_a, operand_b)
            elif operation == 'or':
                result = self.calculator.bitwise_or(operand_a, operand_b)
            elif operation == 'xor':
                result = self.calculator.bitwise_xor(operand_a, operand_b)
            elif operation == 'not':
                result = self.calculator.bitwise_not(operand_a)
            else:
                return APIResponse(
                    success=False,
                    data=None,
                    message=f"Unknown operation: {operation}"
                )
            
            data = {
                'operation': operation,
                'result': result.value,
                'binary': ''.join(map(str, result.binary_result)) if result.binary_result else None
            }
            
            return APIResponse(
                success=True,
                data=data,
                message=f"Calculation {operation} completed"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Error in calculation: {str(e)}"
            )
    
    # ========================================================================
    # ASSEMBLY ENDPOINTS
    # ========================================================================
    
    def assemble_code(self, code: str) -> APIResponse:
        """Assemble assembly code to machine code"""
        try:
            machine_code = self.assembler.assemble(code)
            
            data = {
                'assembly_code': code,
                'machine_code': [f"0x{byte:02X}" for byte in machine_code],
                'size_bytes': len(machine_code)
            }
            
            return APIResponse(
                success=True,
                data=data,
                message="Assembly completed"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Assembly error: {str(e)}"
            )
    
    def disassemble_code(self, machine_code: List[int]) -> APIResponse:
        """Disassemble machine code to assembly"""
        try:
            assembly = self.assembler.disassemble(machine_code)
            
            data = {
                'machine_code': [f"0x{byte:02X}" for byte in machine_code],
                'assembly': assembly
            }
            
            return APIResponse(
                success=True,
                data=data,
                message="Disassembly completed"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Disassembly error: {str(e)}"
            )
    
    # ========================================================================
    # CPU ENDPOINTS
    # ========================================================================
    
    def execute_cpu_program(self, program: List[int]) -> APIResponse:
        """Execute program on CPU"""
        try:
            # Load program into RAM
            for i, byte in enumerate(program):
                if i < 256:
                    self.ram.write(i, byte)
            
            # Reset and run CPU
            self.cpu.reset()
            self.cpu.run(max_cycles=1000)
            
            data = {
                'cycles_executed': self.cpu.cycles,
                'halted': self.cpu.halted,
                'registers': {
                    'A': self.cpu.registers.A,
                    'B': self.cpu.registers.B,
                    'PC': self.cpu.registers.PC,
                    'SP': self.cpu.registers.SP,
                    'FLAGS': self.cpu.registers.FLAGS
                }
            }
            
            return APIResponse(
                success=True,
                data=data,
                message="Program executed"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"CPU execution error: {str(e)}"
            )
    
    def get_cpu_registers(self) -> APIResponse:
        """Get CPU register values"""
        data = {
            'A': self.cpu.registers.A,
            'B': self.cpu.registers.B,
            'C': self.cpu.registers.C,
            'D': self.cpu.registers.D,
            'PC': self.cpu.registers.PC,
            'SP': self.cpu.registers.SP,
            'FLAGS': self.cpu.registers.FLAGS,
            'flags_detail': {
                'Zero': self.cpu.registers.get_flag('Z'),
                'Carry': self.cpu.registers.get_flag('C'),
                'Negative': self.cpu.registers.get_flag('N'),
                'Overflow': self.cpu.registers.get_flag('O')
            }
        }
        
        return APIResponse(
            success=True,
            data=data,
            message="CPU registers retrieved"
        )
    
    # ========================================================================
    # MEMORY ENDPOINTS
    # ========================================================================
    
    def read_memory(self, address: int, count: int = 1) -> APIResponse:
        """Read from memory"""
        try:
            values = []
            for i in range(count):
                addr = (address + i) & 0xFF
                values.append(self.ram.read(addr))
            
            data = {
                'address': f"0x{address:02X}",
                'count': count,
                'values': [f"0x{v:02X}" for v in values]
            }
            
            return APIResponse(
                success=True,
                data=data,
                message=f"Read {count} bytes from memory"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Memory read error: {str(e)}"
            )
    
    def write_memory(self, address: int, value: int) -> APIResponse:
        """Write to memory"""
        try:
            self.ram.write(address, value)
            
            data = {
                'address': f"0x{address:02X}",
                'value': f"0x{value:02X}"
            }
            
            return APIResponse(
                success=True,
                data=data,
                message=f"Wrote to memory at 0x{address:02X}"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Memory write error: {str(e)}"
            )
    
    # ========================================================================
    # CHARACTER ENDPOINTS
    # ========================================================================
    
    def character_operation(self, char1: str, char2: str, operation: str) -> APIResponse:
        """Perform logic operation on characters"""
        try:
            if operation == 'AND':
                result = CharacterLogicOperations.char_AND(char1, char2)
            elif operation == 'OR':
                result = CharacterLogicOperations.char_OR(char1, char2)
            elif operation == 'XOR':
                result = CharacterLogicOperations.char_XOR(char1, char2)
            elif operation == 'NOT':
                result = CharacterLogicOperations.char_NOT(char1)
            else:
                return APIResponse(
                    success=False,
                    data=None,
                    message=f"Unknown operation: {operation}"
                )
            
            data = {
                'char1': char1,
                'char1_ascii': ord(char1),
                'char2': char2 if char2 else None,
                'char2_ascii': ord(char2) if char2 else None,
                'operation': operation,
                'result': result,
                'result_ascii': ord(result)
            }
            
            return APIResponse(
                success=True,
                data=data,
                message="Character operation completed"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Character operation error: {str(e)}"
            )
    
    # ========================================================================
    # BINARY CONVERSION ENDPOINTS
    # ========================================================================
    
    def convert_binary(self, value: int, to_format: str) -> APIResponse:
        """Convert value to different formats"""
        try:
            binary = BinaryOperations.int_to_8bit(value)
            
            data = {
                'decimal': value,
                'binary': ''.join(map(str, binary)),
                'hexadecimal': f"0x{value:02X}",
                'octal': f"0o{value:03o}"
            }
            
            if to_format.lower() == 'binary':
                result = data['binary']
            elif to_format.lower() == 'hex':
                result = data['hexadecimal']
            elif to_format.lower() == 'octal':
                result = data['octal']
            else:
                result = data
            
            return APIResponse(
                success=True,
                data=data,
                message=f"Converted {value} to {to_format}"
            )
        
        except Exception as e:
            return APIResponse(
                success=False,
                data=None,
                message=f"Conversion error: {str(e)}"
            )

# ============================================================================
# FLASK APPLICATION (if Flask is available)
# ============================================================================

if USE_FLASK:
    app = Flask(__name__)
    api = LogicGatesAPI()
    
    @app.route('/api/info', methods=['GET'])
    def api_info():
        response = api.get_api_info()
        return jsonify(response.to_dict())
    
    @app.route('/api/gate/execute', methods=['POST'])
    def execute_gate():
        data = request.get_json()
        response = api.execute_gate(
            data.get('gate_type'),
            data.get('input_a'),
            data.get('input_b')
        )
        return jsonify(response.to_dict())
    
    @app.route('/api/gate/truth_table/<gate_type>', methods=['GET'])
    def truth_table(gate_type):
        response = api.get_truth_table(gate_type)
        return jsonify(response.to_dict())
    
    @app.route('/api/calculator/compute', methods=['POST'])
    def calculate():
        data = request.get_json()
        response = api.calculate(
            data.get('operation'),
            data.get('operand_a'),
            data.get('operand_b')
        )
        return jsonify(response.to_dict())
    
    @app.route('/api/assembly/assemble', methods=['POST'])
    def assemble():
        data = request.get_json()
        response = api.assemble_code(data.get('code'))
        return jsonify(response.to_dict())
    
    @app.route('/api/cpu/registers', methods=['GET'])
    def cpu_registers():
        response = api.get_cpu_registers()
        return jsonify(response.to_dict())
    
    @app.route('/api/memory/read/<int:address>', methods=['GET'])
    def read_memory(address):
        count = request.args.get('count', 1, type=int)
        response = api.read_memory(address, count)
        return jsonify(response.to_dict())
    
    @app.route('/api/memory/write', methods=['POST'])
    def write_memory():
        data = request.get_json()
        response = api.write_memory(
            data.get('address'),
            data.get('value')
        )
        return jsonify(response.to_dict())

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_api():
    """Demonstrate API functionality"""
    
    print("=" * 70)
    print("LOGIC GATES API DEMONSTRATION")
    print("=" * 70)
    
    api = LogicGatesAPI()
    
    # System info
    print("\n1. API INFO")
    print("-" * 70)
    response = api.get_api_info()
    print(response.to_json())
    
    # Logic gate
    print("\n\n2. EXECUTE LOGIC GATE")
    print("-" * 70)
    response = api.execute_gate("AND", 1, 1)
    print(response.to_json())
    
    # Calculator
    print("\n\n3. CALCULATOR")
    print("-" * 70)
    response = api.calculate("add", 25, 17)
    print(response.to_json())
    
    # Assembly
    print("\n\n4. ASSEMBLE CODE")
    print("-" * 70)
    code = "LDA 0x10\nADD\nHLT"
    response = api.assemble_code(code)
    print(response.to_json())
    
    # Memory
    print("\n\n5. MEMORY OPERATIONS")
    print("-" * 70)
    write_response = api.write_memory(0x10, 0xFF)
    print(write_response.to_json())
    
    read_response = api.read_memory(0x10)
    print(read_response.to_json())
    
    # Character operations
    print("\n\n6. CHARACTER OPERATIONS")
    print("-" * 70)
    response = api.character_operation('A', 'B', 'XOR')
    print(response.to_json())

if __name__ == "__main__":
    demonstrate_api()
    
    if USE_FLASK:
        print("\n\nStarting Flask API server...")
        print("Visit http://localhost:5000/api/info")
        # app.run(debug=True, port=5000)
    else:
        print("\n\nFlask not available. Install with: pip install flask")
