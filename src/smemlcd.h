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

#if !defined (_SMEMLCD_H_)
#define _SMEMLCD_H_

/*!
 * Initialize LCD screen.
 *
 * \param f_dev SPI device filename, i.e. /dev/spi.
 */
int smemlcd_init(const char *f_dev);

/*!
 * Clear LCD screen.
 */
int smemlcd_clear(void);

/*!
 * Write data to LCD screen.
 */
int smemlcd_write(uint8_t*, uint8_t, uint8_t);

/*!
 * Write data to LCD screen in asynchronous way.
 *
 * Use `smemlcd_write_async_end` to finish the call.
 */
int smemlcd_write_async(uint8_t *data, uint8_t, uint8_t);

/*!
 * Finish asynchronous write to LCD screen.
 */
int smemlcd_write_async_end(void);

/*!
 * Close open resources claimed by LCD screen.
 */
int smemlcd_close(void);

#endif /* _SMEMLCD_H_ */

/*
 * vim: sw=4:et:ai
 */
