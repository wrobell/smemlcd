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

import signal

from _smemlcd import ffi, lib

class SMemLCD(object):
    """
    Sharp Memory LCDs display class.
    """
    def __init__(self, f_dev):
        """
        Create Sharp Memory LCD display instance.

        :param f_dev: SPI device filename, i.e. /dev/spi.
        """
        lib.smemlcd_init(f_dev.encode())


    def write(self, data):
        """
        Write data to Sharp memory LCD.

        :param data: Screen data to display.
        """
        n = len(data)
        assert n == 12000
        lib.smemlcd_write(data)


# vim: sw=4:et:ai
