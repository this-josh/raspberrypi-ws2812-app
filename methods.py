from rpi_ws281x import *

def tricolour(strip, num_leds: int):
    """Wipe color across display a pixel at a time."""
    each_part = num_leds // 3

    for led in range(each_part):
        strip.setPixelColorRGB(led, 255, 0, 0)
        strip.setPixelColorRGB(led+each_part, 255, 255, 255)
        strip.setPixelColorRGB(led+(each_part*2), 0, 0, 255)

