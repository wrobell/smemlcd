/*
 * smemlcd - Sharp Memory LCDs library
 *
 * Copyright (C) 2014 by Artur Wroblewski <wrobell@pld-linux.org>
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

/*
 * based on http://elinux.org/RPi_Low-level_peripherals#C_2
 */

#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define BCM2708_PERI_BASE 0x20000000
#define GPIO_BASE (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */

#define PAGE_SIZE (4 * 1024)
#define BLOCK_SIZE (4 * 1024)

static volatile unsigned *gpio;

/* GPIO setup macros. Always use GPIO_IN before using GPIO_OUT. */
#define GPIO_IN(pin) *(gpio + ((pin) / 10)) &= ~(7 << (((pin) % 10) * 3))
#define GPIO_OUT(pin) *(gpio + ((pin) / 10)) |=  (1 << (((pin) % 10) * 3))

#define GPIO_SET(pin) *(gpio + 7) = 1 << pin
#define GPIO_CLR(pin) *(gpio + 10) = 1 << pin

int gpio_init() {
    int mem_fd;
    void *gpio_map;

    if ((mem_fd = open("/dev/mem", O_RDWR | O_SYNC)) < 0) {
        fprintf(stderr, "Cannot open /dev/mem\n");
        return -1;
    }

    gpio_map = mmap(
        NULL, BLOCK_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, mem_fd, GPIO_BASE
    );

    close(mem_fd);

    if (gpio_map == MAP_FAILED) {
        fprintf(stderr, "mmap error %d\n", (int) gpio_map);
        return -1;
    }

    gpio = (volatile unsigned *) gpio_map;
    return 0;
}

/*
 * vim: sw=4:et:ai
 */
