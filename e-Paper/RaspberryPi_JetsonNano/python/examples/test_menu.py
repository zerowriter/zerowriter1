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

def write_line(text):
    for letter in list(text):
        zero_writer.keyboard.simulate_key_release(MockKeyEvent(letter))
        zero_writer.loop()
    zero_writer.keyboard.simulate_key_release(MockKeyEvent('enter'))

zero_writer.keyboard.simulate_key_press(MockKeyEvent('ctrl'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('m'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('ctrl'))

time.sleep(0.5)

# go to load
zero_writer.keyboard.simulate_key_release(MockKeyEvent('down'))
time.sleep(0.5)

# enter load
zero_writer.keyboard.simulate_key_release(MockKeyEvent('enter'))
time.sleep(1)

# go to first file
zero_writer.keyboard.simulate_key_release(MockKeyEvent('down'))
time.sleep(0.5)

# load file
zero_writer.keyboard.simulate_key_release(MockKeyEvent('enter'))

# visually make sure it's loaded
time.sleep(3)

zero_writer.keyboard.simulate_key_release(MockKeyEvent('down'))
time.sleep(0.5)
zero_writer.keyboard.simulate_key_release(MockKeyEvent('down'))
time.sleep(0.5)
zero_writer.keyboard.simulate_key_release(MockKeyEvent('down'))

time.sleep(0.5)
zero_writer.keyboard.simulate_key_release(MockKeyEvent('enter'))

time.sleep(15)