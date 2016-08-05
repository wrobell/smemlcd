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

    def write(self, data):
        """
        Write data to Sharp Memory LCD.

        :param data: Screen data to display.
        """
        n = len(data)
        assert n == 12000
        lib.smemlcd_write(data)

    async def write_async(self, data):
        """
        Write data to Sharp Memory LCD in asynchronous manner.

        :param data: Screen data to display.
        """
        n = len(data)
        assert n == 12000

        self._future = asyncio.Future(loop=self._loop)
        lib.smemlcd_write_async(data)
        await self._future

    def _write_async_end(self):
        """
        Finish asynchronous write call to Sharp Memory LCD.
        """
        lib.smemlcd_write_async_end()
        self._future.set_result(None)
        self._future = None

    def close(self):
        if self._loop:
            self._loop.remove_signal_handler(signal.SIGUSR1)
        lib.smemlcd_close()


# vim: sw=4:et:ai
