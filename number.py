import board
import time
import neopixel

class Number(object):

    def __init__(self, len1, len2, color=(255,0,0), brightness=0.25):
        self.strip1 = neopixel.NeoPixel(board.GP0, len1, auto_write=False)
        self.strip2 = neopixel.NeoPixel(board.GP1, len2, auto_write=False)
        self.color = color
        self.brightness = brightness
        self.strip1.brightness = brightness
        self.strip1.fill(color)
        self.strip2.brightness = brightness
        self.strip2.fill(color)

    def set_color(self, color):
        self.color = color
        self.strip1.fill(color)
        self.strip2.fill(color)

    def step(self):
        pass
        
    def show(self):
        self.strip1.show()
        self.strip2.show()

    def clear(self):
        self.set_color((0, 0, 0))
        self.show()
            

class FadeNumber(Number):

    def __init__(self, len1, len2, color=(255,0,0), bright_step=0.1, max_brightness=0.25, min_brightness=0):
        Number.__init__(self, len1, len2, color, brightness=0)
        self.bright_step = bright_step
        self.max_brightness = max_brightness
        self.min_brightness = min_brightness

    def step(self):
        if self.brightness <= self.min_brightness:
            self.brightness = self.min_brightness
            self.bright_step = -self.bright_step
        elif self.brightness >= self.max_brightness:
            self.brightness = self.max_brightness
            self.bright_step = -self.bright_step
            
        self.brightness = self.brightness + self.bright_step
        self.strip1.brightness = self.brightness
        self.strip2.brightness = self.brightness
        
