from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from PIL import ImageTk

class MockEPD:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.is_initialized = False
        self.is_cleared = False
        self.is_sleeping = False
        self.displayed_image = None
        self.root = tk.Tk()
        self.root.title('Mock EPD Display')
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.photo = None  # Placeholder for the PhotoImage object

    def init(self):
        self.is_initialized = True

    def Clear(self):
        self.is_cleared = True
        # Create a white image to represent the cleared state
        self.displayed_image = Image.new('1', (self.width, self.height), 255)
        self.update_canvas()

    def sleep(self):
        self.is_sleeping = True

    def display(self, image):
        # Convert the bytes data back to a PIL image and update the canvas
        self.displayed_image = Image.frombytes('1', (self.width, self.height), image)
        self.update_canvas()

    def getbuffer(self, image):
        return image.tobytes()

    def update_canvas(self):
        # Convert the PIL image to a format that tkinter can use and update the canvas
        self.photo = ImageTk.PhotoImage(image=self.displayed_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.root.update_idletasks()
        self.root.update()

    # Add more methods as needed to mimic the real EPD class behavior
