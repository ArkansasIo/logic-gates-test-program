-- ============================================================================
-- LOGIC GATES DATABASE SCHEMA
-- Complete SQL schema for storing logic gate truth tables and operations
-- ============================================================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS gate_operations;
DROP TABLE IF EXISTS truth_table;
DROP TABLE IF EXISTS logic_gates;
DROP TABLE IF EXISTS gate_types;
DROP TABLE IF EXISTS computer_components;
DROP TABLE IF EXISTS cpu_instructions;
DROP TABLE IF EXISTS memory_operations;

-- ============================================================================
-- GATE TYPES TABLE
-- ============================================================================

CREATE TABLE gate_types (
    gate_id INTEGER PRIMARY KEY,
    gate_name VARCHAR(10) NOT NULL UNIQUE,
    num_inputs INTEGER NOT NULL,
    description TEXT,
    symbol VARCHAR(5)
);

-- Insert all logic gate types
INSERT INTO gate_types (gate_id, gate_name, num_inputs, description, symbol) VALUES
(1, 'AND', 2, 'Returns 1 only if both inputs are 1', '&'),
(2, 'OR', 2, 'Returns 1 if at least one input is 1', '|'),
(3, 'NOT', 1, 'Inverts the input', '~'),
(4, 'NAND', 2, 'NOT-AND, returns 0 only if both inputs are 1', '~&'),
(5, 'NOR', 2, 'NOT-OR, returns 1 only if both inputs are 0', '~|'),
(6, 'XOR', 2, 'Returns 1 if inputs are different', '^'),
(7, 'XNOR', 2, 'Returns 1 if inputs are the same', '~^'),
(8, 'BUFFER', 1, 'Passes input unchanged', '->');

-- ============================================================================
-- TRUTH TABLES FOR ALL LOGIC GATES
-- ============================================================================

CREATE TABLE truth_table (
    truth_id INTEGER PRIMARY KEY AUTOINCREMENT,
    gate_id INTEGER NOT NULL,
    input_a INTEGER NOT NULL CHECK(input_a IN (0, 1)),
    input_b INTEGER CHECK(input_b IN (0, 1)),
    output INTEGER NOT NULL CHECK(output IN (0, 1)),
    FOREIGN KEY (gate_id) REFERENCES gate_types(gate_id)
);

-- AND Gate Truth Table
INSERT INTO truth_table (gate_id, input_a, input_b, output) VALUES
(1, 0, 0, 0),
(1, 0, 1, 0),
(1, 1, 0, 0),
(1, 1, 1, 1);

-- OR Gate Truth Table
INSERT INTO truth_table (gate_id, input_a, input_b, output) VALUES
(2, 0, 0, 0),
(2, 0, 1, 1),
(2, 1, 0, 1),
(2, 1, 1, 1);

-- NOT Gate Truth Table
INSERT INTO truth_table (gate_id, input_a, input_b, output) VALUES
(3, 0, NULL, 1),
(3, 1, NULL, 0);

-- NAND Gate Truth Table
INSERT INTO truth_table (gate_id, input_a, input_b, output) VALUES
(4, 0, 0, 1),
(4, 0, 1, 1),
(4, 1, 0, 1),
(4, 1, 1, 0);

-- NOR Gate Truth Table
INSERT INTO truth_table (gate_id, input_a, input_b, output) VALUES
(5, 0, 0, 1),
(5, 0, 1, 0),
(5, 1, 0, 0),
(5, 1, 1, 0);

-- XOR Gate Truth Table
INSERT INTO truth_table (gate_id, input_a, input_b, output) VALUES
(6, 0, 0, 0),
(6, 0, 1, 1),
(6, 1, 0, 1),
(6, 1, 1, 0);

-- XNOR Gate Truth Table
INSERT INTO truth_table (gate_id, input_a, input_b, output) VALUES
(7, 0, 0, 1),
(7, 0, 1, 0),
(7, 1, 0, 0),
(7, 1, 1, 1);

-- BUFFER Gate Truth Table
INSERT INTO truth_table (gate_id, input_a, input_b, output) VALUES
(8, 0, NULL, 0),
(8, 1, NULL, 1);

-- ============================================================================
-- GATE OPERATIONS LOG
-- ============================================================================

CREATE TABLE gate_operations (
    operation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    gate_id INTEGER NOT NULL,
    input_a INTEGER NOT NULL CHECK(input_a IN (0, 1)),
    input_b INTEGER CHECK(input_b IN (0, 1)),
    output INTEGER NOT NULL CHECK(output IN (0, 1)),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (gate_id) REFERENCES gate_types(gate_id)
);

-- ============================================================================
-- COMPUTER COMPONENTS TABLE
-- ============================================================================

CREATE TABLE computer_components (
    component_id INTEGER PRIMARY KEY,
    component_name VARCHAR(20) NOT NULL UNIQUE,
    component_type VARCHAR(20) NOT NULL,
    description TEXT,
    size_bytes INTEGER,
    speed_mhz INTEGER,
    is_volatile INTEGER CHECK(is_volatile IN (0, 1))
);

-- Insert computer components
INSERT INTO computer_components (component_id, component_name, component_type, description, size_bytes, speed_mhz, is_volatile) VALUES
(1, 'CPU', 'Processor', '8-bit Central Processing Unit', NULL, 8, 0),
(2, 'GPU', 'Processor', 'Graphics Processing Unit', NULL, 4, 0),
(3, 'RAM', 'Memory', 'Random Access Memory - Volatile', 256, NULL, 1),
(4, 'ROM', 'Memory', 'Read-Only Memory - Non-volatile', 256, NULL, 0),
(5, 'EEPROM', 'Memory', 'Electrically Erasable Programmable ROM', 128, NULL, 0),
(6, 'Storage', 'Storage', 'Hard Drive Storage', 65536, NULL, 0),
(7, 'CMOS', 'Settings', 'BIOS settings and Real-Time Clock', 128, NULL, 0),
(8, 'BIOS', 'Firmware', 'Basic Input/Output System', NULL, NULL, 0);

-- ============================================================================
-- CPU INSTRUCTION SET TABLE
-- ============================================================================

CREATE TABLE cpu_instructions (
    opcode INTEGER PRIMARY KEY,
    mnemonic VARCHAR(10) NOT NULL UNIQUE,
    description TEXT,
    num_operands INTEGER,
    cycles INTEGER,
    affects_flags VARCHAR(10)
);

-- Insert 8-bit CPU instruction set
INSERT INTO cpu_instructions (opcode, mnemonic, description, num_operands, cycles, affects_flags) VALUES
(0x00, 'NOP', 'No Operation', 0, 1, ''),
(0x01, 'LDA', 'Load A from memory', 1, 2, 'Z'),
(0x02, 'LDB', 'Load B from memory', 1, 2, 'Z'),
(0x03, 'STA', 'Store A to memory', 1, 2, ''),
(0x04, 'STB', 'Store B to memory', 1, 2, ''),
(0x10, 'ADD', 'Add B to A', 0, 1, 'ZC'),
(0x11, 'SUB', 'Subtract B from A', 0, 1, 'ZC'),
(0x12, 'AND', 'Bitwise AND A with B', 0, 1, 'Z'),
(0x13, 'OR', 'Bitwise OR A with B', 0, 1, 'Z'),
(0x14, 'XOR', 'Bitwise XOR A with B', 0, 1, 'Z'),
(0x15, 'NOT', 'Bitwise NOT A', 0, 1, 'Z'),
(0x16, 'SHL', 'Shift Left A', 0, 1, 'ZC'),
(0x17, 'SHR', 'Shift Right A', 0, 1, 'ZC'),
(0x20, 'JMP', 'Jump to address', 1, 2, ''),
(0x21, 'JZ', 'Jump if Zero flag set', 1, 2, ''),
(0x22, 'JNZ', 'Jump if Zero flag clear', 1, 2, ''),
(0x30, 'CALL', 'Call subroutine', 1, 3, ''),
(0x31, 'RET', 'Return from subroutine', 0, 3, ''),
(0x40, 'PUSH', 'Push A to stack', 0, 2, ''),
(0x41, 'POP', 'Pop from stack to A', 0, 2, ''),
(0xFF, 'HLT', 'Halt execution', 0, 1, '');

-- ============================================================================
-- MEMORY OPERATIONS TABLE
-- ============================================================================

CREATE TABLE memory_operations (
    operation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    component_id INTEGER NOT NULL,
    operation_type VARCHAR(10) CHECK(operation_type IN ('READ', 'WRITE')),
    address INTEGER NOT NULL,
    value INTEGER CHECK(value >= 0 AND value <= 255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (component_id) REFERENCES computer_components(component_id)
);

-- ============================================================================
-- USEFUL QUERIES AND VIEWS
-- ============================================================================

-- View: Complete truth tables with gate names
CREATE VIEW v_truth_tables AS
SELECT 
    gt.gate_name,
    tt.input_a,
    tt.input_b,
    tt.output
FROM truth_table tt
JOIN gate_types gt ON tt.gate_id = gt.gate_id
ORDER BY gt.gate_id, tt.truth_id;

-- View: Gate operation statistics
CREATE VIEW v_gate_statistics AS
SELECT 
    gt.gate_name,
    COUNT(*) as operation_count,
    COUNT(CASE WHEN go.output = 1 THEN 1 END) as output_ones,
    COUNT(CASE WHEN go.output = 0 THEN 1 END) as output_zeros
FROM gate_operations go
JOIN gate_types gt ON go.gate_id = gt.gate_id
GROUP BY gt.gate_name;

-- View: CPU instruction summary
CREATE VIEW v_cpu_instruction_summary AS
SELECT 
    opcode,
    mnemonic,
    description,
    num_operands,
    cycles,
    affects_flags,
    CASE 
        WHEN opcode BETWEEN 0x00 AND 0x0F THEN 'Memory Operations'
        WHEN opcode BETWEEN 0x10 AND 0x1F THEN 'Arithmetic/Logic'
        WHEN opcode BETWEEN 0x20 AND 0x2F THEN 'Control Flow'
        WHEN opcode BETWEEN 0x30 AND 0x3F THEN 'Subroutine'
        WHEN opcode BETWEEN 0x40 AND 0x4F THEN 'Stack Operations'
        ELSE 'Special'
    END as instruction_category
FROM cpu_instructions
ORDER BY opcode;

-- View: Memory component summary
CREATE VIEW v_memory_summary AS
SELECT 
    component_name,
    description,
    size_bytes,
    CASE 
        WHEN is_volatile = 1 THEN 'Volatile'
        ELSE 'Non-volatile'
    END as volatility,
    COALESCE(
        (SELECT COUNT(*) FROM memory_operations mo 
         WHERE mo.component_id = cc.component_id), 0
    ) as total_operations
FROM computer_components cc
WHERE component_type IN ('Memory', 'Storage')
ORDER BY size_bytes DESC;

-- ============================================================================
-- SAMPLE QUERIES
-- ============================================================================

-- Query 1: Get truth table for specific gate
-- SELECT * FROM v_truth_tables WHERE gate_name = 'AND';

-- Query 2: Find all gates that output 1 for inputs (1,1)
-- SELECT gate_name FROM truth_table tt
-- JOIN gate_types gt ON tt.gate_id = gt.gate_id
-- WHERE input_a = 1 AND input_b = 1 AND output = 1;

-- Query 3: Get all instructions that affect the Zero flag
-- SELECT mnemonic, description FROM cpu_instructions
-- WHERE affects_flags LIKE '%Z%';

-- Query 4: Memory operations summary by component
-- SELECT 
--     cc.component_name,
--     COUNT(*) as total_ops,
--     COUNT(CASE WHEN mo.operation_type = 'READ' THEN 1 END) as reads,
--     COUNT(CASE WHEN mo.operation_type = 'WRITE' THEN 1 END) as writes
-- FROM memory_operations mo
-- JOIN computer_components cc ON mo.component_id = cc.component_id
-- GROUP BY cc.component_name;

-- ============================================================================
-- STORED PROCEDURES (SQLite doesn't support these, but here's the logic)
-- ============================================================================

-- Function to evaluate logic gate
-- CREATE FUNCTION eval_gate(gate_name VARCHAR, a INT, b INT) RETURNS INT
-- This would look up the truth table and return the output

-- Procedure to log gate operation
-- CREATE PROCEDURE log_gate_operation(gate_name VARCHAR, a INT, b INT, output INT)
-- This would insert into gate_operations table

-- ============================================================================
-- BINARY/HEXADECIMAL LOOKUP TABLE
-- ============================================================================

CREATE TABLE binary_hex_lookup (
    decimal_value INTEGER PRIMARY KEY CHECK(decimal_value >= 0 AND decimal_value <= 255),
    binary_value VARCHAR(8) NOT NULL,
    hex_value VARCHAR(2) NOT NULL
);

-- Insert values for 0-255
-- (Sample entries - you can generate all 256)
INSERT INTO binary_hex_lookup (decimal_value, binary_value, hex_value) VALUES
(0, '00000000', '00'),
(1, '00000001', '01'),
(2, '00000010', '02'),
(3, '00000011', '03'),
(4, '00000100', '04'),
(5, '00000101', '05'),
(6, '00000110', '06'),
(7, '00000111', '07'),
(8, '00001000', '08'),
(15, '00001111', '0F'),
(16, '00010000', '10'),
(31, '00011111', '1F'),
(32, '00100000', '20'),
(63, '00111111', '3F'),
(64, '01000000', '40'),
(127, '01111111', '7F'),
(128, '10000000', '80'),
(255, '11111111', 'FF');

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

CREATE INDEX idx_truth_table_gate ON truth_table(gate_id);
CREATE INDEX idx_truth_table_inputs ON truth_table(input_a, input_b);
CREATE INDEX idx_gate_operations_gate ON gate_operations(gate_id);
CREATE INDEX idx_gate_operations_time ON gate_operations(timestamp);
CREATE INDEX idx_memory_operations_component ON memory_operations(component_id);
CREATE INDEX idx_memory_operations_type ON memory_operations(operation_type);

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Display summary
SELECT 'Logic Gates Database Schema Created Successfully!' as Status;
SELECT COUNT(*) as 'Total Logic Gates' FROM gate_types;
SELECT COUNT(*) as 'Total Truth Table Entries' FROM truth_table;
SELECT COUNT(*) as 'Total CPU Instructions' FROM cpu_instructions;
SELECT COUNT(*) as 'Total Computer Components' FROM computer_components;
