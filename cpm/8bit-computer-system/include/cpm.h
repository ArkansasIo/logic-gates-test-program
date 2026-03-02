/*
 * CP/M Compatibility Layer Header
 * Provides CP/M 2.2 BDOS and BIOS emulation
 */

#ifndef CPM_H
#define CPM_H

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

/* CP/M memory layout */
#define CPM_BASE        0x0000
#define CPM_BDOS        0xDC00  /* BDOS entry point */
#define CPM_BIOS        0xE400  /* BIOS entry point */
#define CPM_TPA_START   0x0100  /* Transient Program Area */
#define CPM_TPA_SIZE    0xDB00  /* ~56KB for programs */

/* CP/M BDOS function numbers */
#define CPM_BOOT        0       /* System boot */
#define CPM_CONIN       1       /* Console input */
#define CPM_CONOUT      2       /* Console output */
#define CPM_READER      3       /* Reader input */
#define CPM_PUNCH       4       /* Punch output */
#define CPM_LIST        5       /* List output */
#define CPM_CONIO       6       /* Direct console I/O */
#define CPM_GETIOB      7       /* Get I/O byte */
#define CPM_SETIOB      8       /* Set I/O byte */
#define CPM_PRTSTR      9       /* Print string */
#define CPM_RDBUF       10      /* Read console buffer */
#define CPM_CONST       11      /* Get console status */
#define CPM_VERSION     12      /* Get version number */
#define CPM_RESETDSK    13      /* Reset disk system */
#define CPM_SELDSK      14      /* Select disk */
#define CPM_OPEN        15      /* Open file */
#define CPM_CLOSE       16      /* Close file */
#define CPM_SRCHF       17      /* Search for first */
#define CPM_SRCHN       18      /* Search for next */
#define CPM_DELETE      19      /* Delete file */
#define CPM_READ        20      /* Read sequential */
#define CPM_WRITE       21      /* Write sequential */
#define CPM_MAKE        22      /* Make file */
#define CPM_RENAME      23      /* Rename file */
#define CPM_LOGINVEC    24      /* Get login vector */
#define CPM_CURRDISK    25      /* Get current disk */
#define CPM_SETDMA      26      /* Set DMA address */
#define CPM_GETALOC     27      /* Get allocation vector */
#define CPM_WRTPROT     28      /* Write protect disk */
#define CPM_RDOVEC      29      /* Get read-only vector */
#define CPM_SETATTR     30      /* Set file attributes */
#define CPM_GETDPB      31      /* Get disk parameter block */
#define CPM_USERCODE    32      /* Get/Set user code */
#define CPM_RDRANDOM    33      /* Read random */
#define CPM_WTRANDOM    34      /* Write random */
#define CPM_FILESIZE    35      /* Compute file size */
#define CPM_SETRANDOM   36      /* Set random record */

/* CP/M FCB (File Control Block) */
typedef struct {
    uint8_t drive;              /* Drive (0=default, 1=A, 2=B, etc.) */
    char name[8];               /* Filename */
    char ext[3];                /* Extension */
    uint8_t extent;             /* Extent number */
    uint8_t s1;                 /* Reserved */
    uint8_t s2;                 /* Reserved */
    uint8_t record_count;       /* Records in current extent */
    uint8_t reserved[16];       /* Disk map */
    uint8_t current_record;     /* Current record */
    uint8_t random[3];          /* Random access record number */
} CPM_FCB;

/* CP/M Disk Parameter Block */
typedef struct {
    uint16_t sectors_per_track;
    uint8_t block_shift;
    uint8_t block_mask;
    uint8_t extent_mask;
    uint16_t max_blocks;
    uint16_t dir_entries;
    uint8_t alloc0;
    uint8_t alloc1;
    uint16_t checksum_size;
    uint16_t reserved_tracks;
} CPM_DPB;

/* CP/M state */
typedef struct {
    bool enabled;
    uint8_t current_drive;
    uint16_t dma_address;       /* DMA address for disk I/O */
    uint8_t user_code;
    char disk_images[16][256];  /* Paths to disk images */
    FILE *disk_files[16];       /* Open disk file handles */
    CPM_FCB fcb_table[16];      /* Open file table */
} CPM_State;

/* Global CP/M instance */
extern CPM_State cpm_state;

/* CP/M functions */
void cpm_init(CPM_State *cpm);
void cpm_reset(CPM_State *cpm);
void cpm_boot(CPM_State *cpm);
bool cpm_load_program(CPM_State *cpm, const char *filename);
void cpm_mount_disk(CPM_State *cpm, uint8_t drive, const char *image_path);

/* BDOS call handler */
uint8_t cpm_bdos_call(CPM_State *cpm, uint8_t function, uint16_t param);

/* Console I/O */
uint8_t cpm_conin(void);
void cpm_conout(uint8_t c);
uint8_t cpm_const(void);
void cpm_prtstr(uint16_t addr);

/* File I/O */
uint8_t cpm_open_file(CPM_FCB *fcb);
uint8_t cpm_close_file(CPM_FCB *fcb);
uint8_t cpm_read_seq(CPM_FCB *fcb);
uint8_t cpm_write_seq(CPM_FCB *fcb);
uint8_t cpm_make_file(CPM_FCB *fcb);
uint8_t cpm_delete_file(CPM_FCB *fcb);

/* Disk operations */
void cpm_select_disk(uint8_t drive);
void cpm_set_dma(uint16_t address);
void cpm_read_sector(uint8_t drive, uint16_t track, uint16_t sector);
void cpm_write_sector(uint8_t drive, uint16_t track, uint16_t sector);

#endif /* CPM_H */
