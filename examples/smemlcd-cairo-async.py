#
# smemlcd - Sharp Memory LCDs library
#
# Copyright (C) 2014-2017 by Artur Wroblewski <wrobell@riseup.net>
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

import argparse
import asyncio
import math
import time

from smemlcd import SMemLCD
import cairocffi as cairo

parser = argparse.ArgumentParser(description='smemlcd library asyncio example')
parser.add_argument(
    '-p', dest='policy', choices=('default', 'uv'), nargs=1,
    help='TrueType font filename'
)
parser.add_argument('-f', dest='font', default='profont', nargs=1, help='font name')
parser.add_argument('device', help='SPI device filename, i.e. /dev/spi')
args = parser.parse_args()

WIDTH, HEIGHT = 400, 240

def center(cr, y, txt):
    w, h = cr.text_extents(txt)[2:4]
    x = int((WIDTH - w) / 2)
    cr.move_to(x, y)
    cr.show_text(txt)

if args.policy == 'uv':
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

img_data = bytearray(12480)
surface = cairo.ImageSurface.create_for_data(
    img_data, cairo.FORMAT_A1, 400, 240
)
cr = cairo.Context(surface)

# sizes for profont: 10, 11, 12, 15, 17, 22, 29
cr.select_font_face(args.font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
cr.set_font_size(29)

async def run(lcd):
    for i in range(60, -1, -1):
        start = time.monotonic()
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        center(cr, 60, 'smemlcd library demo')

        s = 'closing in {:02d}...'.format(i)
        center(cr, 100, s)

        cr.rectangle(5, 120, 390, 20)
        cr.stroke()
        cr.rectangle(6, 121, 388 * (60 - i) / 60, 18)
        cr.fill()

        sw = time.monotonic()
        await lcd.write_async(img_data)
        end = time.monotonic()
        print('time: process={:.4f}, write={:.4f}'.format(end - start, end - sw))

        await asyncio.sleep(0.2)


loop = asyncio.get_event_loop()

lcd = SMemLCD(args.device, loop=loop)
try:
    loop.run_until_complete(run(lcd))
finally:
    loop.close()
    lcd.close()

# vim: sw=4:et:ai
