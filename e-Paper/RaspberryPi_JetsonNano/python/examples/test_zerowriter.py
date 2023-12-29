import time
import keymaps
from PIL import Image, ImageDraw, ImageFont

from mock_epd import MockEPD
from zerowriter import ZeroWriter
from mock_keyboard import MockKeyboard


zero_writer = ZeroWriter()
zero_writer.epd = MockEPD(400, 300)
zero_writer.keyboard = MockKeyboard()
zero_writer.initialize()
zero_writer.run()
