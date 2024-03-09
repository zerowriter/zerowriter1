WAVESHARE V1 / 2.1 DISPLAYS ONLY

This branch is experimental. This branch is for waveshare 2.1 displays and includes all the recent updates, like menus, filesharing, etc.
It isn't tested very much yet but should be pretty stable.

Note / Disclaimer: The waveshare 2.1 is fast at the cost of clarity. You might find it a bit "muddy" -- that is because I have modified the original driver to prioritize speed over contrast. The 2.2 version is the opposite -- slower, cleaner, brighter.
It's because of how the eink panels works. The 2.1 panel lets you control the speed (in hz) of how fast the waveform is applied.
If you are interested in editing or adjusting, check out the new4in2part.py driver file. It's fairly well documented.


# zerowriter

An easy, DIY eink typewriter running on a raspberry pi zero. Perfect for beginners.
Components list: https://github.com/zerowriter/zerowriter1/blob/main/componentslist

----------

This branch merges jacobsmith's update with the fixed driver for the rev 2.1 waveshare display.

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

The waveshare 2.1 is fast at the cost of clarity. You might find it a bit "muddy" -- that is because I have modified the original driver to prioritize speed over contrast. The 2.2 version is the opposite -- slower, cleaner, brighter.

Use a Pi Zero 2W. Don't use an original Zero.

----------

Setup / Getting Started
- requires pi zero 2w running linux 12 bookworm, light install recomend (headless/no GUI)
- set up ssh and configure your pi zero remotely via terminal or powershell
- https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_Manual refer to the waveshare guide for pinout and install instructions. You can use my e-Paper directory instead of theirs, but probably test with their code first
- Drop in the e-Paper folder provided in this repo and run sudo python main.py from ssh
- install SMB or similar so you can access your files via SMB from another device
- Set up bashrc to boot to main.py

Hardware Features
- 40% keyboard and an eink display
- tons of storage
- bring-your-own-battery-pack: 10,000mah battery will yield around 25-30 hours of usage, a lot more if you cut networking
- or just plug it into something
- portable! stylish! cool! modified from the https://penkesu.computer/ penkesu computer

Enjoy! Have fun. Happy writing.
