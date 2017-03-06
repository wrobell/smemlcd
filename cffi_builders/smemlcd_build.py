#
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

import cffi

ffi = cffi.FFI()
ffi.cdef("""
int smemlcd_init(const char *);
int smemlcd_write(uint8_t *);
int smemlcd_write_async(uint8_t *);
int smemlcd_write_async_end(void);
int smemlcd_clear(void);
int smemlcd_close(void);
""")

ffi.set_source('_smemlcd', """
#include <smemlcd.h>
""", libraries=['smemlcd'], library_dirs=['src/.libs'], include_dirs=['src'])

# vim: sw=4:et:ai

