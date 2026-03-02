/*
 * Serial Port Implementation
 * Basic UART-like serial communication
 */

#include <stdio.h>
#include <string.h>
#include "io.h"

void serial_init(SerialPort *sp) {
    memset(sp, 0, sizeof(SerialPort));
    sp->tx_ready = true;
    sp->rx_ready = false;
    sp->status = 0x80;  /* TX ready */
}

void serial_write_data(SerialPort *sp, uint8_t data) {
    sp->data = data;
    sp->tx_ready = false;
    
    /* In a real implementation, this would send data */
    /* For now, just output to console */
    putchar(data);
    fflush(stdout);
    
    sp->tx_ready = true;
    sp->status |= 0x80;  /* TX ready flag */
}

uint8_t serial_read_data(SerialPort *sp) {
    if (!sp->rx_ready) {
        return 0;
    }
    
    uint8_t data = sp->data;
    sp->rx_ready = false;
    sp->status &= ~0x01;  /* Clear RX ready flag */
    
    return data;
}

void serial_write_char(char c) {
    serial_write_data(&serial, (uint8_t)c);
}

void serial_write_string(const char *str) {
    while (*str) {
        serial_write_char(*str++);
    }
}
