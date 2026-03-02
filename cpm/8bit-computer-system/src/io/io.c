/*
 * I/O System Implementation
 * Main I/O dispatcher and port management
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "io.h"
#include "gpu.h"

/* Global I/O device instances */
Keyboard keyboard;
SerialPort serial;
CMOS cmos;

void io_init(void) {
    kbd_init(&keyboard);
    serial_init(&serial);
    cmos_init(&cmos);
    printf("I/O system initialized\n");
}

void io_reset(void) {
    kbd_clear(&keyboard);
    serial_init(&serial);
    cmos_reset(&cmos);
}

void io_update(void) {
    /* Update CMOS RTC periodically */
    static uint64_t last_update = 0;
    static uint64_t update_counter = 0;
    
    update_counter++;
    if (update_counter - last_update >= 1000) {
        cmos_update_rtc(&cmos);
        last_update = update_counter;
    }
}

uint8_t io_read(uint8_t port) {
    /* GPU ports */
    if (port >= IO_GPU_START && port <= IO_GPU_END) {
        return gpu_io_read(port);
    }
    /* Keyboard ports */
    else if (port >= IO_KBD_START && port <= IO_KBD_END) {
        if (port == KBD_DATA) {
            return kbd_get_key(&keyboard);
        } else if (port == KBD_STATUS) {
            return kbd_key_available(&keyboard) ? 0x01 : 0x00;
        }
    }
    /* Serial ports */
    else if (port >= IO_SERIAL_START && port <= IO_SERIAL_END) {
        if (port == SERIAL_DATA) {
            return serial_read_data(&serial);
        } else if (port == SERIAL_STATUS) {
            return serial.status;
        } else if (port == SERIAL_CONTROL) {
            return serial.control;
        }
    }
    /* CMOS ports */
    else if (port >= IO_CMOS_START && port <= IO_CMOS_END) {
        if (port == CMOS_DATA) {
            return cmos_read(&cmos, cmos.address);
        } else if (port == CMOS_ADDR) {
            return cmos.address;
        }
    }
    
    return 0xFF;  /* Return 0xFF for unimplemented ports */
}

void io_write(uint8_t port, uint8_t value) {
    /* GPU ports */
    if (port >= IO_GPU_START && port <= IO_GPU_END) {
        gpu_io_write(port, value);
    }
    /* Keyboard ports */
    else if (port >= IO_KBD_START && port <= IO_KBD_END) {
        if (port == KBD_DATA) {
            kbd_put_key(&keyboard, value);
        }
    }
    /* Serial ports */
    else if (port >= IO_SERIAL_START && port <= IO_SERIAL_END) {
        if (port == SERIAL_DATA) {
            serial_write_data(&serial, value);
        } else if (port == SERIAL_STATUS) {
            serial.status = value;
        } else if (port == SERIAL_CONTROL) {
            serial.control = value;
        }
    }
    /* CMOS ports */
    else if (port >= IO_CMOS_START && port <= IO_CMOS_END) {
        if (port == CMOS_ADDR) {
            cmos.address = value & 0x7F;
        } else if (port == CMOS_DATA) {
            cmos_write(&cmos, cmos.address, value);
        }
    }
}
