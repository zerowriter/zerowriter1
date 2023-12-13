# zerowriter
 
The e-Paper directory is modified waveshare drivers. All waveshare code belongs to them. 

Use this modified code at your own risk. The modified driver may cause damage to your display. Don't blame me.

How it works:

Inside the e-Paper directory, I built an application on top of the example code from waveshare. You can find it in e-Paper/RaspberryPiJetsonNano/python/examples main.py

The application itself can be modified to do whatever you want. The basics:

epd.init() clears the screen using slow look up tables -- this prevents artifacting

epd.init_Partial() runs a faster update using modified LUT. 

