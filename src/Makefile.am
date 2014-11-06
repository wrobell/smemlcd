lib_LTLIBRARIES = libsmemlcd.la

libsmemlcd_la_SOURCES = smemlcd.c
libsmemlcd_la_LDFLAGS = -version-info 0:0:0
include_HEADERS = smemlcd.h

AM_CPPFLAGS=-DBOARD="\"@BOARD@-gpio.c\""

EXTRA_DIST = at91-gpio.c rpi-gpio.c
