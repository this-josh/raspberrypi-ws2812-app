from rpi_ws281x import Color, PixelStrip
import time
import logging
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# constants
LED_COUNT = 300  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


def setup_strip():
    global LED_BRIGHTNESS
    global which_effect
    which_effect = False
    # LED strip configuration:
    strip = PixelStrip(
        LED_COUNT,
        LED_PIN,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        LED_CHANNEL,
    )
    # Intialize the library (must be called once before other functions).
    logger.debug(f"Setting up strip")
    strip.begin()
    clear_strip(strip)
    colour_wipe(strip, Color(255, 0, 0), wait_ms=2, force=True)
    colour_wipe(strip, Color(0, 0, 0), wait_ms=2, force=True)
    return strip


def tricolour(strip, **kwargs):
    """Wipe color across display a pixel at a time."""
    each_part = strip.numPixels() // 3
    logger.debug(each_part)
    for led in range(each_part):
        strip.setPixelColorRGB(led, 255, 0, 0)
        strip.setPixelColorRGB(led + each_part, 255, 255, 255)
        strip.setPixelColorRGB(led + (each_part * 2), 0, 0, 255)
    strip.show()


def clear_strip(strip):
    logger.debug("clear_striping strip")
    for led in range(strip.numPixels()):
        strip.setPixelColor(led, 0)
    strip.show()


def solid_colour(strip, colour1, **kwargs):
    for led in range(strip.numPixels()):
        strip.setPixelColor(led, colour1)
    strip.show()


def colour_flipper(num_in_block, colour_1, colour_2):
    in_this_block = 0
    while True:
        if in_this_block < num_in_block:
            in_this_block += 1
            yield colour_1
        else:
            in_this_block += 1
            yield colour_2
            if in_this_block >= 2 * num_in_block:
                in_this_block = 0


def block_wave(strip, colour1=None, colour2=None, wait_ms=20):
    colour1 = Color(255, 0, 0) if colour1 is None else colour1
    colour2 = Color(0, 120, 0) if colour2 is None else colour2
    clear_strip(strip)
    logger.debug(colour1)
    logger.debug(colour2)

    colour_iter = colour_flipper(num_in_block=30, colour_1=colour1, colour_2=colour2)
    start = 0
    while which_effect == "colour_wave":
        start += 1
        for led in range(start, strip.numPixels() + start):
            if which_effect != "colour_wave":
                return
            led = led % strip.numPixels()
            strip.setPixelColor(led, next(colour_iter))
        strip.show()
        time.sleep(wait_ms / 1000.0)
        if start >= strip.numPixels():
            start = 0


def _pulse_brightness(strip, wait_ms):
    max_brightness = 200
    for brightness in range(0, max_brightness * 2, 2):
        if which_effect != "pulse":
            return
        if brightness > 200:
            brightness = abs(brightness - max_brightness * 2)
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def pulse(strip, colour1=None, colour2=None, wait_ms=10):
    #! problem if user changes colour
    clear_strip(strip)
    colour1 = Color(255, 0, 0) if colour1 is None else colour1
    colour2 = Color(0, 120, 0) if colour2 is None else colour2
    logger.debug("pulse option")
    logger.debug(colour1)
    logger.debug(colour2)
    while which_effect == "pulse":
        logger.debug("loop")
        for led in range(strip.numPixels()):
            strip.setPixelColor(led, colour1)
        _pulse_brightness(strip, wait_ms)
        for led in range(strip.numPixels()):
            strip.setPixelColor(led, colour2)
        _pulse_brightness(strip, wait_ms)


def meet_in_the_middle(strip, colour1=None, colour2=None, wait_ms=20):
    """Both ends go towards the middle, then bounce back away"""
    clear_strip(strip)
    colour1 = Color(255, 0, 0) if colour1 is None else colour1
    colour2 = Color(0, 120, 0) if colour2 is None else colour2
    logger.debug(colour1)
    logger.debug(colour2)

    num_leds = strip.numPixels()
    halfway = num_leds // 2
    while which_effect == "meet_in_middle":
        for led in range(halfway):
            strip.setPixelColor(led, colour1)
            strip.setPixelColor(num_leds - led, colour2)
            if which_effect != "meet_in_middle":
                return
            strip.show()
            time.sleep(wait_ms / 1000.0)
        for led in range(halfway, 0, -1):
            strip.setPixelColor(led, Color(0, 0, 0))
            strip.setPixelColor(num_leds - led, Color(0, 0, 0))
            if which_effect != "meet_in_middle":
                return

            strip.show()
            time.sleep(wait_ms / 1000.0)


def colour_wipe(strip, colour1, wait_ms=50, force: bool = False, **kwargs):
    """Wipe color across display a pixel at a time."""
    logger.debug(f"Colour wipe, colour = {colour1}, delay = {wait_ms}")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, colour1)
        if which_effect != "colour_wipe" and not force:
            clear_strip(strip)
            return
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theater_chase(strip, colour1, wait_ms=50, **kwargs):
    """Movie theater light style chaser animation."""
    while which_effect == "theater_chase":
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, colour1)
            if which_effect != "theater_chase":
                return
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, **kwargs):
    """Draw rainbow that fades across all pixels at once.

    Think of a rainbow wave
    """
    while which_effect == "rainbow":
        for j in range(256):
            # Ensure each led takes all 255 colours
            for i in range(strip.numPixels()):
                # Set the  colour for each led in this iter
                strip.setPixelColor(i, wheel((i + j) & 255))
            if which_effect != "rainbow":
                return
            strip.show()
            time.sleep(wait_ms / 1000.0)


def rainbow_cycle(strip, wait_ms=20, **kwargs):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    while which_effect == "rainbow_cycle":
        for j in range(256):
            for i in range(strip.numPixels()):
                strip.setPixelColor(
                    i, wheel((int(i * 256 / strip.numPixels()) + j) & 255)
                )
            if which_effect != "rainbow_cycle":
                return
            strip.show()
            time.sleep(wait_ms / 1000.0)


def theater_chase_rainbow(strip, wait_ms=50, **kwargs):
    """Rainbow movie theater light style chaser animation."""
    while which_effect == "theater_chase_rainbow":
        for j in range(256):
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, wheel((i + j) % 255))
                if which_effect != "theater_chase_rainbow":
                    return
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)


def twinkle_one_led(strip, colour1, wait_ms=20):
    while which_effect == "twinkle_one_led":
        print("twinkle")
        this_led = random.randrange(0, LED_COUNT)
        print(this_led)
        strip.setPixelColor(this_led, colour1)
        strip.show()
        strip.setPixelColour(this_led, Color(0, 0, 0))
        time.sleep(wait_ms / 1000.0)


def which_method(which_true, strip):
    global which_effect

    if which_effect == "pulse" and which_true != "pulse":
        # If we are about to change from pulse, reset brightness.
        logger.debug(f"Setting brightness to {LED_BRIGHTNESS}")
        strip.setBrightness(LED_BRIGHTNESS)

    logger.debug(f"setting which_effect to {which_true}")
    which_effect = which_true
    if which_effect == "clear_strip":
        clear_strip(strip)
