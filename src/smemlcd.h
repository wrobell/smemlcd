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

#if !defined (_SMEMLCD_H_)
#define _SMEMLCD_H_

/*!
 * Initialize LCD.
 *
 * \param f_dev SPI device filename, i.e. /dev/spi.
 */
int smemlcd_init(const char *f_dev);

/*!
 * Clear LCD.
 */
int smemlcd_clear(void);

/*!
 * Write screen data to LCD.
 */
int smemlcd_write(uint8_t *data);

#endif /* _SMEMLCD_H_ */

/*
 * vim: sw=4:et:ai
 */
