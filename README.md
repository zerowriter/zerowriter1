This branch is experimental. There is a current bug when loading the program related to initializing the display. Sometimes, the epd.init /epd.clear are not executing as intended, which causes a bunch of display related issues.
Feel free to experiment with this branch (and let me know if you solve this bug)

It works flawlessly on my development unit, but on a fresh install the bug has cropped up. So maybe a library or recent update to a SPI driver or something? Not too sure.



# zerowriter

An easy, DIY eink typewriter running on a raspberry pi zero. Perfect for beginners.
Components list: https://github.com/zerowriter/zerowriter1/blob/main/componentslist

----------
This branch merges jacobsmith's update with the fixed driver for the rev 2.2 waveshare display. This branch does not yet support the rev 2.1 (original) display.

This branch will replace the main branch as the codebase is much more feature complete. The 2.2 display will be "THE" supported 4.2" display going forward, as the 2.1 display is not beign manufactured anymore.

NEW: Program Features
- light weight python typewriter
- works with any USB keyboard
- KEYMAPS file  to edit key maps if you don't want to program your keyboard's firmware
- files save in the /data directory where the program resides
- autosaves the cache every time return is pressed
- CTRL R forces screen refresh, handy for catching eink bugs
- CTRL S (quicksave) saves the cache to a txt file
- CTRL N starts a new file
- CTRL G sends a gmail to yourself if configured
- Save As: save a file with a unique name instead of the quicksave
- File browser: load previous files to continue, or press CTRL+BACKSPACE to delete. Deleted files are just moved to the Archive folder 
- Server: you can access your files from your browser via local webserver
- Wi Fi manager: you can find and join local networks. Currently only supports password protected networks.
- Arrow keys can be used to navigate through and review previous writing -- no editing.

----------
 
The e-Paper directory is modified waveshare drivers. All waveshare code belongs to them. Great company, buy their gadgets! Use this modified code at your own risk. The modified driver may cause damage to your display. Don't blame me.

I have included .STL files for the enclosure I have been using. Feel free to use them however you want.

----------

How it works:

Inside the e-Paper directory, I built an application on top of the example code from waveshare. You can find it in e-Paper/RaspberryPiJetsonNano/python/examples main.py. jacobsmith built some more features in, and I have adopted them in to the codebase and built them out further.

Zerowriter now has a menu system. It supports file functions: New, Save As, Load/Delete. It supports Gmail integration for emailing yourself files, but you should only use a burner account as info is stored in a json file. It can generate QR codes, connect to Wifi networks on-device, and host files for local access via a server.

An overclocked Pi Zero 2 W can handle running this stuff around 200ms. You might be able to squeeze performance with a better CPU, or maybe optimizing the buffer in the display driver. Currently, the buffer needs to calculate the entire screen buffer, even for partial updates.

Use a Pi Zero 2W. Don't use an original Zero.

----------

Setup / Getting Started
- requires pi zero 2w running linux 12 bookworm, light install recomend (headless/no GUI)
- set up ssh and configure your pi zero remotely via terminal or powershell
- https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_Manual refer to the waveshare guide for pinout and install instructions. You can use my e-Paper directory instead of theirs, but probably test with their code first
- Drop in the e-Paper folder provided in this repo and run sudo python main.py from ssh
- install SMB or similar so you can access your files via SMB from another device
- Set up crontab (from command line: crontab -e) to boot to main.py

Hardware Features
- 40% keyboard and an eink display
- tons of storage
- bring-your-own-battery-pack: 10,000mah battery will yield around 25-30 hours of usage, a lot more if you cut networking
- or just plug it into something
- portable! stylish! cool! modified from the https://penkesu.computer/ penkesu computer

Crontab
  - this launches the typewriter on powerup
  - install crontab
  - at ssh commandline, type crontab -e and add this line at the bottom:
  #@reboot cd e-Paper/RaspberryPi_JetsonNano/python/examples/ && sudo python main.py &

But instead, I'd recomend using a bashrc file and getting it to boot that folder up. Because crontab actually keeps a terminal running in the background and the user could do some weird stuff unintentionally, oops.

Enjoy! Have fun. Happy writing.
