import time
import keymaps
from PIL import Image, ImageDraw, ImageFont

from mock_epd import MockEPD
from zerowriter import ZeroWriter
from mock_keyboard import MockKeyboard

class MockKeyEvent:
    def __init__(self, name):
        self.name = name


zero_writer = ZeroWriter()
zero_writer.epd = MockEPD(400, 300)
zero_writer.keyboard = MockKeyboard()
zero_writer.initialize()
zero_writer.loop()

for letter in list("this is some test text that we can use to test the zerowriter. it should be long enough to wrap around the screen."):
    zero_writer.keyboard.simulate_key_release(MockKeyEvent(letter))
    zero_writer.loop()

time.sleep(2)
