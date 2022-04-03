#!/usr/bin/env python3

import board
import time
import neopixel

OFF = (0,0,0)
RED = (255,0,0)

#
# Computes a rainbow color after: http://mines.lumpylumpy.com/Electronics/Computers/Software/Cpp/Algorithms/Convert/Colour/index.php#.VroN01jhCUm. Red and blue are just shifted versions of this.
def getGreen(ratio):
    if ratio < 0:
        return 0
    if ratio > 1:
        return 255
    if ratio < 0.1667:
        return int(255 * 6 * ratio)
    if ratio < 0.5:
        return int(255)
    if ratio < 0.6667:
        return int(255*(4-6*ratio))
    return int(0)

def getRed(ratio):
    return getGreen(ratio+0.3333)
def getBlue(ratio):
    return getGreen(ratio-0.3333)

def getRainbowColor(ratio):
    """Computes a color of the rainbow along a spectrum from 0 (red) to 1 (violet)"""
    return (getRed(ratio), getGreen(ratio), getBlue(ratio))

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(len(strip)):
        strip[i] = color
        strip.show()
        time.sleep(wait_ms / 1000.0)

def cylon(strip, color=RED, width=3, wait_ms=50):
    """Send a set of lights back and forth on the display"""
    end=len(strip) - width
    if end <= 0:
        return

    #
    # Start by turning on width pixels
    for j in range(0, width):
        strip[j] = color
    left_pix = 0
    right_pix = width

    #
    # Loop, turning off the first pixel and turning on the last pixel
    # This is the left-to right loop
    while right_pix < len(strip):

        #
        # Look at it for a wee bit
        time.sleep(wait_ms/1000.0)
        #
        # Off and on at the ends
        strip[left_pix] = OFF
        strip[right_pix] = color
        strip.show()
        #
        # Move to the next pixel
        left_pix = left_pix + 1
        right_pix = right_pix + 1

    while left_pix >= 0:

        #
        # Move to the next pixel (we went one beyond on the l-to-r loop, so we decrement
        # at the top of this loop.
        left_pix = left_pix - 1
        right_pix = right_pix - 1
        #
        # Look at it for a wee bit
        time.sleep(wait_ms/1000.0)
        #
        # Off and on at the ends
        strip[right_pix] = OFF
        strip[left_pix] = color
        strip.show()

def rainbow_ratio(strip, n):
    return float(n) / float(len(strip))

def rainbow_cylon(strip, width=3, wait_ms=50):
    """Send a set of lights back and forth on the display"""
    end=len(strip) - width
    if end <= 0:
        return
    #
    # Start by turning on width pixels
    for j in range(0, width):
        strip[j] = getRainbowColor(rainbow_ratio(strip, j))
    left_pix = 0
    right_pix = width

    #
    # Loop, turning off the first pixel and turning on the last pixel
    # This is the left-to right loop
    while right_pix < len(strip):

        #
        # Look at it for a wee bit
        time.sleep(wait_ms/1000.0)
        #
        # Off and on at the ends
        strip[left_pix] = OFF
        strip[right_pix] = getRainbowColor(rainbow_ratio(strip, right_pix))
        strip.show()

        #
        # Move to the next pixel
        left_pix = left_pix + 1
        right_pix = right_pix + 1

    while left_pix > 0:

        #
        # Move to the next pixel (we went one beyond on the l-to-r loop, so we decrement
        # at the top of this loop.
        left_pix = left_pix - 1
        right_pix = right_pix - 1
        #
        # Look at it for a wee bit
        time.sleep(wait_ms/1000.0)
        #
        # Off and on at the ends
        strip[right_pix] = OFF
        strip[left_pix] = getRainbowColor(rainbow_ratio(strip, left_pix))
        strip.show()

# Main program logic follows:
if __name__ == '__main__':
    
    # LED strip configuration:
    LED_COUNT = 35        # Number of LED pixels.

    # Create NeoPixel object with appropriate configuration.
    strip1 = neopixel.NeoPixel(board.GP0, 38, auto_write=False)
    strip2 = neopixel.NeoPixel(board.GP1, 35, auto_write=False)
    strip1.brightness = 0.05
    strip2.brightness = 0.05
    while True:
        rainbow_cylon(strip1, 4)
        rainbow_cylon(strip2, 4)
