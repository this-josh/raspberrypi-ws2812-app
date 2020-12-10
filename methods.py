from rpi_ws281x import Color, PixelStrip
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def setup_strip():
    global LED_BRIGHTNESS
    global pulse_on
    global block_wave_on
    global meet_in_the_middle_on
    pulse_on = False
    block_wave_on = False
    meet_in_the_middle_on = False
    # LED strip configuration:
    LED_COUNT = 300  # Number of LED pixels.
    LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10  # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = (
        False  # True to invert the signal (when using NPN transistor level shift)
    )
    LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
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
    strip.begin()
    clear_strip(strip)
    return strip


def tricolour(strip):
    """Wipe color across display a pixel at a time."""
    each_part = strip.numPixels() // 3
    print(each_part)
    for led in range(each_part):
        strip.setPixelColorRGB(led, 255, 0, 0)
        strip.setPixelColorRGB(led + each_part, 255, 255, 255)
        strip.setPixelColorRGB(led + (each_part * 2), 0, 0, 255)
    strip.show()


def clear_strip(strip):
    print("clear_striping strip")
    for led in range(strip.numPixels()):
        strip.setPixelColor(led, 0)
    strip.show()


def solid_colour(strip, colour):
    for led in range(strip.numPixels()):
        strip.setPixelColor(led, colour)
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
    while block_wave_on:
        start += 1
        for led in range(start, strip.numPixels() + start):
            led = led % strip.numPixels()
            strip.setPixelColor(led, next(colour_iter))
        strip.show()
        time.sleep(wait_ms / 1000.0)
        if start >= strip.numPixels():
            start = 0


def _pulse_brightness(strip, wait_ms):
    max_brightness = 200
    for brightness in range(0, max_brightness * 2, 2):
        if brightness > 200:
            brightness = abs(brightness - max_brightness * 2)
        strip.setBrightness(brightness)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def pulse(strip, colour1=None, colour2=None, wait_ms=10):
    clear_strip(strip)
    colour1 = Color(255, 0, 0) if colour1 is None else colour1
    colour2 = Color(0, 120, 0) if colour2 is None else colour2
    logger.debug("pulse option")
    logger.debug(colour1)
    logger.debug(colour2)
    while pulse_on:
        print("loop")
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
    while meet_in_the_middle_on:
        for led in range(halfway):
            strip.setPixelColor(led, colour1)
            strip.setPixelColor(num_leds - led, colour2)
            strip.show()
            time.sleep(wait_ms / 1000.0)
        for led in range(halfway, 0, -1):
            strip.setPixelColor(led, Color(0, 0, 0))
            strip.setPixelColor(num_leds - led, Color(0, 0, 0))
            strip.show()
            time.sleep(wait_ms / 1000.0)


def which_method(which_true, strip):
    global pulse_on
    global block_wave_on
    global meet_in_the_middle_on
    if which_true == "pulse":
        pulse_on = True
        block_wave_on = False
        meet_in_the_middle_on = False
    elif pulse_on is True and which_true != "pulse":
        strip.setBrightness(LED_BRIGHTNESS)
    if which_true == "colour_wave":
        pulse_on = False
        block_wave_on = True
        meet_in_the_middle_on = False
    elif which_true == "meet_in_middle":
        print("which, method meet in middle")
        pulse_on = False
        block_wave_on = False
        meet_in_the_middle_on = True
    else:
        pulse_on = False
        block_wave_on = False
        meet_in_the_middle_on = False
        clear_strip(strip)
