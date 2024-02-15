# *****************************************************************************
# * | File        :   epd4in2_V2.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2023-09-13
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# This driver has been slightly modified for the Zerowriter project. 
# This modifies the waveshare code beyond their spec and could result
# in damage to the panel long-term. It's untested. Use at your own risk.
#


import logging
import time
from . import epdconfig
from PIL import Image
import RPi.GPIO as GPIO

# Display resolution
EPD_WIDTH  = 400
EPD_HEIGHT = 300

GRAY1 = 0xff  # white
GRAY2 = 0xC0
GRAY3 = 0x80  # gray
GRAY4 = 0x00  # Blackest

logger = logging.getLogger(__name__)


class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.Seconds_1_5S = 0
        self.Seconds_1S = 1
        self.GRAY1 = GRAY1  # white
        self.GRAY2 = GRAY2
        self.GRAY3 = GRAY3  # gray
        self.GRAY4 = GRAY4  # Blackest
        # Initialize buffer and previous_buffer
        self.pixels_per_byte = 8
        self.buffer = [0xFF] * (int(self.width / self.pixels_per_byte) * self.height)
        self.previous_buffer = [0xFF] * (int(self.width / self.pixels_per_byte) * self.height)

    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(100)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(2)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(100)

    def send_command(self, command):
        epdconfig.digital_write(self.dc_pin, 0)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([command])
        epdconfig.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte([data])
        epdconfig.digital_write(self.cs_pin, 1)

    # send a lot of data   
    def send_data2(self, data):
        epdconfig.digital_write(self.dc_pin, 1)
        epdconfig.digital_write(self.cs_pin, 0)
        epdconfig.spi_writebyte2(data)
        epdconfig.digital_write(self.cs_pin, 1)

    def ReadBusy(self):        
        #logger.debug("e-Paper busy")
        while(epdconfig.digital_read(self.busy_pin) == 1):      #  0: idle, 1: busy
            epdconfig.delay_ms(10)
        #logger.debug("e-Paper busy release")
    
    def TurnOnDisplay(self):
        self.send_command(0x22) #Display Update Control
        self.send_data(0xF7)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()
        
    def TurnOnDisplay_Fast(self): #fast
        self.send_command(0x22) #Display Update Control
        self.send_data(0xC7)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()
        
    def TurnOnDisplay_Partial(self):
        
        self.send_command(0x22) #Display Update Control
        self.send_data(0xFF) #FF
        self.send_command(0x20) #Activate Display Update Sequence
        
        #self.ReadBusy()

    def init(self):
        if epdconfig.module_init() != 0:
            return -1
        # EPD hardware init start
        self.reset()
        self.ReadBusy()

        self.send_command(0x12) #SWRESET
        self.ReadBusy()

        self.send_command(0x21)  # Display update control
        self.send_data(0x40)
        self.send_data(0x00)

        self.send_command(0x3C)  # BorderWavefrom
        self.send_data(0x03) #3

        self.send_command(0x11)  # data  entry  mode
        self.send_data(0x03)  # X-mode

        self.send_command(0x44) 
        self.send_data(0x00)
        self.send_data(0x31)  
        
        self.send_command(0x45) 
        self.send_data(0x00)
        self.send_data(0x00)  
        self.send_data(0x2B)
        self.send_data(0x01)

        self.send_command(0x4E) 
        self.send_data(0x00)

        self.send_command(0x4F) 
        self.send_data(0x00)
        self.send_data(0x00)  
        self.ReadBusy()

        return 0
    
    def init_Fast(self, mode):
        if epdconfig.module_init() != 0:
            return -1
        # EPD hardware init start
        self.reset()
        self.ReadBusy()

        self.send_command(0x12) #SWRESET
        self.ReadBusy()

        self.send_command(0x21)  # Display update control
        self.send_data(0x40)
        self.send_data(0x00)

        self.send_command(0x3C)  # BorderWavefrom
        self.send_data(0x05)

        if mode == self.Seconds_1_5S:
             self.send_command(0x1A)
             self.send_data(0x6E)  
        else :
             self.send_command(0x1A)
             self.send_data(0x5E)  

        self.send_command(0x22)  # Load temperature value
        self.send_data(0x91)  
        self.send_command(0x20)  
        self.ReadBusy()

        self.send_command(0x11)  # data  entry  mode
        self.send_data(0x03)  # X-mode

        self.send_command(0x44) 
        self.send_data(0x00)
        self.send_data(0x31)  
        
        self.send_command(0x45) 
        self.send_data(0x00)
        self.send_data(0x00)  
        self.send_data(0x2B)
        self.send_data(0x01)

        self.send_command(0x4E) 
        self.send_data(0x00)

        self.send_command(0x4F) 
        self.send_data(0x00)
        self.send_data(0x00)  
        self.ReadBusy()

        return 0


    def getbuffer(self, image):
        starttime = time.time()
        pixelsperbyte = 8
        buf = [0xFF] * (int(self.width / pixelsperbyte) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()

        if imwidth == self.width and imheight == self.height:
            #logger.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / pixelsperbyte)] &= ~(0x80 >> (x % pixelsperbyte))
        # elif imwidth == self.height and imheight == self.width:
        #     #logger.debug("Vertical")
        #     for y in range(imheight):
        #         for x in range(imwidth):
        #             newx = y
        #             newy = self.height - x - 1
        #             if pixels[x, y] == 0:
        #                 buf[int((newx + newy * self.width) / pixelsperbyte)] &= ~(0x80 >> (y % pixelsperbyte))
        #print (time.time()-starttime)
        return buf
    
    def Clear(self):
        if self.width % 8 == 0:
            linewidth = int(self.width / 8)
        else:
            linewidth = int(self.width / 8) + 1

        self.send_command(0x24)
        self.send_data2([0xff] * int(self.height * linewidth))

        self.send_command(0x26)
        self.send_data2([0xff] * int(self.height * linewidth))

        self.TurnOnDisplay()

    def display(self, image):
        self.send_command(0x24)
        self.send_data2(image)

        self.send_command(0x26)
        self.send_data2(image)

        self.TurnOnDisplay()

    def display_Fast(self, image):
        self.send_command(0x24)
        self.send_data2(image)

        self.send_command(0x26)
        self.send_data2(image)

        self.TurnOnDisplay_Fast()

    def display_Partial(self, Image):
        self.send_command(0x3C)  # BorderWaveform
        self.send_data(0x80) # blank border?

        self.send_command(0x21)  # Display update control
        self.send_data(0x00)

        self.send_command(0x24) # WRITE_RAM
        self.send_data2(Image)  
        self.TurnOnDisplay_Partial()

    def sleep(self):
        self.send_command(0x10)  # DEEP_SLEEP
        self.send_data(0x01)

        epdconfig.delay_ms(2000)
        epdconfig.module_exit()

### END OF FILE ###