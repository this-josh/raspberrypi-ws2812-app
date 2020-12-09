from rpi_ws281x import Color
import time

def tricolour(strip):
    """Wipe color across display a pixel at a time."""
    each_part = strip.numPixels() // 3
    print(each_part)
    for led in range(each_part):
        strip.setPixelColorRGB(led, 255, 0, 0)
        strip.setPixelColorRGB(led+each_part, 255, 255, 255)
        strip.setPixelColorRGB(led+(each_part*2), 0, 0, 255)
    strip.show()

def clear(strip):
    for led in range(strip.numPixels()):
        strip.setPixelColor(led, 0)
    strip.show()

def solid_colour(strip, colour):
    for led in range(strip.numPixels()):
        strip.setPixelColor(led, colour)
    strip.show()

def colour_flipper(num_in_block,colour_1, colour_2):
    in_this_block = 0
    while True:
        if in_this_block< num_in_block:
            in_this_block+=1
            yield colour_1
        else:
            in_this_block+=1
            yield colour_2
            if in_this_block >= 2*num_in_block:
                in_this_block=0

def block_wave(strip,wait_ms=20):
    # Red, Green, Gold
    colour_iter = colour_flipper(num_in_block=30, colour_1=Color(255,0,0), colour_2=Color(0,120,0))
    start = 0
    while True:
        start+=1
        for led in range(start, strip.numPixels()+start):
            led = led%strip.numPixels()
            strip.setPixelColor(led, next(colour_iter))
        strip.show()
        time.sleep(wait_ms/1000.0)
        if start >=strip.numPixels():
            start=0

def _pulse_brightness(strip, wait_ms):
    max_brightness = 200
    for brightness in range(0,max_brightness*2, 2):
        if brightness>200:
            brightness = abs(brightness-max_brightness*2)
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(wait_ms/1000.0)

def pulse(strip, colour1=None, colour2=None, wait_ms=10):
    colour1 = Color(255,0,0) if colour1 is None else colour1
    colour2 = Color(0,120,0) if colour2 is None else colour2
    while True:
        for led in range(strip.numPixels()):
            strip.setPixelColor(led, colour1)
        _pulse_brightness(strip, wait_ms)
        for led in range(strip.numPixels()):
            strip.setPixelColor(led, colour2)
        _pulse_brightness(strip, wait_ms)



def meet_in_the_middle(strip, wait_ms=20):
    """Both ends go towards the middle, then bounce back away"""
    num_leds = strip.numPixels()
    halfway = num_leds//2
    while True:
        for led in range(halfway):
            strip.setPixelColor(led, Color(255,0,0))
            strip.setPixelColor(num_leds-led, Color(0,255,0))
            strip.show()
            time.sleep(wait_ms/1000.0)
        for led in range(halfway,0,-1):
            strip.setPixelColor(led, Color(0,0,0))
            strip.setPixelColor(num_leds-led, Color(0,0,0))
            strip.show()
            time.sleep(wait_ms/1000.0)
