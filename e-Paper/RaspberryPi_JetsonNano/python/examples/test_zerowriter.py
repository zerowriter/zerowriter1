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

write_line("this is some test text that we can use to test the zerowriter. it should be long enough to wrap around the screen.")

write_line("lorem ipsum dolor sit amet, consectetur adipiscing elit. sed non risus. suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor.")
# write_line("cras elementum ultrices diam. maecenas ligula massa, varius a, semper congue, euismod non, mi.")
# write_line("proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit amet erat.")
# write_line("duis semper. duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. pellentesque congue.")
# write_line("ut in risus volutpat libero pharetra tempor. cras vestibulum bibendum augue.")
# write_line("praesent egestas leo in pede. praesent blandit odio eu enim.")
# write_line("pellentesque sed dui ut augue blandit sodales. vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; aliquam nibh.")
# write_line("mauris ac mauris sed pede pellentesque fermentum. maecenas adipiscing ante non diam sodales hendrerit.")
# write_line("ut velit mauris, egestas sed, gravida nec, ornare ut, mi. aenean ut orci vel massa suscipit pulvinar.")
# write_line("nulla sollicitudin. fusce varius, ligula non tempus aliquam, nunc turpis ullamcorper nibh, in tempus sapien eros vitae ligula.")
# write_line("pellentesque rhoncus nunc et augue. integer id felis.")
# write_line("curabitur aliquet pellentesque diam. integer quis metus vitae elit lobortis egestas.")

time.sleep(2)

for letter in "abcdefghijklmnopqrstuvwzyz": 
  zero_writer.keyboard.simulate_key_release(MockKeyEvent(letter))
  zero_writer.loop()

zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('backspace'))
zero_writer.loop()

time.sleep(2)

# zero_writer.keyboard.simulate_key_press(MockKeyEvent('ctrl'))
# zero_writer.keyboard.simulate_key_release(MockKeyEvent('q'))
# zero_writer.keyboard.simulate_key_release(MockKeyEvent('ctrl'))

# time.sleep(15)


write_line("about to test pagination")

time.sleep(2)

zero_writer.keyboard.simulate_key_release(MockKeyEvent('up'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('up'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('up'))
zero_writer.keyboard.simulate_key_release(MockKeyEvent('up'))

time.sleep(2)

zero_writer.keyboard.simulate_key_release(MockKeyEvent('down'))
time.sleep(2)

zero_writer.keyboard.simulate_key_release(MockKeyEvent('down'))
time.sleep(2)

zero_writer.keyboard.simulate_key_release(MockKeyEvent('down'))
time.sleep(2)

zero_writer.keyboard.simulate_key_release(MockKeyEvent('down'))
time.sleep(2)