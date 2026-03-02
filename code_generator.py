"""
Code Generator for Multiple Programming Languages
Generates ASM, C, and C++17 implementations of logic gates
"""

from typing import List, Dict
from enum import Enum

# ============================================================================
# LANGUAGE TYPES
# ============================================================================

class ProgrammingLanguage(Enum):
    """Programming language enumeration"""
    ASM_X86 = "asm_x86"
    ASM_8BIT = "asm_8bit"
    C = "c"
    CPP = "cpp"
    CPP17 = "cpp17"

# ============================================================================
# C CODE GENERATOR
# ============================================================================

class CCodeGenerator:
    """Generates C code for logic gates"""
    
    @staticmethod
    def generate_header() -> str:
        """Generate C header file"""
        return """/*
 * Logic Gates Library - C Implementation
 * 8-bit Logic Operations
 */

#ifndef LOGIC_GATES_H
#define LOGIC_GATES_H

#include <stdint.h>
#include <stdio.h>

/* Basic Logic Gates */
uint8_t AND(uint8_t a, uint8_t b);
uint8_t OR(uint8_t a, uint8_t b);
uint8_t NOT(uint8_t a);
uint8_t NAND(uint8_t a, uint8_t b);
uint8_t NOR(uint8_t a, uint8_t b);
uint8_t XOR(uint8_t a, uint8_t b);
uint8_t XNOR(uint8_t a, uint8_t b);

/* Compound Gates */
void HALF_ADDER(uint8_t a, uint8_t b, uint8_t* sum, uint8_t* carry);
void FULL_ADDER(uint8_t a, uint8_t b, uint8_t cin, uint8_t* sum, uint8_t* cout);

/* 8-bit Operations */
uint8_t add_8bit(uint8_t a, uint8_t b);
uint8_t subtract_8bit(uint8_t a, uint8_t b);
uint8_t multiply_8bit(uint8_t a, uint8_t b);
uint8_t divide_8bit(uint8_t a, uint8_t b, uint8_t* remainder);

/* Bitwise Operations */
uint8_t bitwise_and(uint8_t a, uint8_t b);
uint8_t bitwise_or(uint8_t a, uint8_t b);
uint8_t bitwise_xor(uint8_t a, uint8_t b);
uint8_t bitwise_not(uint8_t a);
uint8_t shift_left(uint8_t value, uint8_t positions);
uint8_t shift_right(uint8_t value, uint8_t positions);

#endif /* LOGIC_GATES_H */
"""
    
    @staticmethod
    def generate_implementation() -> str:
        """Generate C implementation file"""
        return """/*
 * Logic Gates Library - C Implementation
 * Implementation of all logic gate functions
 */

#include "logic_gates.h"

/* ========================================================================
 * BASIC LOGIC GATES
 * ======================================================================== */

uint8_t AND(uint8_t a, uint8_t b) {
    return a & b;
}

uint8_t OR(uint8_t a, uint8_t b) {
    return a | b;
}

uint8_t NOT(uint8_t a) {
    return ~a;
}

uint8_t NAND(uint8_t a, uint8_t b) {
    return ~(a & b);
}

uint8_t NOR(uint8_t a, uint8_t b) {
    return ~(a | b);
}

uint8_t XOR(uint8_t a, uint8_t b) {
    return a ^ b;
}

uint8_t XNOR(uint8_t a, uint8_t b) {
    return ~(a ^ b);
}

/* ========================================================================
 * COMPOUND GATES
 * ======================================================================== */

void HALF_ADDER(uint8_t a, uint8_t b, uint8_t* sum, uint8_t* carry) {
    *sum = XOR(a, b);
    *carry = AND(a, b);
}

void FULL_ADDER(uint8_t a, uint8_t b, uint8_t cin, uint8_t* sum, uint8_t* cout) {
    uint8_t sum1, carry1, carry2;
    HALF_ADDER(a, b, &sum1, &carry1);
    HALF_ADDER(sum1, cin, sum, &carry2);
    *cout = OR(carry1, carry2);
}

/* ========================================================================
 * 8-BIT OPERATIONS
 * ======================================================================== */

uint8_t add_8bit(uint8_t a, uint8_t b) {
    return a + b;
}

uint8_t subtract_8bit(uint8_t a, uint8_t b) {
    return a - b;
}

uint8_t multiply_8bit(uint8_t a, uint8_t b) {
    return (uint8_t)(a * b);
}

uint8_t divide_8bit(uint8_t a, uint8_t b, uint8_t* remainder) {
    if (b == 0) {
        *remainder = 0;
        return 0;
    }
    *remainder = a % b;
    return a / b;
}

/* ========================================================================
 * BITWISE OPERATIONS
 * ======================================================================== */

uint8_t bitwise_and(uint8_t a, uint8_t b) {
    return a & b;
}

uint8_t bitwise_or(uint8_t a, uint8_t b) {
    return a | b;
}

uint8_t bitwise_xor(uint8_t a, uint8_t b) {
    return a ^ b;
}

uint8_t bitwise_not(uint8_t a) {
    return ~a;
}

uint8_t shift_left(uint8_t value, uint8_t positions) {
    return value << positions;
}

uint8_t shift_right(uint8_t value, uint8_t positions) {
    return value >> positions;
}

/* ========================================================================
 * MAIN FUNCTION - DEMONSTRATION
 * ======================================================================== */

int main() {
    printf("Logic Gates Library - C Implementation\\n");
    printf("======================================\\n\\n");
    
    /* Test basic gates */
    printf("Basic Gates:\\n");
    printf("AND(1, 1) = %u\\n", AND(1, 1));
    printf("OR(0, 1) = %u\\n", OR(0, 1));
    printf("XOR(1, 0) = %u\\n", XOR(1, 0));
    printf("NOT(0) = %u\\n\\n", NOT(0) & 1);
    
    /* Test 8-bit operations */
    printf("8-bit Operations:\\n");
    printf("25 + 17 = %u\\n", add_8bit(25, 17));
    printf("50 - 20 = %u\\n", subtract_8bit(50, 20));
    printf("12 * 3 = %u\\n", multiply_8bit(12, 3));
    
    uint8_t remainder;
    uint8_t quotient = divide_8bit(25, 4, &remainder);
    printf("25 / 4 = %u remainder %u\\n\\n", quotient, remainder);
    
    /* Test bitwise operations */
    printf("Bitwise Operations:\\n");
    printf("0xF0 AND 0xAA = 0x%02X\\n", bitwise_and(0xF0, 0xAA));
    printf("0xF0 OR 0x0F = 0x%02X\\n", bitwise_or(0xF0, 0x0F));
    printf("0xAA XOR 0x55 = 0x%02X\\n", bitwise_xor(0xAA, 0x55));
    printf("NOT 0xAA = 0x%02X\\n", bitwise_not(0xAA));
    
    return 0;
}
"""

# ============================================================================
# C++17 CODE GENERATOR
# ============================================================================

class CPP17CodeGenerator:
    """Generates C++17 code for logic gates"""
    
    @staticmethod
    def generate_header() -> str:
        """Generate C++17 header file"""
        return """/*
 * Logic Gates Library - C++17 Implementation
 * Modern C++ with templates, constexpr, and type safety
 */

#ifndef LOGIC_GATES_HPP
#define LOGIC_GATES_HPP

#include <cstdint>
#include <array>
#include <optional>
#include <variant>
#include <iostream>
#include <string_view>

namespace LogicGates {

// ============================================================================
// Type Aliases and Constants
// ============================================================================

using Bit = uint8_t;
using Byte = uint8_t;
template<size_t N>
using BitArray = std::array<Bit, N>;

constexpr Bit LOW = 0;
constexpr Bit HIGH = 1;

// ============================================================================
// Basic Logic Gates
// ============================================================================

constexpr Bit AND(Bit a, Bit b) noexcept {
    return a & b;
}

constexpr Bit OR(Bit a, Bit b) noexcept {
    return a | b;
}

constexpr Bit NOT(Bit a) noexcept {
    return ~a & 1;
}

constexpr Bit NAND(Bit a, Bit b) noexcept {
    return NOT(AND(a, b));
}

constexpr Bit NOR(Bit a, Bit b) noexcept {
    return NOT(OR(a, b));
}

constexpr Bit XOR(Bit a, Bit b) noexcept {
    return a ^ b;
}

constexpr Bit XNOR(Bit a, Bit b) noexcept {
    return NOT(XOR(a, b));
}

// ============================================================================
// Logic Gate Classes with Templates
// ============================================================================

template<typename T>
class LogicGate {
public:
    virtual ~LogicGate() = default;
    virtual T execute(T a, T b) const = 0;
    [[nodiscard]] virtual std::string_view name() const noexcept = 0;
};

template<typename T>
class ANDGate : public LogicGate<T> {
public:
    constexpr T execute(T a, T b) const override {
        return a & b;
    }
    
    [[nodiscard]] std::string_view name() const noexcept override {
        return "AND";
    }
};

template<typename T>
class ORGate : public LogicGate<T> {
public:
    constexpr T execute(T a, T b) const override {
        return a | b;
    }
    
    [[nodiscard]] std::string_view name() const noexcept override {
        return "OR";
    }
};

template<typename T>
class XORGate : public LogicGate<T> {
public:
    constexpr T execute(T a, T b) const override {
        return a ^ b;
    }
    
    [[nodiscard]] std::string_view name() const noexcept override {
        return "XOR";
    }
};

// ============================================================================
// Compound Gates
// ============================================================================

struct HalfAdderResult {
    Bit sum;
    Bit carry;
};

constexpr HalfAdderResult HalfAdder(Bit a, Bit b) noexcept {
    return {XOR(a, b), AND(a, b)};
}

struct FullAdderResult {
    Bit sum;
    Bit carry;
};

constexpr FullAdderResult FullAdder(Bit a, Bit b, Bit cin) noexcept {
    auto [sum1, carry1] = HalfAdder(a, b);
    auto [sum, carry2] = HalfAdder(sum1, cin);
    return {sum, OR(carry1, carry2)};
}

// ============================================================================
// 8-bit Operations
// ============================================================================

class ArithmeticLogicUnit {
public:
    constexpr Byte add(Byte a, Byte b) const noexcept {
        return a + b;
    }
    
    constexpr Byte subtract(Byte a, Byte b) const noexcept {
        return a - b;
    }
    
    constexpr Byte multiply(Byte a, Byte b) const noexcept {
        return static_cast<Byte>(a * b);
    }
    
    struct DivisionResult {
        Byte quotient;
        Byte remainder;
    };
    
    [[nodiscard]] constexpr std::optional<DivisionResult> 
    divide(Byte a, Byte b) const noexcept {
        if (b == 0) return std::nullopt;
        return DivisionResult{
            static_cast<Byte>(a / b),
            static_cast<Byte>(a % b)
        };
    }
    
    constexpr Byte bitwise_and(Byte a, Byte b) const noexcept {
        return a & b;
    }
    
    constexpr Byte bitwise_or(Byte a, Byte b) const noexcept {
        return a | b;
    }
    
    constexpr Byte bitwise_xor(Byte a, Byte b) const noexcept {
        return a ^ b;
    }
    
    constexpr Byte bitwise_not(Byte a) const noexcept {
        return ~a;
    }
    
    constexpr Byte shift_left(Byte value, uint8_t positions) const noexcept {
        return value << positions;
    }
    
    constexpr Byte shift_right(Byte value, uint8_t positions) const noexcept {
        return value >> positions;
    }
};

// ============================================================================
// Modern C++17 Features
// ============================================================================

// Structured bindings example
template<typename T>
auto compute_all_gates(T a, T b) {
    return std::make_tuple(
        AND(a, b),
        OR(a, b),
        XOR(a, b),
        NAND(a, b),
        NOR(a, b),
        XNOR(a, b)
    );
}

// If constexpr example
template<typename T>
constexpr T apply_gate(T a, T b, std::string_view gate_name) {
    if constexpr (std::is_same_v<T, Bit>) {
        if (gate_name == "AND") return AND(a, b);
        if (gate_name == "OR") return OR(a, b);
        if (gate_name == "XOR") return XOR(a, b);
    }
    return 0;
}

// Fold expressions example
template<typename... Args>
constexpr Bit multi_and(Args... args) {
    return (args & ...);
}

template<typename... Args>
constexpr Bit multi_or(Args... args) {
    return (args | ...);
}

} // namespace LogicGates

#endif // LOGIC_GATES_HPP
"""
    
    @staticmethod
    def generate_implementation() -> str:
        """Generate C++17 implementation file"""
        return """/*
 * Logic Gates Library - C++17 Implementation
 * Test program demonstrating modern C++ features
 */

#include "logic_gates.hpp"
#include <iostream>
#include <iomanip>
#include <bitset>

using namespace LogicGates;

void print_truth_table() {
    std::cout << "\\nTruth Tables for Logic Gates\\n";
    std::cout << "=============================\\n\\n";
    
    std::cout << "A | B | AND | OR | XOR | NAND | NOR | XNOR\\n";
    std::cout << "--|---|-----|----|----|------|-----|-----\\n";
    
    for (Bit a : {0, 1}) {
        for (Bit b : {0, 1}) {
            auto [and_r, or_r, xor_r, nand_r, nor_r, xnor_r] = compute_all_gates(a, b);
            
            std::cout << static_cast<int>(a) << " | " 
                     << static_cast<int>(b) << " | "
                     << static_cast<int>(and_r) << "   | "
                     << static_cast<int>(or_r) << "  | "
                     << static_cast<int>(xor_r) << "  | "
                     << static_cast<int>(nand_r) << "    | "
                     << static_cast<int>(nor_r) << "   | "
                     << static_cast<int>(xnor_r) << "\\n";
        }
    }
}

void test_alu() {
    std::cout << "\\n8-bit ALU Operations\\n";
    std::cout << "====================\\n\\n";
    
    ArithmeticLogicUnit alu;
    
    std::cout << "25 + 17 = " << static_cast<int>(alu.add(25, 17)) << "\\n";
    std::cout << "50 - 20 = " << static_cast<int>(alu.subtract(50, 20)) << "\\n";
    std::cout << "12 * 3 = " << static_cast<int>(alu.multiply(12, 3)) << "\\n";
    
    if (auto result = alu.divide(25, 4)) {
        std::cout << "25 / 4 = " << static_cast<int>(result->quotient)
                 << " remainder " << static_cast<int>(result->remainder) << "\\n";
    }
    
    std::cout << "\\nBitwise Operations:\\n";
    Byte val1 = 0xF0, val2 = 0xAA;
    std::cout << "0xF0 AND 0xAA = 0x" << std::hex << std::setw(2) << std::setfill('0')
             << static_cast<int>(alu.bitwise_and(val1, val2)) << "\\n" << std::dec;
    std::cout << "0xF0 OR  0xAA = 0x" << std::hex << std::setw(2) << std::setfill('0')
             << static_cast<int>(alu.bitwise_or(val1, val2)) << "\\n" << std::dec;
    std::cout << "0xF0 XOR 0xAA = 0x" << std::hex << std::setw(2) << std::setfill('0')
             << static_cast<int>(alu.bitwise_xor(val1, val2)) << "\\n" << std::dec;
}

void test_compound_gates() {
    std::cout << "\\nCompound Gates\\n";
    std::cout << "==============\\n\\n";
    
    std::cout << "Half Adder (1 + 1):\\n";
    auto [sum, carry] = HalfAdder(1, 1);
    std::cout << "Sum: " << static_cast<int>(sum) 
             << ", Carry: " << static_cast<int>(carry) << "\\n\\n";
    
    std::cout << "Full Adder (1 + 1 + 1):\\n";
    auto [sum2, carry2] = FullAdder(1, 1, 1);
    std::cout << "Sum: " << static_cast<int>(sum2) 
             << ", Carry: " << static_cast<int>(carry2) << "\\n";
}

void test_fold_expressions() {
    std::cout << "\\nC++17 Fold Expressions\\n";
    std::cout << "======================\\n\\n";
    
    std::cout << "Multi-AND(1, 1, 1, 1): " << static_cast<int>(multi_and(1, 1, 1, 1)) << "\\n";
    std::cout << "Multi-AND(1, 1, 0, 1): " << static_cast<int>(multi_and(1, 1, 0, 1)) << "\\n";
    std::cout << "Multi-OR(0, 0, 0, 1): " << static_cast<int>(multi_or(0, 0, 0, 1)) << "\\n";
}

int main() {
    std::cout << "Logic Gates Library - C++17 Implementation\\n";
    std::cout << "==========================================\\n";
    
    print_truth_table();
    test_compound_gates();
    test_alu();
    test_fold_expressions();
    
    return 0;
}
"""

# ============================================================================
# ASSEMBLY CODE GENERATOR (8-bit)
# ============================================================================

class ASM8BitCodeGenerator:
    """Generates 8-bit assembly code"""
    
    @staticmethod
    def generate_logic_gates_asm() -> str:
        """Generate assembly for logic gates"""
        return """; ============================================================================
; Logic Gates - 8-bit Assembly Implementation
; Implements all basic logic gates and operations
; ============================================================================

; Data section
.data
    result db 0                ; Result storage
    operand_a db 0             ; First operand
    operand_b db 0             ; Second operand

; ============================================================================
; Basic Logic Gates
; ============================================================================

; AND gate
; Input: A register (operand1), B register (operand2)
; Output: A register
AND_GATE:
    LDA operand_a              ; Load first operand
    LDB operand_b              ; Load second operand
    AND                        ; Perform AND operation
    STA result                 ; Store result
    RET

; OR gate
; Input: A register (operand1), B register (operand2)
; Output: A register
OR_GATE:
    LDA operand_a              ; Load first operand
    LDB operand_b              ; Load second operand
    OR                         ; Perform OR operation
    STA result                 ; Store result
    RET

; XOR gate
; Input: A register (operand1), B register (operand2)
; Output: A register
XOR_GATE:
    LDA operand_a              ; Load first operand
    LDB operand_b              ; Load second operand
    XOR                        ; Perform XOR operation
    STA result                 ; Store result
    RET

; NOT gate
; Input: A register
; Output: A register
NOT_GATE:
    LDA operand_a              ; Load operand
    NOT                        ; Perform NOT operation
    STA result                 ; Store result
    RET

; ============================================================================
; Compound Operations
; ============================================================================

; Half Adder
; Input: operand_a, operand_b
; Output: result (sum), carry flag
HALF_ADDER:
    LDA operand_a              ; Load first operand
    LDB operand_b              ; Load second operand
    
    ; Calculate sum (XOR)
    XOR                        ; A = A XOR B
    PUSH                       ; Save sum on stack
    
    ; Calculate carry (AND)
    LDA operand_a              ; Reload first operand
    LDB operand_b              ; Reload second operand
    AND                        ; A = A AND B (carry)
    STA 0xF0                   ; Store carry at 0xF0
    
    POP                        ; Restore sum
    STA result                 ; Store sum
    RET

; Full Adder
; Input: operand_a, operand_b, carry_in (at 0xF1)
; Output: result (sum), carry_out (at 0xF0)
FULL_ADDER:
    ; First half adder
    LDA operand_a
    LDB operand_b
    XOR                        ; sum1 = a XOR b
    PUSH                       ; Save sum1
    
    LDA operand_a
    LDB operand_b
    AND                        ; carry1 = a AND b
    STA 0xF2                   ; Store carry1
    
    ; Second half adder
    POP                        ; Get sum1
    LDB 0xF1                   ; Load carry_in
    XOR                        ; sum = sum1 XOR carry_in
    STA result                  ; Store final sum
    PUSH                       ; Save for later
    
    POP                        ; Reload sum1
    LDB 0xF1                   ; Load carry_in
    AND                        ; carry2 = sum1 AND carry_in
    
    ; carry_out = carry1 OR carry2
    LDB 0xF2                   ; Load carry1
    OR                         ; A = carry2 OR carry1
    STA 0xF0                   ; Store carry_out
    RET

; ============================================================================
; 8-bit Addition
; ============================================================================

ADD_8BIT:
    LDA operand_a              ; Load first number
    LDB operand_b              ; Load second number
    ADD                        ; Add
    STA result                 ; Store result
    RET

; ============================================================================
; 8-bit Subtraction
; ============================================================================

SUB_8BIT:
    LDA operand_a              ; Load first number
    LDB operand_b              ; Load second number
    SUB                        ; Subtract
    STA result                 ; Store result
    RET

; ============================================================================
; Bitwise Operations
; ============================================================================

BITWISE_AND:
    LDA operand_a
    LDB operand_b
    AND
    STA result
    RET

BITWISE_OR:
    LDA operand_a
    LDB operand_b
    OR
    STA result
    RET

BITWISE_XOR:
    LDA operand_a
    LDB operand_b
    XOR
    STA result
    RET

BITWISE_NOT:
    LDA operand_a
    NOT
    STA result
    RET

; ============================================================================
; Main Program - Test Logic Gates
; ============================================================================

MAIN:
    ; Test AND gate
    LDA 0x0F                   ; Load 00001111
    STA operand_a
    LDA 0xF0                   ; Load 11110000
    STA operand_b
    CALL AND_GATE              ; Result: 00000000
    
    ; Test OR gate
    LDA 0x0F
    STA operand_a
    LDA 0xF0
    STA operand_b
    CALL OR_GATE               ; Result: 11111111
    
    ; Test XOR gate
    LDA 0xAA                   ; Load 10101010
    STA operand_a
    LDA 0x55                   ; Load 01010101
    STA operand_b
    CALL XOR_GATE              ; Result: 11111111
    
    ; Test addition
    LDA 25                     ; Load 25
    STA operand_a
    LDA 17                     ; Load 17
    STA operand_b
    CALL ADD_8BIT              ; Result: 42
    
    HLT                        ; Halt program

; End of program
"""

# ============================================================================
# CODE GENERATOR MANAGER
# ============================================================================

class CodeGeneratorManager:
    """Manages code generation for all languages"""
    
    def __init__(self):
        self.c_gen = CCodeGenerator()
        self.cpp17_gen = CPP17CodeGenerator()
        self.asm_gen = ASM8BitCodeGenerator()
    
    def generate_all(self, output_dir: str = "."):
        """Generate code in all languages"""
        files_generated = []
        
        # C code
        c_header = self.c_gen.generate_header()
        c_impl = self.c_gen.generate_implementation()
        
        # C++ code
        cpp_header = self.cpp17_gen.generate_header()
        cpp_impl = self.cpp17_gen.generate_implementation()
        
        # Assembly code
        asm_code = self.asm_gen.generate_logic_gates_asm()
        
        return {
            'c_header': c_header,
            'c_implementation': c_impl,
            'cpp17_header': cpp_header,
            'cpp17_implementation': cpp_impl,
            'asm_8bit': asm_code
        }

# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_code_generation():
    """Demonstrate code generation"""
    
    print("=" * 70)
    print("CODE GENERATOR - C, C++17, AND ASSEMBLY")
    print("=" * 70)
    
    manager = CodeGeneratorManager()
    generated = manager.generate_all()
    
    print("\nGenerated files:")
    print("-" * 70)
    
    for lang, code in generated.items():
        lines = code.split('\n')
        print(f"\n{lang.upper()}: {len(lines)} lines generated")
        print(f"First 20 lines preview:")
        print("-" * 70)
        for line in lines[:20]:
            print(line)
        print("...")

if __name__ == "__main__":
    demonstrate_code_generation()
