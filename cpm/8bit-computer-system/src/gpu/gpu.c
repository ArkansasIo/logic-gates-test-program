/*
 * GPU - Graphics Processing Unit Implementation
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "gpu.h"
#include "memory.h"

GPU gpu;

/* 8x8 font data (ASCII 32-127) - simplified */
static const uint8_t font_data[96][8] __attribute__((unused)) = {
    /* Space through ~ */
    {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00}, /* Space */
    {0x18,0x3C,0x3C,0x18,0x18,0x00,0x18,0x00}, /* ! */
    {0x36,0x36,0x00,0x00,0x00,0x00,0x00,0x00}, /* " */
    /* ... rest of font (simplified for brevity) */
};

void gpu_init(GPU *g) {
    memset(g, 0, sizeof(GPU));
    g->enabled = true;
    g->text_mode = true;
    g->control = GPU_CTRL_ENABLE | GPU_CTRL_TEXT_MODE;
    g->current_color = 7;  /* White */
    
    gpu_load_default_palette(g);
    gpu_clear_screen(g, 0);
    gpu_clear_text(g);
    
    printf("GPU initialized: %dx%d, %d colors\n",
           SCREEN_WIDTH, SCREEN_HEIGHT, PALETTE_SIZE);
}

void gpu_reset(GPU *g) {
    g->cursor_x = 0;
    g->cursor_y = 0;
    g->scroll = 0;
    gpu_clear_screen(g, 0);
    gpu_clear_text(g);
}

void gpu_update(GPU *g) {
    if (!g->enabled) return;
    
    /* Update frame counter */
    g->frame_count++;
    
    /* Handle VSync */
    if (g->control & GPU_CTRL_VSYNC) {
        g->status |= 0x01;  /* VSync flag */
    }
}

void gpu_render(GPU *g __attribute__((unused))) {
    /* In a real implementation, this would render to screen */
    /* For now, it's a placeholder */
}

void gpu_set_pixel(GPU *g, uint16_t x, uint16_t y, uint8_t color) {
    if (x >= SCREEN_WIDTH || y >= SCREEN_HEIGHT) return;
    g->framebuffer[y * SCREEN_WIDTH + x] = color;
}

uint8_t gpu_get_pixel(GPU *g, uint16_t x, uint16_t y) {
    if (x >= SCREEN_WIDTH || y >= SCREEN_HEIGHT) return 0;
    return g->framebuffer[y * SCREEN_WIDTH + x];
}

void gpu_clear_screen(GPU *g, uint8_t color) {
    memset(g->framebuffer, color, sizeof(g->framebuffer));
}

void gpu_draw_rect(GPU *g, uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint8_t color) {
    for (uint16_t dy = 0; dy < h; dy++) {
        for (uint16_t dx = 0; dx < w; dx++) {
            gpu_set_pixel(g, x + dx, y + dy, color);
        }
    }
}

void gpu_draw_line(GPU *g, uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint8_t color) {
    /* Bresenham's line algorithm */
    int dx = abs((int)x2 - (int)x1);
    int dy = abs((int)y2 - (int)y1);
    int sx = x1 < x2 ? 1 : -1;
    int sy = y1 < y2 ? 1 : -1;
    int err = dx - dy;
    
    while (1) {
        gpu_set_pixel(g, x1, y1, color);
        
        if (x1 == x2 && y1 == y2) break;
        
        int e2 = 2 * err;
        if (e2 > -dy) {
            err -= dy;
            x1 += sx;
        }
        if (e2 < dx) {
            err += dx;
            y1 += sy;
        }
    }
}

void gpu_put_char(GPU *g, char c) {
    if (!g->text_mode) return;
    
    if (c == '\n') {
        g->cursor_x = 0;
        g->cursor_y++;
        if (g->cursor_y >= TEXT_HEIGHT) {
            gpu_scroll_text(g);
            g->cursor_y = TEXT_HEIGHT - 1;
        }
        return;
    }
    
    if (c == '\r') {
        g->cursor_x = 0;
        return;
    }
    
    if (c == '\b') {
        if (g->cursor_x > 0) g->cursor_x--;
        return;
    }
    
    /* Store character in text buffer */
    int pos = g->cursor_y * TEXT_WIDTH + g->cursor_x;
    g->text_buffer[pos] = c;
    g->text_colors[pos] = g->current_color;
    
    g->cursor_x++;
    if (g->cursor_x >= TEXT_WIDTH) {
        g->cursor_x = 0;
        g->cursor_y++;
        if (g->cursor_y >= TEXT_HEIGHT) {
            gpu_scroll_text(g);
            g->cursor_y = TEXT_HEIGHT - 1;
        }
    }
}

void gpu_print_string(GPU *g, const char *str) {
    while (*str) {
        gpu_put_char(g, *str++);
    }
}

void gpu_set_cursor(GPU *g, uint16_t x, uint16_t y) {
    if (x < TEXT_WIDTH) g->cursor_x = x;
    if (y < TEXT_HEIGHT) g->cursor_y = y;
}

void gpu_clear_text(GPU *g) {
    memset(g->text_buffer, ' ', sizeof(g->text_buffer));
    memset(g->text_colors, 7, sizeof(g->text_colors));
    g->cursor_x = 0;
    g->cursor_y = 0;
}

void gpu_scroll_text(GPU *g) {
    /* Move all lines up by one */
    memmove(g->text_buffer, g->text_buffer + TEXT_WIDTH,
            TEXT_WIDTH * (TEXT_HEIGHT - 1));
    memmove(g->text_colors, g->text_colors + TEXT_WIDTH,
            TEXT_WIDTH * (TEXT_HEIGHT - 1));
    
    /* Clear last line */
    memset(g->text_buffer + TEXT_WIDTH * (TEXT_HEIGHT - 1), ' ', TEXT_WIDTH);
    memset(g->text_colors + TEXT_WIDTH * (TEXT_HEIGHT - 1), 7, TEXT_WIDTH);
}

void gpu_set_palette(GPU *gpu, uint8_t index, uint8_t r, uint8_t g, uint8_t b) {
    gpu->palette[index].r = r;
    gpu->palette[index].g = g;
    gpu->palette[index].b = b;
}

void gpu_load_default_palette(GPU *gpu) {
    /* CGA-inspired palette */
    gpu_set_palette(gpu, 0, 0, 0, 0);         /* Black */
    gpu_set_palette(gpu, 1, 0, 0, 170);       /* Blue */
    gpu_set_palette(gpu, 2, 0, 170, 0);       /* Green */
    gpu_set_palette(gpu, 3, 0, 170, 170);     /* Cyan */
    gpu_set_palette(gpu, 4, 170, 0, 0);       /* Red */
    gpu_set_palette(gpu, 5, 170, 0, 170);     /* Magenta */
    gpu_set_palette(gpu, 6, 170, 85, 0);      /* Brown */
    gpu_set_palette(gpu, 7, 170, 170, 170);   /* Light Gray */
    gpu_set_palette(gpu, 8, 85, 85, 85);      /* Dark Gray */
    gpu_set_palette(gpu, 9, 85, 85, 255);     /* Light Blue */
    gpu_set_palette(gpu, 10, 85, 255, 85);    /* Light Green */
    gpu_set_palette(gpu, 11, 85, 255, 255);   /* Light Cyan */
    gpu_set_palette(gpu, 12, 255, 85, 85);    /* Light Red */
    gpu_set_palette(gpu, 13, 255, 85, 255);   /* Light Magenta */
    gpu_set_palette(gpu, 14, 255, 255, 85);   /* Yellow */
    gpu_set_palette(gpu, 15, 255, 255, 255);  /* White */
    
    /* Fill remaining palette with gradient */
    for (int i = 16; i < 256; i++) {
        gpu_set_palette(gpu, i, i, i, i);
    }
}

void gpu_io_write(uint8_t port, uint8_t value) {
    switch (port) {
        case GPU_CTRL:
            gpu.control = value;
            gpu.enabled = value & GPU_CTRL_ENABLE;
            gpu.text_mode = value & GPU_CTRL_TEXT_MODE;
            break;
            
        case GPU_CURSOR_X:
            gpu.cursor_x = value % TEXT_WIDTH;
            break;
            
        case GPU_CURSOR_Y:
            gpu.cursor_y = value % TEXT_HEIGHT;
            break;
            
        case GPU_COLOR:
            gpu.current_color = value;
            break;
            
        case GPU_PALETTE_IDX:
            gpu.palette_index = value;
            break;
            
        case GPU_PALETTE_R:
            gpu.palette[gpu.palette_index].r = value;
            break;
            
        case GPU_PALETTE_G:
            gpu.palette[gpu.palette_index].g = value;
            break;
            
        case GPU_PALETTE_B:
            gpu.palette[gpu.palette_index].b = value;
            break;
            
        case GPU_CHAR:
            gpu_put_char(&gpu, value);
            break;
            
        case GPU_SCROLL:
            gpu.scroll = value;
            break;
    }
}

uint8_t gpu_io_read(uint8_t port) {
    switch (port) {
        case GPU_CTRL:
            return gpu.control;
            
        case GPU_STATUS:
            return gpu.status;
            
        case GPU_CURSOR_X:
            return gpu.cursor_x;
            
        case GPU_CURSOR_Y:
            return gpu.cursor_y;
            
        case GPU_COLOR:
            return gpu.current_color;
            
        case GPU_PALETTE_IDX:
            return gpu.palette_index;
            
        case GPU_PALETTE_R:
            return gpu.palette[gpu.palette_index].r;
            
        case GPU_PALETTE_G:
            return gpu.palette[gpu.palette_index].g;
            
        case GPU_PALETTE_B:
            return gpu.palette[gpu.palette_index].b;
            
        default:
            return 0;
    }
}
