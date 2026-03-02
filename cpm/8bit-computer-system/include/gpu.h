/*
 * GPU - Graphics Processing Unit
 * Simple 8-bit graphics processor
 */

#ifndef GPU_H
#define GPU_H

#include <stdint.h>
#include <stdbool.h>

/* Display configuration */
#define SCREEN_WIDTH    320
#define SCREEN_HEIGHT   240
#define SCREEN_BPP      8       /* 8 bits per pixel (256 colors) */
#define PALETTE_SIZE    256

/* GPU registers (I/O ports) */
#define GPU_CTRL        0x00    /* Control register */
#define GPU_STATUS      0x01    /* Status register */
#define GPU_CURSOR_X    0x02    /* Cursor X position */
#define GPU_CURSOR_Y    0x03    /* Cursor Y position */
#define GPU_COLOR       0x04    /* Current color */
#define GPU_PALETTE_IDX 0x05    /* Palette index */
#define GPU_PALETTE_R   0x06    /* Palette red component */
#define GPU_PALETTE_G   0x07    /* Palette green component */
#define GPU_PALETTE_B   0x08    /* Palette blue component */
#define GPU_CHAR        0x09    /* Character to draw */
#define GPU_SCROLL      0x0A    /* Scroll register */

/* GPU control bits */
#define GPU_CTRL_ENABLE     0x01    /* Enable display */
#define GPU_CTRL_TEXT_MODE  0x02    /* Text mode (80x30) */
#define GPU_CTRL_GRAPHICS   0x04    /* Graphics mode */
#define GPU_CTRL_CURSOR     0x08    /* Show cursor */
#define GPU_CTRL_VSYNC      0x10    /* VSync enable */

/* Text mode configuration */
#define TEXT_WIDTH      80
#define TEXT_HEIGHT     30
#define FONT_WIDTH      8
#define FONT_HEIGHT     8

/* Color structure */
typedef struct {
    uint8_t r, g, b;
} RGB;

/* GPU state */
typedef struct {
    /* Display buffer */
    uint8_t framebuffer[SCREEN_WIDTH * SCREEN_HEIGHT];
    
    /* Text mode buffer */
    uint8_t text_buffer[TEXT_WIDTH * TEXT_HEIGHT];
    uint8_t text_colors[TEXT_WIDTH * TEXT_HEIGHT];
    
    /* Palette */
    RGB palette[PALETTE_SIZE];
    
    /* Registers */
    uint8_t control;
    uint8_t status;
    uint16_t cursor_x;
    uint16_t cursor_y;
    uint8_t current_color;
    uint8_t palette_index;
    uint8_t scroll;
    
    /* State */
    bool text_mode;
    bool enabled;
    uint64_t frame_count;
} GPU;

/* Global GPU instance */
extern GPU gpu;

/* GPU functions */
void gpu_init(GPU *g);
void gpu_reset(GPU *g);
void gpu_update(GPU *g);
void gpu_render(GPU *g);

/* Drawing functions */
void gpu_set_pixel(GPU *g, uint16_t x, uint16_t y, uint8_t color);
uint8_t gpu_get_pixel(GPU *g, uint16_t x, uint16_t y);
void gpu_clear_screen(GPU *g, uint8_t color);
void gpu_draw_rect(GPU *g, uint16_t x, uint16_t y, uint16_t w, uint16_t h, uint8_t color);
void gpu_draw_line(GPU *g, uint16_t x1, uint16_t y1, uint16_t x2, uint16_t y2, uint8_t color);

/* Text mode functions */
void gpu_put_char(GPU *g, char c);
void gpu_print_string(GPU *g, const char *str);
void gpu_set_cursor(GPU *g, uint16_t x, uint16_t y);
void gpu_clear_text(GPU *g);
void gpu_scroll_text(GPU *g);

/* Palette functions */
void gpu_set_palette(GPU *gpu, uint8_t index, uint8_t r, uint8_t g, uint8_t b);
void gpu_load_default_palette(GPU *gpu);

/* I/O port handlers */
void gpu_io_write(uint8_t port, uint8_t value);
uint8_t gpu_io_read(uint8_t port);

#endif /* GPU_H */
