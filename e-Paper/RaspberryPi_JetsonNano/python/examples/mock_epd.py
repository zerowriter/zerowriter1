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

    def sleep(self):
        self.is_sleeping = True

    def display(self, image):
        self.displayed_image = image

    def getbuffer(self, image):
        return image.tobytes()

    # Add more methods as needed to mimic the real EPD class behavior
