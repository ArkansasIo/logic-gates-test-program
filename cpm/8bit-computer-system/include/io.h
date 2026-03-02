/*
 * I/O System Header
 * Keyboard, Serial, CMOS, and other I/O devices
 */

#ifndef IO_H
#define IO_H

#include <stdint.h>
#include <stdbool.h>
#include <time.h>

/* I/O Port ranges */
#define IO_GPU_START    0x00
#define IO_GPU_END      0x0F
#define IO_KBD_START    0x10
#define IO_KBD_END      0x1F
#define IO_SERIAL_START 0x20
#define IO_SERIAL_END   0x2F
#define IO_PARALLEL_START 0x30
#define IO_PARALLEL_END 0x3F
#define IO_CMOS_START   0x40
#define IO_CMOS_END     0x4F
#define IO_DISK_START   0x50
#define IO_DISK_END     0x5F

/* Keyboard */
#define KBD_DATA        0x10    /* Keyboard data port */
#define KBD_STATUS      0x11    /* Keyboard status port */
#define KBD_BUFFER_SIZE 16

typedef struct {
    uint8_t buffer[KBD_BUFFER_SIZE];
    uint8_t read_pos;
    uint8_t write_pos;
    bool key_available;
} Keyboard;

/* Serial Port (UART 8250 compatible) */
#define SERIAL_DATA     0x20    /* Data register */
#define SERIAL_STATUS   0x21    /* Status register */
#define SERIAL_CONTROL  0x22    /* Control register */

typedef struct {
    uint8_t data;
    uint8_t status;
    uint8_t control;
    bool tx_ready;
    bool rx_ready;
} SerialPort;

/* CMOS/RTC */
#define CMOS_ADDR       0x40    /* CMOS address register */
#define CMOS_DATA       0x41    /* CMOS data register */
#define CMOS_SIZE       128     /* 128 bytes of CMOS RAM */

/* CMOS Register addresses */
#define CMOS_RTC_SEC    0x00
#define CMOS_RTC_MIN    0x02
#define CMOS_RTC_HOUR   0x04
#define CMOS_RTC_DAY    0x07
#define CMOS_RTC_MONTH  0x08
#define CMOS_RTC_YEAR   0x09
#define CMOS_CONFIG     0x10    /* System configuration */
#define CMOS_BOOTDEV    0x11    /* Boot device */
#define CMOS_MEMSIZE    0x12    /* Memory size */

typedef struct {
    uint8_t ram[CMOS_SIZE];
    uint8_t address;
    time_t last_update;
} CMOS;

/* Global I/O instances */
extern Keyboard keyboard;
extern SerialPort serial;
extern CMOS cmos;

/* I/O System Functions */
void io_init(void);
void io_reset(void);
void io_update(void);

/* Main I/O handlers */
uint8_t io_read(uint8_t port);
void io_write(uint8_t port, uint8_t value);

/* Keyboard functions */
void kbd_init(Keyboard *kbd);
void kbd_put_key(Keyboard *kbd, uint8_t key);
uint8_t kbd_get_key(Keyboard *kbd);
bool kbd_key_available(Keyboard *kbd);
void kbd_clear(Keyboard *kbd);

/* Serial port functions */
void serial_init(SerialPort *sp);
void serial_write_data(SerialPort *sp, uint8_t data);
uint8_t serial_read_data(SerialPort *sp);
void serial_write_char(char c);
void serial_write_string(const char *str);

/* CMOS functions */
void cmos_init(CMOS *cm);
void cmos_reset(CMOS *cm);
void cmos_update_rtc(CMOS *cm);
uint8_t cmos_read(CMOS *cm, uint8_t addr);
void cmos_write(CMOS *cm, uint8_t addr, uint8_t value);
void cmos_save(CMOS *cm, const char *filename);
void cmos_load(CMOS *cm, const char *filename);

/* Helper functions */
uint8_t bcd_to_bin(uint8_t bcd);
uint8_t bin_to_bcd(uint8_t bin);

#endif /* IO_H */
