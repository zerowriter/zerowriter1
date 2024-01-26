# *****************************************************************************
# * | File        :   epd4in2.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V4.2
# * | Date        :   2022-10-29
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
# Zerowriter Project disclaimer:
#
# This original driver has been modified for use in the Zerowriter project.
# The changes made push the display configuration outside of the recommended
# specs. Use at your own risk. 
#
# In general: We have used the fast LUT from Ben Krasnow:
# https://benkrasnow.blogspot.com/2017/10/fast-partial-refresh-on-42-e-paper.html
# and implemented it with the waveshare drivers, replacing the standard LUT.
# The original LUT have been shifted to Slow LUT. They clear the screen and prevent
# artifacting. 
#
# These LUT settings are display specific and only seem compatible with the waveshare 4.2"
# You could modify it to work with other waveshare displays, but it will be harder to get the
# latency to a respectable level.
#
# The partial update code is old waveshare code and doesn't actually function.
# There have been a few other minor adjustments that I found improved latency performance.
# The display buffer itself is a bit troublesome. It needs to buffer the entire screen,
# even if you are only updating one line. The typewriter application works around it,
# but there would be big improvements in latency if we could write a better buffer.
#
# 

import logging
from . import epdconfig
from PIL import Image
import RPi.GPIO as GPIO
import time

# Display resolution
EPD_WIDTH  = 400
EPD_HEIGHT = 300


GRAY1 = 0xff  # white
GRAY2 = 0xff
GRAY3 = 0x00  # gray
GRAY4 = 0x00  # Blackest

# Define the batch size (adjust as needed)
BATCH_SIZE_X = 24
BATCH_SIZE_Y = 24

logger = logging.getLogger(__name__)


class EPD:
    def __init__(self):
        self.reset_pin = epdconfig.RST_PIN
        self.dc_pin = epdconfig.DC_PIN
        self.busy_pin = epdconfig.BUSY_PIN
        self.cs_pin = epdconfig.CS_PIN
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.GRAY1 = GRAY1  # white
        self.GRAY2 = GRAY2
        self.GRAY3 = GRAY3  # gray
        self.GRAY4 = GRAY4  # Blackest
        self.DATA = [0x00] * 15000

    lut_vcom0 = [
        0x00, 0x0E, 0x00, 0x00, 0x00, 0x01,        
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,        
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,        
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,        
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,        
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,        
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_ww = [
        0xA0, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_bw = [
        0xA0, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_wb = [
        0x50, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    lut_bb = [
        0x50, 0x0E, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00 
    ]
    
    #slow lut
    
    slow_lut_vcom0 = [
        0x00, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x00, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x00, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00,
    ]
    slow_lut_ww = [
        0x50, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x90, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0xA0, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    slow_lut_bw = [
        0x50, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x90, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0xA0, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    slow_lut_wb = [
        0xA0, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x90, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x50, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    slow_lut_bb = [
        0x20, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x90, 0x0F, 0x0F, 0x00, 0x00, 0x01,
        0x10, 0x08, 0x08, 0x00, 0x00, 0x02,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]    
    
    
    # ******************************partial screen update LUT*********************************/
    EPD_4IN2_Partial_lut_vcom1 = [
        0x00, 0x01, 0x20, 0x01, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    EPD_4IN2_Partial_lut_ww1 = [
        0x00, 0x01, 0x20, 0x01, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    EPD_4IN2_Partial_lut_bw1 = [
        0x20, 0x01, 0x20, 0x01, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    EPD_4IN2_Partial_lut_wb1 = [
        0x10, 0x01, 0x20, 0x01, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    EPD_4IN2_Partial_lut_bb1 = [
        0x00, 0x01, 0x20, 0x01, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    # ******************************gray*********************************/
    # 0~3 gray
    EPD_4IN2_4Gray_lut_vcom = [
        0x00, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x60, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x00, 0x00, 0x00, 0x01,
        0x00, 0x13, 0x0A, 0x01, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]
    # R21
    EPD_4IN2_4Gray_lut_ww = [
        0x40, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x10, 0x14, 0x0A, 0x00, 0x00, 0x01,
        0xA0, 0x13, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    # R22H r
    EPD_4IN2_4Gray_lut_bw = [
        0x40, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x0A, 0x00, 0x00, 0x01,
        0x99, 0x0C, 0x01, 0x03, 0x04, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    # R23H w
    EPD_4IN2_4Gray_lut_wb = [
        0x40, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x00, 0x14, 0x0A, 0x00, 0x00, 0x01,
        0x99, 0x0B, 0x04, 0x04, 0x01, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]
    # R24H b
    EPD_4IN2_4Gray_lut_bb = [
        0x80, 0x0A, 0x00, 0x00, 0x00, 0x01,
        0x90, 0x14, 0x14, 0x00, 0x00, 0x01,
        0x20, 0x14, 0x0A, 0x00, 0x00, 0x01,
        0x50, 0x13, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ]

    # Hardware reset
    def reset(self):
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(10)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(10)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(10)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(10)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(10)
        epdconfig.digital_write(self.reset_pin, 0)
        epdconfig.delay_ms(10)
        epdconfig.digital_write(self.reset_pin, 1)
        epdconfig.delay_ms(10)

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
        self.send_command(0x71)
        while epdconfig.digital_read(self.busy_pin) == 0:  # 0: idle, 1: busy
            self.send_command(0x71)
            epdconfig.delay_ms(20)

    def set_lut(self):
        self.send_command(0x20)  # vcom
        self.send_data2(self.lut_vcom0)

        self.send_command(0x21)  # ww --
        self.send_data2(self.lut_ww)

        self.send_command(0x22)  # bw r
        self.send_data2(self.lut_bw)

        self.send_command(0x23)  # wb w
        self.send_data2(self.lut_bb)

        self.send_command(0x24)  # bb b
        self.send_data2(self.lut_wb)
        
    def set_slow_lut(self):
        self.send_command(0x20)  # vcom
        self.send_data2(self.slow_lut_vcom0)

        self.send_command(0x21)  # ww --
        self.send_data2(self.slow_lut_ww)

        self.send_command(0x22)  # bw r
        self.send_data2(self.slow_lut_bw)

        self.send_command(0x23)  # wb w
        self.send_data2(self.slow_lut_bb)

        self.send_command(0x24)  # bb b
        self.send_data2(self.slow_lut_wb)

    def Partial_SetLut(self):
        self.send_command(0x20)
        self.send_data2(self.EPD_4IN2_Partial_lut_vcom1)

        self.send_command(0x21)
        self.send_data2(self.EPD_4IN2_Partial_lut_ww1)

        self.send_command(0x22)
        self.send_data2(self.EPD_4IN2_Partial_lut_bw1)

        self.send_command(0x23)
        self.send_data2(self.EPD_4IN2_Partial_lut_wb1)

        self.send_command(0x24)
        self.send_data2(self.EPD_4IN2_Partial_lut_bb1)

    def Gray_SetLut(self):
        self.send_command(0x20)  # vcom
        self.send_data2(self.EPD_4IN2_4Gray_lut_vcom)

        self.send_command(0x21)  # red not use
        self.send_data2(self.EPD_4IN2_4Gray_lut_ww)

        self.send_command(0x22)  # bw r
        self.send_data2(self.EPD_4IN2_4Gray_lut_bw)

        self.send_command(0x23)  # wb w
        self.send_data2(self.EPD_4IN2_4Gray_lut_wb)

        self.send_command(0x24)  # bb b
        self.send_data2(self.EPD_4IN2_4Gray_lut_bb)

        self.send_command(0x25)  # vcom
        self.send_data2(self.EPD_4IN2_4Gray_lut_ww)

    def init(self):
        if epdconfig.module_init() != 0:
            return -1
        # EPD hardware init start
        self.reset()

        self.send_command(0x01)  # POWER SETTING
        self.send_data(0x03)  # VDS_EN, VDG_EN
        self.send_data(0x00)  # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b)  # VDH
        self.send_data(0x2b)  # VDL

        self.send_command(0x06)  # boost soft start
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)

        self.send_command(0x04)  # POWER_ON
        self.ReadBusy()

        self.send_command(0x00)  # panel setting
        self.send_data(0xbf)  # KW-BF   KWR-AF  BWROTP 0f

        self.send_command(0x30)  # PLL setting
        self.send_data(0x3C)  #3C 3A 100HZ   29 150Hz 39 200HZ  31 171HZ

        self.send_command(0x61)  # resolution setting
        self.send_data(0x01)
        self.send_data(0x90)  # 128
        self.send_data(0x01)
        self.send_data(0x2c)

        self.send_command(0x82)  # vcom_DC setting
        self.send_data(0x12)

        self.send_command(0X50)  # VCOM AND DATA INTERVAL SETTING
        self.send_data(
            0xF7)  # 97white border 77black border  VBDF 17|D7 VBDW 97 VBDB 57  VBDF F7 VBDW 77 VBDB 37  VBDR B7

        self.set_slow_lut()
        self.ReadBusy() #added aug17
        # EPD hardware init end
        return 0

    def init_Partial(self):
        if epdconfig.module_init() != 0:
            return -1
        # EPD hardware init start
        self.reset()

        self.send_command(0x01)  # POWER SETTING
        self.send_data(0x03)  # VDS_EN, VDG_EN
        self.send_data(0x00)  # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b)  # VDH
        self.send_data(0x2b)  # VDL

        self.send_command(0x06)  # boost soft start
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)

        self.send_command(0x04)  # POWER_ON
        self.ReadBusy()

        self.send_command(0x00)  # panel setting
        self.send_data(0xbf)  # KW-BF   KWR-AF  BWROTP 0f

        self.send_command(0x30)  # PLL setting
        self.send_data(0x3c)  #3c 3A 100HZ   29 150Hz **39** 200HZ  31 171HZ

        self.send_command(0x61)  # resolution setting
        self.send_data(0x01)
        self.send_data(0x90)  # 128
        self.send_data(0x01)
        self.send_data(0x2c)

        self.send_command(0x82)  # vcom_DC setting
        self.send_data(0x12)

        self.send_command(0X50)  # VCOM AND DATA INTERVAL SETTING
        self.send_data(#17 or F7 = no flashing
            0xF7)  #07def 97white border 77black border  VBDF *17*|D7 VBDW 97 VBDB 57  VBDF F7 VBDW 77 VBDB 37  VBDR B7

        self.set_lut()
        #self.ReadBusy()
        # EPD hardware init end
        return 0

    def getbuffer(self, image):
        #ms=time.time()
        # logger.debug("bufsiz = ",int(self.width/8) * self.height)
        buf = [0xFF] * (int(self.width / 8) * self.height)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()
        # logger.debug("imwidth = %d, imheight = %d",imwidth,imheight)
        if imwidth == self.width and imheight == self.height:
            #logger.debug("Horizontal")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        elif imwidth == self.height and imheight == self.width:
            #logger.debug("Vertical")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[int((newx + newy * self.width) / 8)] &= ~(0x80 >> (y % 8))
        #print (time.time()-ms)
        return buf

    def display(self, image):
        if self.width % 8 == 0:
            linewidth = int(self.width / 8)
        else:
            linewidth = int(self.width / 8) + 1

        self.send_command(0x92) #91=partial 92=regular
        self.send_command(0x90)  # resolution setting
        #self.set_lut() #likely not needed each time as the LUT are set on init.
        self.send_command(0x10)
        self.send_data2([0xFF] * int(self.width * linewidth)) #high cpu overhead
        self.send_command(0x13)
        self.send_data2(image)

        self.send_command(0x12) #refresh
       
        #self.ReadBusy()


    def Clear(self):
        if self.width % 8 == 0:
            linewidth = int(self.width / 8)
        else:
            linewidth = int(self.width / 8) + 1

        self.send_command(0x10)
        self.send_data2([0xff] * int(self.height * linewidth))

        self.send_command(0x13)
        self.send_data2([0xff] * int(self.height * linewidth))

        self.send_command(0x12)
        #self.ReadBusy()

    def sleep(self):
        self.send_command(0x02)  # POWER_OFF
        self.ReadBusy()
        self.send_command(0x07)  # DEEP_SLEEP
        self.send_data(0XA5)

        epdconfig.delay_ms(2000)
        epdconfig.module_exit()

### END OF FILE ###
