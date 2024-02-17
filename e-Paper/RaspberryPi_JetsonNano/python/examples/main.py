#
# ZeroWriter
#
# This code is open-source. Feel free to modify and redistribute as you want.
# Participate on reddit in r/zerowriter if you want.
#
# Using the new4in2part library
#
# a python e-typewriter using eink and a USB keyboard
# this program outputs directly to the SPI eink screen, and is driven by a
# raspberry pi zero (or any pi). technically, it operates headless as the OS has no
# access to the SPI screen. it handles keyboard input directly via keyboard library.
#
# currently ONLY supports waveshare 4in2
#

import time
import keyboard
import keymaps
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd4in2_V2

from zerowriter import ZeroWriter


# Instantiate ZeroWriter with the default configuration
zero_writer = ZeroWriter()

try:
  zero_writer.epd = epd4in2_V2.EPD()
  zero_writer.keyboard = keyboard
  zero_writer.initialize()
  zero_writer.run()

except KeyboardInterrupt:
    pass

finally:
    keyboard.unhook_all()
    zero_writer.epd.init()
    time.sleep(1)
    zero_writer.epd.Clear()
    zero_writer.epd.sleep()
