"""
SQL Database Generator and Manager
Creates and manages the logic gates database
"""

import sqlite3
from typing import List, Tuple
from logic_gates import *
from computer_components import Opcode

class LogicGatesDatabaseManager:
    """Manager for logic gates database"""
    
    def __init__(self, db_path: str = "logic_gates.db"):
        """Initialize database manager"""
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        return self.conn
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def create_database(self):
        """Create database from SQL schema"""
        print("Creating database...")
        
        # Read SQL schema
        with open('logic_gates_database.sql', 'r') as f:
            sql_script = f.read()
        
        # Execute schema
        cursor = self.conn.cursor()
        
        # Split and execute statements (SQLite doesn't handle all in one go)
        statements = sql_script.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    cursor.execute(statement)
                except sqlite3.OperationalError as e:
                    if "already exists" not in str(e):
                        print(f"Warning: {e}")
        
        self.conn.commit()
        print("Database created successfully!")
    
    def log_gate_operation(self, gate_name: str, input_a: int, input_b: int = None, output: int = None):
        """Log a gate operation to the database"""
        cursor = self.conn.cursor()
        
        # Get gate_id
        cursor.execute("SELECT gate_id FROM gate_types WHERE gate_name = ?", (gate_name,))
        result = cursor.fetchone()
        if not result:
            return
        
        gate_id = result[0]
        
        # Execute gate if output not provided
        if output is None:
            gate = LogicGate(GateType[gate_name])
            output = gate.execute(input_a, input_b)
        
        # Insert operation
        cursor.execute("""
            INSERT INTO gate_operations (gate_id, input_a, input_b, output)
            VALUES (?, ?, ?, ?)
        """, (gate_id, input_a, input_b, output))
        
        self.conn.commit()
    
    def log_memory_operation(self, component_name: str, operation_type: str, address: int, value: int):
        """Log a memory operation"""
        cursor = self.conn.cursor()
        
        # Get component_id
        cursor.execute("SELECT component_id FROM computer_components WHERE component_name = ?", (component_name,))
        result = cursor.fetchone()
        if not result:
            return
        
        component_id = result[0]
        
        # Insert operation
        cursor.execute("""
            INSERT INTO memory_operations (component_id, operation_type, address, value)
            VALUES (?, ?, ?, ?)
        """, (component_id, operation_type, address, value))
        
        self.conn.commit()
    
    def get_truth_table(self, gate_name: str) -> List[Tuple]:
        """Get truth table for a specific gate"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT input_a, input_b, output
            FROM v_truth_tables
            WHERE gate_name = ?
            ORDER BY input_a, input_b
        """, (gate_name,))
        return cursor.fetchall()
    
    def get_gate_statistics(self) -> List[Tuple]:
        """Get statistics for all gates"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM v_gate_statistics")
        return cursor.fetchall()
    
    def get_cpu_instructions(self) -> List[Tuple]:
        """Get all CPU instructions"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT opcode, mnemonic, description, num_operands, cycles
            FROM cpu_instructions
            ORDER BY opcode
        """)
        return cursor.fetchall()
    
    def display_truth_tables(self):
        """Display all truth tables"""
        print("\n" + "=" * 60)
        print("TRUTH TABLES FROM DATABASE")
        print("=" * 60)
        
        gates = ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR', 'XNOR', 'BUFFER']
        
        for gate_name in gates:
            table = self.get_truth_table(gate_name)
            print(f"\n{gate_name} Gate:")
            
            if table[0][1] is None:  # Single input gate
                print("  A | Output")
                print("  --|-------")
                for row in table:
                    print(f"  {row[0]} |   {row[2]}")
            else:  # Two input gate
                print("  A | B | Output")
                print("  --|---|-------")
                for row in table:
                    print(f"  {row[0]} | {row[1]} |   {row[2]}")
    
    def display_cpu_instructions(self):
        """Display CPU instruction set"""
        print("\n" + "=" * 80)
        print("8-BIT CPU INSTRUCTION SET")
        print("=" * 80)
        
        instructions = self.get_cpu_instructions()
        
        print(f"\n{'Opcode':<8} {'Mnemonic':<10} {'Operands':<10} {'Cycles':<8} {'Description'}")
        print("-" * 80)
        
        for opcode, mnemonic, description, num_operands, cycles in instructions:
            opcode_str = f"0x{opcode:02X}"
            print(f"{opcode_str:<8} {mnemonic:<10} {num_operands:<10} {cycles:<8} {description}")
    
    def display_memory_operations(self):
        """Display memory operation statistics"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                cc.component_name,
                COUNT(*) as total_ops,
                COUNT(CASE WHEN mo.operation_type = 'READ' THEN 1 END) as reads,
                COUNT(CASE WHEN mo.operation_type = 'WRITE' THEN 1 END) as writes
            FROM memory_operations mo
            JOIN computer_components cc ON mo.component_id = cc.component_id
            GROUP BY cc.component_name
        """)
        
        results = cursor.fetchall()
        
        if results:
            print("\n" + "=" * 60)
            print("MEMORY OPERATIONS STATISTICS")
            print("=" * 60)
            
            print(f"\n{'Component':<15} {'Total Ops':<12} {'Reads':<10} {'Writes':<10}")
            print("-" * 60)
            
            for row in results:
                print(f"{row[0]:<15} {row[1]:<12} {row[2]:<10} {row[3]:<10}")
        else:
            print("\nNo memory operations logged yet.")
    
    def run_tests(self):
        """Run test operations and log them"""
        print("\n" + "=" * 60)
        print("RUNNING TEST OPERATIONS")
        print("=" * 60)
        
        # Test logic gates
        print("\nTesting logic gates...")
        test_cases = [(0,0), (0,1), (1,0), (1,1)]
        
        for a, b in test_cases:
            self.log_gate_operation('AND', a, b)
            self.log_gate_operation('OR', a, b)
            self.log_gate_operation('XOR', a, b)
        
        # Test single-input gates
        for a in [0, 1]:
            self.log_gate_operation('NOT', a, None)
        
        print("Logged 14 gate operations")
        
        # Test memory operations
        print("\nTesting memory operations...")
        for i in range(10):
            self.log_memory_operation('RAM', 'WRITE', i, i * 10)
            self.log_memory_operation('RAM', 'READ', i, i * 10)
        
        print("Logged 20 memory operations")
        
        # Display statistics
        stats = self.get_gate_statistics()
        if stats:
            print("\n" + "=" * 60)
            print("GATE OPERATION STATISTICS")
            print("=" * 60)
            
            print(f"\n{'Gate':<10} {'Operations':<12} {'Ones':<10} {'Zeros':<10}")
            print("-" * 60)
            
            for gate_name, op_count, ones, zeros in stats:
                print(f"{gate_name:<10} {op_count:<12} {ones:<10} {zeros:<10}")

def main():
    """Main function"""
    print("=" * 60)
    print("LOGIC GATES DATABASE MANAGER")
    print("=" * 60)
    
    db = LogicGatesDatabaseManager()
    db.connect()
    
    try:
        # Create database
        db.create_database()
        
        # Display truth tables
        db.display_truth_tables()
        
        # Display CPU instructions
        db.display_cpu_instructions()
        
        # Run tests
        db.run_tests()
        
        # Display memory operations
        db.display_memory_operations()
        
        print("\n" + "=" * 60)
        print("Database location: " + db.db_path)
        print("=" * 60)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
