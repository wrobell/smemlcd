#
# smemlcd - Sharp Memory LCDs library
#
# Copyright (C) 2014 by Artur Wroblewski <wrobell@pld-linux.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Sharp Memory LCDs library.
"""

import asyncio
import signal

from _smemlcd import ffi, lib

class SMemLCD(object):
    """
    Sharp Memory LCDs display class.

    Use `width` equal to 52 and reversed set to true for Cairo. Use
    `width` equal to 50 and reversed set to false for PIL.

    :var width: Width of buffer line in bytes.
    :var reversed: Reverse order of buffer byte.
    """
    def __init__(self, f_dev, loop=None):
        """
        Create Sharp Memory LCD display instance.

        :param f_dev: SPI device filename, i.e. /dev/spi.
        :param loop: Asyncio loop instance.
        """
        lib.smemlcd_init(f_dev.encode())
        if loop:
            loop.add_signal_handler(signal.SIGUSR1, self._write_async_end)
        self._loop = loop
        self._future = None

        self.width = 52
        self.reversed = True

    def write(self, data):
        """
        Write data to Sharp Memory LCD.

        :param data: Screen buffer data.
        """
        r = lib.smemlcd_write(ffi.from_buffer(data), self.width, self.reversed)
        if r != 0:
            raise SMemLCDError('Write error')

    async def write_async(self, data):
        """
        Write data to Sharp Memory LCD.

        The method is a coroutine.

        :param data: Screen buffer data.
        """
        if self._future:
            raise SMemLCDError('Asynchronous call in progress')

        self._future = self._loop.create_future()
        r = lib.smemlcd_write_async(ffi.from_buffer(data), self.width, self.reversed)
        if r != 0:
            raise SMemLCDError('Asynchronous write cannot be started')
        await self._future

    def _write_async_end(self):
        """
        Finish asynchronous write call to Sharp Memory LCD.
        """
        r = lib.smemlcd_write_async_end()
        if r == 0:
            self._future.set_result(None)
            self._future = None
        else:
            self._future.set_exception(SMemLCDError('Asynchronous write error'))

    def close(self):
        """
        Release resources hold by Sharp Memory LCD.
        """
        lib.smemlcd_close()
        if self._loop:
            self._loop.remove_signal_handler(signal.SIGUSR1)
        if self._future and not self._future.done():
            self._future.set_exception(asyncio.CancelledError('Display closed'))


class SMemLCDError(Exception):
    """
    Raised when accessing Sharp Memory LCD fails.

    At the moment raised only when asynchronous call is in progress.
    """


# vim: sw=4:et:ai
