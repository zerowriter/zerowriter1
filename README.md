# zerowriter

An easy, DIY eink typewriter running on a raspberry pi zero. Perfect for beginners.

This project is open-source. Do whatever you want with it. Please note the display drivers and waveshare code belongs to them. But buy their displays, they rock.

Components list: https://github.com/zerowriter/zerowriter1/blob/main/components_list

pi zero setup steps: https://github.com/zerowriter/zerowriter1/blob/main/how-to-setup-your-pi

----------
 
The e-Paper directory is modified waveshare drivers. All waveshare code belongs to them. Great company, buy their gadgets!

Use this modified code at your own risk. The modified driver may cause damage to your display. Don't blame me.

I have included .STL files for the enclosure I have been using. Feel free to use them however you want.

----------

How it works:

Inside the e-Paper directory, I built an application on top of the example code from waveshare. You can find it in e-Paper/RaspberryPiJetsonNano/python/examples main.py

The application itself can be modified to do whatever you want (or just leave it be). The basics:

epd.init() clears the screen using slow look up tables -- this prevents artifacting

epd.init_Partial() runs a faster update using modified LUT. (Ben Krasnow: https://hackaday.com/2017/10/31/ben-krasnow-hacks-e-paper-for-fastest-refresh-rate/) -- important to note this only works with the 4.2" waveshare display.

An overclocked Pi Zero 2 W can handle running this stuff around 150-200ms. You might be able to squeeze performance with a better CPU, or maybe optimizing the buffer in the display driver. Currently, the buffer needs to calculate the entire screen buffer, even for partial updates. Try playing with your overclocking settings to see if you get something that fits what you want to do.

Use a Pi Zero 2. Don't use an original Zero. The extra power is very useful.

----------

Setup / Getting Started:

https://github.com/zerowriter/zerowriter1/blob/main/how-to-setup-your-pi

- requires pi zero 2w running bookworm, light install recomend (headless/no GUI)
- set up ssh and configure your pi zero remotely via terminal or powershell
- Drop in the e-Paper folder provided in this repo and run main.py from ssh
- Set up crontab (from command line: crontab -e) to boot to main.py

Hardware Features:
- 40% keyboard and an eink display
- tons of storage
- bring-your-own-battery-pack: 10,000mah battery will yield around 25-30 hours of usage, a lot more if you cut networking
- or just plug it into something
- portable! stylish! cool! modified from the https://penkesu.computer/ penkesu computer

Program Features:
- light weight python typewriter
- works with any USB keyboard
- KEYMAPS file to edit key maps if you don't want to program your keyboard's firmware
- files save in the /data directory where the program resides, access via SMB
- autosaves the cache every time return is pressed
- CTRL S saves the cache to a txt file
- CTRL N starts a new file
- CTRL ESC turns unit off.
- (NEW, likely buggy) The arrow keys can be used to navigate through and review previous writing
- You could easily add an output to google drive or etc

Current Issues / Requests / Going Further:
- I'm not a programmer, so my code isn't very clean.. would be great to have someone revise it at some point.
- Running multiple instances of the display driver will cause weird issues -- be sure to kill the main.py process or reboot regularly if you are tinkering
- Due to the way pi zero power works, there is no standby, so zerowriter consumes considerable power when idle. maybe someone can think of a creative workaround here?
- The display buffer code from waveshare requires a full buffer even for partial display updates. Writing a display buffer is beyond what I can do... this would have big implications for speed / refresh rate
- If you want to save power, you could disable networking entirely, and cut other services. I don't find it worth the trouble as I use SSH so frequently 
- Want to install your own lipo battery? Go for it. There's space inside to accomodate. Thing is, it adds complexity and isn't really a fit for an easy DIY build. 'Cause you need to measure the lipo, and do other stuff to handle it... on the hardware and software side. I think it is beyond the scope for this project but feel free to do it yourself and share. I think it could be cool.
- I'd like to keep this program simple and clean, so I want to avoid bloat... not interested in editing features, or even file managers and such. Maybe could change my mind on that.

Enjoy! Have fun. Happy writing.
