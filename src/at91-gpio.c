/*
 * smemlcd - Sharp Memory LCDs library
 *
 * Copyright (C) 2014-2017 by Artur Wroblewski <wrobell@riseup.net>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define BLOCK_SIZE 4096UL
#define MAP_MASK (BLOCK_SIZE - 1)
#define GPIO_A_BASE 0xfffff400

static void *PIO_PER;   /* 0x0000 */
static void *PIO_OER;   /* 0x0010 */
static void *PIO_SODR;  /* 0x0030 */
static void *PIO_CODR;  /* 0x0034 */

#define GPIO_IN(pin) *(unsigned int *) PIO_PER = 1 << pin
#define GPIO_OUT(pin) *(unsigned int *) PIO_OER = 1 << pin

#define GPIO_SET(pin) *(unsigned int *) PIO_SODR = 1 << pin
#define GPIO_CLR(pin) *(unsigned int *) PIO_CODR = 1 << pin

int gpio_init() {
    int mem_fd;
    void *gpio_map;

    if ((mem_fd = open("/dev/mem", O_RDWR | O_SYNC)) < 0) {
        fprintf(stderr, "Cannot open /dev/mem\n");
        return -1;
    }

    gpio_map = mmap(
        0, BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, mem_fd,
        GPIO_A_BASE & ~MAP_MASK
    );

    close(mem_fd);

    if (gpio_map == MAP_FAILED) {
        fprintf(stderr, "mmap error %d\n", gpio_map);
        return -1;
    }

    PIO_PER = gpio_map + (GPIO_A_BASE & MAP_MASK);
    PIO_OER = gpio_map + ((GPIO_A_BASE + 0x10) & MAP_MASK);
    PIO_SODR = gpio_map + ((GPIO_A_BASE + 0x30) & MAP_MASK);
    PIO_CODR = gpio_map + ((GPIO_A_BASE + 0x34) & MAP_MASK);

    return 0;
}

/*
 * vim: sw=4:et:ai
 */ 
