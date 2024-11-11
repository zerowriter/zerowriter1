important update: raspberry pi OS has changed GPIO support, so it is important you use archived versions of the OS: https://github.com/zerowriter/zerowriter1/issues/26#issuecomment-2466903737

THIS BRANCH IS FOR REV 2.2 DISPLAYS.

# zerowriter

An easy, DIY eink typewriter running on a raspberry pi zero. Perfect for beginners.
Components list: https://github.com/zerowriter/zerowriter1/blob/main/componentslist

Setup: https://github.com/zerowriter/zerowriter1/blob/waveshare_2.2/setup_2.2

NOTE: There is a known bug which may cause your pi zero to lose wifi connection after the first boot / setup. In this case, you need to connect your pi to HDMI and reconfigure wifi in sudo raspi-config and then you will be good to go again. This only needs to be done once. This bug is because of the network controller in the zerowriter software which lets you join wifi networks (like a regular computer).

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
- https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_Manual refer to the waveshare guide for pinout. probably test with their code first to make sure display works.
- (https://github.com/zerowriter/zerowriter1/blob/waveshare_2.2/setup_2.2)

Hardware 
- 40% keyboard and an eink display
- tons of storage
- bring-your-own-battery-pack: 10,000mah battery will yield around 25-30 hours of usage, a lot more if you cut networking
- or just plug it into something
- portable! stylish! cool! modified from the https://penkesu.computer/ penkesu computer


Enjoy! Have fun. Happy writing.
