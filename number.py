import board
import time
import neopixel

class Number(object):

    def __init__(self, len1, len2, color=(255,0,0), brightness=0.25):
        self.strips = (neopixel.NeoPixel(board.GP0, len1, auto_write=False),
                       neopixel.NeoPixel(board.GP1, len2, auto_write=False))
        self.color = color
        self.brightness = brightness
        self.strips[0].brightness = brightness
        self.strips[0].fill(color)
        self.strips[1].brightness = brightness
        self.strips[1].fill(color)

    def set_color(self, color):
        self.color = color
        self.strips[0].fill(color)
        self.strips[1].fill(color)

    def step(self):
        pass
        
    def show(self):
        self.strips[0].show()
        self.strips[1].show()

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
        self.strips[0].brightness = self.brightness
        self.strips[1].brightness = self.brightness

class StepState():
    def __init__(self, strip, width, color):
        self.strip = strip
        self.width = width
        self.color = color
        self.left_pix = -width
        self.right_pix = -1
        self.dir = 0

    def step(self):
        if self.dir == 0:
            #
            # Left to right
            if self.left_pix >= 0:
                self.strip[self.left_pix] = (0,0,0)
            self.left_pix = self.left_pix+1
            self.right_pix = self.right_pix+1
            for i in range(self.left_pix,self.right_pix):
                if i >= 0 and i < len(self.strip):
                    self.strip[i] = self.color
            if self.left_pix >= len(self.strip):
                self.left_pix = len(self.strip)
                self.right_pix = len(self.strip) + self.width
                self.dir = 1
                
        else:
            #
            # Right to left. Thank goodness Python is less verbose than Java.
            if self.right_pix >= 0 and self.right_pix < len(self.strip):
                self.strip[self.right_pix] = (0,0,0)
            self.left_pix = self.left_pix-1
            self.right_pix = self.right_pix-1
            for i in range(self.left_pix, self.right_pix):
                if i >= 0 and i < len(self.strip):
                    self.strip[i] = self.color
            if self.right_pix <= 0:
                self.right_pix = -1
                self.left_pix = -self.width
                self.dir = 0
            

class ChaseNumber(Number):
    def __init__(self, len1, len2, color=(255,0,0), width=5, brightness=0.25):
        Number.__init__(self, len1, len2, color=color, brightness=brightness)
        self.width = width
        self.states = (StepState(self.strips[0], width, color),
                       StepState(self.strips[1], width, color))

    def step(self):
        self.states[0].step()
        self.states[1].step()
        
