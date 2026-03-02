# Makefile for 8-Bit Computer System

CC = gcc
CFLAGS = -Wall -Wextra -O2 -Iinclude
LDFLAGS = -lm

# Directories
SRC_DIR = src
INC_DIR = include
BUILD_DIR = build
BIN_DIR = bin

# Source files
CPU_SRC = $(SRC_DIR)/cpu/z80.c
MEM_SRC = $(SRC_DIR)/memory/ram.c
GPU_SRC = $(SRC_DIR)/gpu/gpu.c
IO_SRC = $(SRC_DIR)/io/io.c $(SRC_DIR)/io/keyboard.c $(SRC_DIR)/io/serial.c $(SRC_DIR)/io/cmos.c
CPM_SRC = $(SRC_DIR)/cpm/cpm.c
MAIN_SRC = $(SRC_DIR)/main.c

ALL_SRC = $(MAIN_SRC) $(CPU_SRC) $(MEM_SRC) $(GPU_SRC) $(IO_SRC) $(CPM_SRC)

# Object files
OBJS = $(ALL_SRC:$(SRC_DIR)/%.c=$(BUILD_DIR)/%.o)

# Assembler
ASM_SRC = asm/assembler.c
ASM_BIN = $(BIN_DIR)/assembler

# Target executables
EMULATOR = $(BIN_DIR)/emulator

# BIOS and OS
BIOS_ASM = bios/bios.asm
BIOS_BIN = bios/bios.bin
OS_ASM = os/kernel.asm
OS_BIN = os/kernel.bin

# Examples
HELLO_ASM = examples/hello/hello.asm
HELLO_BIN = examples/hello/hello.bin
DEMO_ASM = examples/graphics/demo.asm
DEMO_BIN = examples/graphics/demo.bin

.PHONY: all clean emulator assembler bios os examples directories

all: directories emulator assembler bios os examples

directories:
	@mkdir -p $(BUILD_DIR)/cpu $(BUILD_DIR)/memory $(BUILD_DIR)/gpu $(BUILD_DIR)/io $(BUILD_DIR)/cpm
	@mkdir -p $(BIN_DIR)

# Build emulator
emulator: directories $(EMULATOR)

$(EMULATOR): $(ALL_SRC)
	$(CC) $(CFLAGS) -o $@ $(ALL_SRC) $(LDFLAGS)
	@echo "Emulator built successfully!"

# Build assembler
assembler: directories $(ASM_BIN)

$(ASM_BIN): $(ASM_SRC)
	$(CC) $(CFLAGS) -o $@ $(ASM_SRC)
	@echo "Assembler built successfully!"

# Build BIOS
bios: $(ASM_BIN) $(BIOS_BIN)

$(BIOS_BIN): $(BIOS_ASM)
	$(ASM_BIN) $(BIOS_ASM) -o $(BIOS_BIN)
	@echo "BIOS assembled successfully!"

# Build OS
os: $(ASM_BIN) $(OS_BIN)

$(OS_BIN): $(OS_ASM)
	$(ASM_BIN) $(OS_ASM) -o $(OS_BIN)
	@echo "OS kernel assembled successfully!"

# Build examples
examples: $(ASM_BIN) $(HELLO_BIN) $(DEMO_BIN)

$(HELLO_BIN): $(HELLO_ASM)
	$(ASM_BIN) $(HELLO_ASM) -o $(HELLO_BIN)
	@echo "Hello World example assembled!"

$(DEMO_BIN): $(DEMO_ASM)
	$(ASM_BIN) $(DEMO_ASM) -o $(DEMO_BIN)
	@echo "Graphics demo assembled!"

# Run emulator
run: all
	$(EMULATOR)

run-hello: all
	$(EMULATOR) $(HELLO_BIN)

run-demo: all
	$(EMULATOR) $(DEMO_BIN)

# Debug mode
debug: all
	$(EMULATOR) --debug

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR) $(BIN_DIR)
	rm -f $(BIOS_BIN) $(OS_BIN) $(HELLO_BIN) $(DEMO_BIN)
	@echo "Clean complete!"

# Help
help:
	@echo "8-Bit Computer System - Build System"
	@echo ""
	@echo "Available targets:"
	@echo "  all        - Build everything"
	@echo "  emulator   - Build the emulator only"
	@echo "  assembler  - Build the assembler only"
	@echo "  bios       - Assemble the BIOS"
	@echo "  os         - Assemble the OS kernel"
	@echo "  examples   - Assemble example programs"
	@echo "  run        - Build and run emulator"
	@echo "  run-hello  - Build and run Hello World example"
	@echo "  run-demo   - Build and run graphics demo"
	@echo "  debug      - Run emulator in debug mode"
	@echo "  clean      - Remove all build artifacts"
	@echo "  help       - Show this help message"
