# zerowriter

----------

Zerowriter Ink (all-in-one device) is now available: https://www.crowdsupply.com/zerowriter/zerowriter-ink

Interest form / survey for potential future products: https://forms.gle/8dZwQsYdUa9X49WCA 
----------

Yo! Check the back of your 4.2" waveshare e-Paper. If it says Rev2.2 or has a V2 sticker, you'll want to use this branch: 

https://github.com/zerowriter/zerowriter1/tree/waveshare_2.2
The waveshare_2.2 branch is built specifically for the v2 displays. The main branches won't function properly on these displays. Going forward, this will likely be the default branch for the project.

If it says Rev2.1, you'll want to use these branches:

https://github.com/zerowriter/zerowriter1/tree/main_full
The main_full branch has a bunch of updates and includes a lot of new features.

This main branch will be discontinued and not further developed.
I am leaving it as-is because some people may want the simple typewriter with no extra software features. And it is a small codebase.

----------

An easy, DIY eink typewriter running on a raspberry pi zero. Perfect for beginners.

This project is open-source. Do whatever you want with it. Please note the display drivers and waveshare code belongs to them. But buy their displays, they rock.

Credit to: https://penkesu.computer/ for the original project that inspired this.

Components list: https://github.com/zerowriter/zerowriter1/blob/main/componentslist

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

epd.init_Partial() runs a faster update using modified LUT. (Ben Krasnow: https://hackaday.com/2017/10/31/ben-krasnow-hacks-e-paper-for-fastest-refresh-rate/) -- important to note this only works with the 4.2" v1 waveshare display.

Use a Pi Zero 2W. Don't use an original Zero. The extra power is very useful.

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

===

Have fun! Happy writing...

===

Steps to use a Bluetooth Keyboard

1. Run `sudo bluetoothctl`
2. Run `agent on`
3. Run `default-agent`
4. Run `scan on`
5. Wait until you see your device listed (be sure your keyboard is in pairing mode)
6. Run `scan off`
7. Run `devices` to list known Bluetooth devices
8. Run `pair AA:BB:CC:DD:EE:FF` where `AA:BB:CC:DD:EE:FF` is the MAC address of your bluetooth keyboard
9. You may need to reboot your raspberry pi before python is able to register your bluetooth keyboard.

https://www.youtube.com/watch?v=UEmSsscijKE has a video walkthrough of the above steps as well.

