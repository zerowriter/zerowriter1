#
# ZeroWriter
#
# This code is open-source. Feel free to modify and redistribute as you want.
# Participate on reddit in r/zerowriter if you want.
#
# Using the new4in2part library
#
# a python e-typewriter using eink and a USB keyboard
# this program outputs directly to the SPI eink screen, and is driven by a
# raspberry pi zero (or any pi). technically, it operates headless as the OS has no
# access to the SPI screen. it handles keyboard input directly via keyboard library.
#
# currently ONLY supports waveshare 4in2
#

import time
import keyboard
import keymaps
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import new4in2part
import textwrap
import subprocess
import signal
import os
from pathlib import Path


# Initialize the e-Paper display
# clear refreshes whole screen, should be done on slow init()
epd = new4in2part.EPD()
epd.init()
epd.Clear()

#Initialize display-related variables)
display_image = Image.new('1', (epd.width,epd.height), 255)
display_draw = ImageDraw.Draw(display_image)

#Display settings like font size, spacing, etc.
display_start_line = 0
font24 = ImageFont.truetype('Courier Prime.ttf', 18) #24
textWidth=16
linespacing = 22
chars_per_line = 32 #28
lines_on_screen = 12
last_display_update = time.time()

#display related
needs_display_update = True
needs_input_update = True
updating_input_area = False
input_catchup = False
display_catchup = False
display_updating = False
shift_active = False
control_active = False
exit_cleanup = False
console_message = ""
scrollindex=1


# Initialize cursor position
cursor_position = 0

# Initialize text matrix (size of text file)
max_lines = 100  # Maximum number of lines, adjust as needed
max_chars_per_line = chars_per_line  # Maximum characters per line, adjust as needed
text_content=""
temp_content=""
input_content=""
previous_lines = []
typing_last_time = time.time()  # Timestamp of last key press

#file directory setup: "/data/cache.txt"
file_path = os.path.join(os.path.dirname(__file__), 'data', 'cache.txt')

def load_previous_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            print(file_path)
            lines = file.readlines()
            return [line.strip() for line in lines]
    except FileNotFoundError:
        print("error")
        return []
    
def save_previous_lines(file_path, lines):
    print("attempting save")
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line + '\n')

def update_display():
    global last_display_update
    global needs_display_update
    global cursor_index
    global previous_lines
    global display_updating
    global updating_input_area
    global console_message
    global current_line
    global scrollindex
    
    # Clear the main display area -- also clears input line (270-300)
    display_draw.rectangle((0, 0, 400, 300), fill=255)
    
    # Display the previous lines
    y_position = 270 - linespacing  # leaves room for cursor input

    #Make a temp array from previous_lines. And then reverse it and display as usual.
    current_line=max(0,len(previous_lines)-lines_on_screen*scrollindex)
    temp=previous_lines[current_line:current_line+lines_on_screen]
    #print(temp)# to debug if you change the font parameters (size, chars per line, etc)

    for line in reversed(temp[-lines_on_screen:]):
       display_draw.text((10, y_position), line[:max_chars_per_line], font=font24, fill=0)
       y_position -= linespacing

    #Display Console Message
    if console_message != "":
        display_draw.rectangle((300, 270, 400, 300), fill=255)
        display_draw.text((300, 270), console_message, font=font24, fill=0)
        console_message = ""
    
    #generate display buffer for display
    partial_buffer = epd.getbuffer(display_image)
    epd.display(partial_buffer)

    last_display_update = time.time()
    display_catchup = True
    display_updating= False
    needs_display_update = False

def update_input_area(): #this updates the input area of the typewriter (active line)
    global last_display_update
    global needs_display_update
    global cursor_index
    global needs_input_update
    global updating_input_area

    cursor_index = cursor_position
    display_draw.rectangle((0, 270, 400, 300), fill=255)  # Clear display
    
    #add cursor
    temp_content = input_content[:cursor_index] + "|" + input_content[cursor_index:]
    
    #draw input line text
    display_draw.text((10, 270), str(temp_content), font=font24, fill=0)
    
    #generate display buffer for input line
    updating_input_area = True
    partial_buffer = epd.getbuffer(display_image)
    epd.display(partial_buffer)
    updating_input_area = False
    
def insert_character(character):
    global cursor_position
    global input_content
    global needs_display_update
    
    cursor_index = cursor_position
    
    if cursor_index <= len(input_content):
        # Insert character in the text_content string
        input_content = input_content[:cursor_index] + character + input_content[cursor_index:]
        cursor_position += 1  # Move the cursor forward
    
    needs_input_update = True

def delete_character():
    global cursor_position
    global input_content
    global needs_display_update
    
    cursor_index = cursor_position
    
    if cursor_index > 0:
        # Remove the character at the cursor position
        input_content = input_content[:cursor_index - 1] + input_content[cursor_index:]
        cursor_position -= 1  # Move the cursor back
        needs_input_update = True

    
def handle_key_down(e): #keys being held, ie modifier keys
    global shift_active
    global control_active
    
    if e.name == 'shift': #if shift is released
        shift_active = True
    if e.name == 'ctrl': #if shift is released
        control_active = True
    

def handle_key_press(e):
    global cursor_position
    global typing_last_time
    global display_start_line
    global needs_display_update
    global needs_input_update
    global shift_active
    global exit_cleanup
    global input_content
    global previous_lines
    global display_updating
    global input_catchup
    global control_active
    global console_message
    global scrollindex
    
    #save via ctrl + s
    if e.name== "s" and control_active:
        timestamp = time.strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        filename = os.path.join(os.path.dirname(__file__), 'data', f'zw_{timestamp}.txt')
        save_previous_lines(filename, previous_lines)
        
        console_message = f"[Saved]"
        update_display()
        time.sleep(1)
        console_message = ""
        update_display()

    #new file (clear) via ctrl + n
    if e.name== "n" and control_active: #ctrl+n
        #save the cache first
        timestamp = time.strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        filename = os.path.join(os.path.dirname(__file__), 'data', f'zw_{timestamp}.txt')
        save_previous_lines(filename, previous_lines)
        
        #create a blank doc
        previous_lines.clear()
        input_content = ""

        console_message = f"[New]"
        update_display()
        time.sleep(1)
        console_message = ""
        update_display()

    if e.name== "down" or e.name== "right":
       #move scrollindex down
       scrollindex = scrollindex - 1
       if scrollindex < 1:
            scrollindex = 1
       #--
       console_message = (f'[{round(len(previous_lines)/lines_on_screen)-scrollindex+1}/{round(len(previous_lines)/lines_on_screen)}]')
       update_display()
       console_message = ""

    if e.name== "up" or e.name== "left":
       #move scrollindex up
       scrollindex = scrollindex + 1
       if scrollindex > round(len(previous_lines)/lines_on_screen+1):
            scrollindex = round(len(previous_lines)/lines_on_screen+1)
       #--
       console_message = (f'[{round(len(previous_lines)/lines_on_screen)-scrollindex+1}/{round(len(previous_lines)/lines_on_screen)}]')
       update_display()
       console_message = ""

    #powerdown - could add an autosleep if you want to save battery
    if e.name == "esc" and control_active: #ctrl+esc
        #run powerdown script
        display_draw.rectangle((0, 0, 400, 300), fill=255)  # Clear display
        display_draw.text((55, 150), "ZeroWriter Powered Down.", font=font24, fill=0)
        partial_buffer = epd.getbuffer(display_image)
        epd.display(partial_buffer)
        time.sleep(3)
        subprocess.run(['sudo', 'poweroff', '-f'])
        
        needs_display_update = True
        needs_input_update = True
        input_catchup = True
        
        
    if e.name == "tab": 
        #just using two spaces for tab, kind of cheating, whatever.
        insert_character(" ")
        insert_character(" ")
        
        # Check if adding the character exceeds the line length limit
        if cursor_position > chars_per_line:
            previous_lines.append(input_content)                
            # Update input_content to contain the remaining characters
            input_content = ""
            needs_display_update = True #trigger a display refresh
        # Update cursor_position to the length of the remaining input_content
        cursor_position = len(input_content)
        
        needs_input_update = True
        input_catchup = True
        
    if e.name == "backspace":
        delete_character()
        needs_input_update = True
        input_catchup = True
            
    elif e.name == "space": #space bar
        insert_character(" ")
        
        # Check if adding the character exceeds the line length limit
        if cursor_position > chars_per_line:
            previous_lines.append(input_content)                
            input_content = ""
            needs_display_update = True
        # Update cursor_position to the length of the remaining input_content
        cursor_position = len(input_content)
        
        needs_input_update = True
        input_catchup = True
    
    elif e.name == "enter":
        if scrollindex>1:
            #if you were reviewing text, jump to scrollindex=1
            scrollindex = 1
            update_display()
        else:
            # Add the input to the previous_lines array
            previous_lines.append(input_content)
            input_content = "" #clears input content
            cursor_position=0
            #save the file when enter is pressed
            save_previous_lines(file_path, previous_lines)
            needs_display_update = True
            input_catchup = True
        
    if e.name == 'ctrl': #if control is released
        control_active = False 

    if e.name == 'shift': #if shift is released
        shift_active = False

    elif len(e.name) == 1 and control_active == False:  # letter and number input
        
        if shift_active:
            char = keymaps.shift_mapping.get(e.name)
            input_content += char
        else:
            input_content += e.name
            
        cursor_position += 1
        needs_input_update = True

        # Check if adding the character exceeds the line length limit
        if cursor_position > chars_per_line:
            # Find the last space character before the line length limit
            last_space = input_content.rfind(' ', 0, chars_per_line)
            sentence = input_content[:last_space]
            # Append the sentence to the previous lines
            previous_lines.append(sentence)                

            # Update input_content to contain the remaining characters
            input_content = input_content[last_space + 1:]
            needs_display_update=True
            
        # Update cursor_position to the length of the remaining input_content
        cursor_position = len(input_content)                

    typing_last_time = time.time()
    input_catchup==True
    needs_input_update = True
    
def handle_interrupt(signal, frame):
    keyboard.unhook_all()
    epd.init()
    epd.Clear()
    exit(0)

#Startup Stuff ---
keyboard.on_press(handle_key_down, suppress=False) #handles modifiers and shortcuts
keyboard.on_release(handle_key_press, suppress=True)
signal.signal(signal.SIGINT, handle_interrupt)

#init_display routine
epd.init()
epd.Clear
previous_lines = load_previous_lines(file_path)#('previous_lines.txt')
epd.init_Partial()
epd.Clear
needs_display_update = True
needs_input_update = False


#mainloop
try:
    while True:
        
        if exit_cleanup:
            break
                
        if needs_display_update and not display_updating:
            update_display()
            needs_diplay_update=False
            typing_last_time = time.time()
            
        elif (time.time()-typing_last_time)<(.5): #if not doing a full refresh, do partials
            #the screen enters a high refresh mode when there has been keyboard input
            if not updating_input_area and scrollindex==1:
                update_input_area()
        #time.sleep(0.05) #the sleep here seems to help the processor handle things, especially on 64-bit installs
        
except KeyboardInterrupt:
    pass

finally:
    keyboard.unhook_all()
    epd.init()
    time.sleep(1)
    epd.Clear()
    epd.sleep()
