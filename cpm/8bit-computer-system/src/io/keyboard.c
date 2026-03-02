/*
 * Keyboard Implementation
 * Simple ring buffer keyboard input
 */

#include <stdio.h>
#include <string.h>
#include "io.h"

void kbd_init(Keyboard *kbd) {
    memset(kbd, 0, sizeof(Keyboard));
    kbd->read_pos = 0;
    kbd->write_pos = 0;
    kbd->key_available = false;
}

void kbd_put_key(Keyboard *kbd, uint8_t key) {
    kbd->buffer[kbd->write_pos] = key;
    kbd->write_pos = (kbd->write_pos + 1) % KBD_BUFFER_SIZE;
    kbd->key_available = true;
}

uint8_t kbd_get_key(Keyboard *kbd) {
    if (!kbd_key_available(kbd)) {
        return 0;
    }
    
    uint8_t key = kbd->buffer[kbd->read_pos];
    kbd->read_pos = (kbd->read_pos + 1) % KBD_BUFFER_SIZE;
    
    if (kbd->read_pos == kbd->write_pos) {
        kbd->key_available = false;
    }
    
    return key;
}

bool kbd_key_available(Keyboard *kbd) {
    return kbd->read_pos != kbd->write_pos;
}

void kbd_clear(Keyboard *kbd) {
    kbd->read_pos = 0;
    kbd->write_pos = 0;
    kbd->key_available = false;
}
