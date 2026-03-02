# Build script for Windows (PowerShell)
# 8-Bit Computer System

Write-Host "8-Bit Computer System - Build Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Create directories
$dirs = @("build\cpu", "build\memory", "build\gpu", "build\io", "build\cpm", "bin")
foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
    }
}

# Compiler settings
$CC = "gcc"
$CFLAGS = "-Wall -Wextra -O2 -Iinclude"

# Build emulator
Write-Host "Building emulator..." -ForegroundColor Yellow
$sources = @(
    "src\main.c",
    "src\cpu\z80.c",
    "src\memory\ram.c",
    "src\gpu\gpu.c",
    "src\io\io.c",
    "src\io\keyboard.c",
    "src\io\serial.c",
    "src\io\cmos.c",
    "src\cpm\cpm.c"
)

$cmd = "$CC $CFLAGS -o bin\emulator.exe " + ($sources -join " ")
Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Emulator built successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Emulator build failed!" -ForegroundColor Red
    exit 1
}

# Build assembler
Write-Host "Building assembler..." -ForegroundColor Yellow
$cmd = "$CC $CFLAGS -o bin\assembler.exe asm\assembler.c"
Invoke-Expression $cmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Assembler built successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Assembler build failed!" -ForegroundColor Red
    exit 1
}

# Assemble BIOS
Write-Host "Assembling BIOS..." -ForegroundColor Yellow
& "bin\assembler.exe" "bios\bios.asm" "-o" "bios\bios.bin"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ BIOS assembled!" -ForegroundColor Green
}

# Assemble OS kernel
Write-Host "Assembling OS kernel..." -ForegroundColor Yellow
& "bin\assembler.exe" "os\kernel.asm" "-o" "os\kernel.bin"
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ OS kernel assembled!" -ForegroundColor Green
}

# Assemble examples
Write-Host "Assembling examples..." -ForegroundColor Yellow
& "bin\assembler.exe" "examples\hello\hello.asm" "-o" "examples\hello\hello.bin"
& "bin\assembler.exe" "examples\graphics\demo.asm" "-o" "examples\graphics\demo.bin"
Write-Host "✓ Examples assembled!" -ForegroundColor Green

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the emulator:" -ForegroundColor Cyan
Write-Host "  .\bin\emulator.exe" -ForegroundColor White
Write-Host "  .\bin\emulator.exe examples\hello\hello.bin" -ForegroundColor White
Write-Host "  .\bin\emulator.exe --debug" -ForegroundColor White
