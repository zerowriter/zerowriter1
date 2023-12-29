from PIL import Image, ImageDraw, ImageFont

class MockEPD:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.is_initialized = False
        self.is_cleared = False
        self.is_sleeping = False
        self.displayed_image = None

    def init(self):
        self.is_initialized = True

    def Clear(self):
        self.is_cleared = True
        # Create a white image to represent the cleared state
        self.displayed_image = Image.new('1', (self.width, self.height), 255)

    def sleep(self):
        self.is_sleeping = True

    def display(self, image):
        # Convert the bytes data back to a PIL image and show it
        self.displayed_image = Image.frombytes('1', (self.width, self.height), image)
        self.displayed_image.show('mock_display_output.png')

    def getbuffer(self, image):
        return image.tobytes()

    # Add more methods as needed to mimic the real EPD class behavior
