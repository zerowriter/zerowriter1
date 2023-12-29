import time
import keymaps
from PIL import Image, ImageDraw, ImageFont

class ZeroWriter:
    def __init__(self):
        self.epd = None
        self.display_image = None
        self.display_draw = None
        self.display_updating = False
        self.cursor_position = 0
        self.text_content = ""
        self.input_content = ""
        self.previous_lines = []
        self.needs_display_update = True
        self.needs_input_update = True
        self.chars_per_line = 32
        self.lines_on_screen = 12
        self.font_size = 18
        self.line_spacing = 22
        self.scrollindex = 0
        self.console_message = ""
        self.updating_input_area = False
    
    def initialize(self):
        self.epd.init()
        self.epd.Clear()
        self.display_image = Image.new('1', (self.epd.width, self.epd.height), 255)
        self.display_draw = ImageDraw.Draw(self.display_image)
        self.last_display_update = time.time()

    def load_previous_lines(self, file_path):
        try:
            with open(file_path, 'r') as file:
                print(file_path)
                lines = file.readlines()
                return [line.strip() for line in lines]
        except FileNotFoundError:
            print("error")
            return []

    def save_previous_lines(self, file_path, lines):
      print("attempting save")
      with open(file_path, 'w') as file:
          for line in lines:
              file.write(line + '\n')

    def update_display(self):
        self.display_updating = True

        # Clear the main display area -- also clears input line (270-300)
        self.display_draw.rectangle((0, 0, 400, 300), fill=255)
        
        # Display the previous lines
        y_position = 270 - self.line_spacing  # leaves room for cursor input

        #Make a temp array from previous_lines. And then reverse it and display as usual.
        current_line=max(0,len(self.previous_lines)-self.lines_on_screen*self.scrollindex)
        temp=self.previous_lines[current_line:current_line+self.lines_on_screen]
        #print(temp)# to debug if you change the font parameters (size, chars per line, etc)

        for line in reversed(temp[-self.lines_on_screen:]):
          display_draw.text((10, y_position), line[:max_chars_per_line], font=font24, fill=0)
          y_position -= self.line_spacing

        #Display Console Message
        if self.console_message != "":
            display_draw.rectangle((300, 270, 400, 300), fill=255)
            display_draw.text((300, 270), self.console_message, font=font24, fill=0)
            self.console_message = ""
        
        #generate display buffer for display
        partial_buffer = self.epd.getbuffer(self.display_image)
        self.epd.display(partial_buffer)

        self.last_display_update = time.time()
        self.display_updating = False
        self.needs_display_update = False

    def update_input_area(self):
        cursor_index = self.cursor_position
        self.display_draw.rectangle((0, 270, 400, 300), fill=255)  # Clear display
        
        #add cursor
        temp_content = input_content[:cursor_index] + "|" + input_content[cursor_index:]
        
        #draw input line text
        self.display_draw.text((10, 270), str(temp_content), font=font24, fill=0)
        
        #generate display buffer for input line
        self.updating_input_area = True
        partial_buffer = epd.getbuffer(self.display_image)
        self.epd.display(partial_buffer)
        self.updating_input_area = False

    def insert_character(self, character):
        cursor_index = self.cursor_position
        
        if cursor_index <= len(self.input_content):
            # Insert character in the text_content string
            self.input_content = self.input_content[:cursor_index] + character + input_content[cursor_index:]
            self.cursor_position += 1  # Move the cursor forward
        
        self.needs_input_update = True

    def delete_character(self):
        # Method to delete a character at the cursor position
        pass

    def handle_key_down(self, e):
        if e.name == 'shift': #if shift is released
            self.shift_active = True
        if e.name == 'ctrl': #if shift is released
            self.control_active = True

    def handle_key_press(self, e):
        if len(e.name) == 1 and control_active == False:  # letter and number input
            if shift_active:
                char = keymaps.shift_mapping.get(e.name)
                self.input_content += char
            else:
                self.input_content += e.name
                
            self.cursor_position += 1
            self.needs_input_update = True

            # Check if adding the character exceeds the line length limit
            if self.cursor_position > self.chars_per_line:
                # Find the last space character before the line length limit
                last_space = input_content.rfind(' ', 0, chars_per_line)
                sentence = input_content[:last_space]
                # Append the sentence to the previous lines
                self.previous_lines.append(sentence)                

                # Update input_content to contain the remaining characters
                self.input_content = input_content[last_space + 1:]
                self.needs_display_update=True
                
            # Update cursor_position to the length of the remaining input_content
            self.cursor_position = len(input_content)                

        self.typing_last_time = time.time()
        self.needs_input_update = True

    def handle_interrupt(self, signal, frame):
      self.keyboard.unhook_all()
      epd.init()
      epd.Clear()
      exit(0)

    def run(self):
        self.epd.init()
        self.epd.Clear()
        self.keyboard.on_press(self.handle_key_down, suppress=False) #handles modifiers and shortcuts
        self.keyboard.on_release(self.handle_key_press, suppress=True)

        while True:
            if self.needs_display_update and not self.display_updating:
                self.update_display()
                self.needs_diplay_update=False
                self.typing_last_time = time.time()
                
            elif (time.time()-self.typing_last_time)<(.5): #if not doing a full refresh, do partials
                #the screen enters a high refresh mode when there has been keyboard input
                if not self.updating_input_area and self.scrollindex==1:
                    self.update_input_area()
