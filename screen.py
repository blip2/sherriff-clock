import board
import time
import displayio
import framebufferio
import rgbmatrix
import adafruit_display_text.label
from adafruit_bitmap_font import bitmap_font

LARGE_FONT = bitmap_font.load_font("fonts/icl16x16u.bdf", displayio.Bitmap)
SMALL_FONT = bitmap_font.load_font("fonts/ie8x14u.bdf", displayio.Bitmap)

class Screen:
    display = None

    def __init__(self):
        displayio.release_displays()

        bit_depth = 2
        base_width = 32
        base_height = 16
        chain_across = 1
        tile_down = 4

        width = base_width * chain_across
        height = base_height * tile_down

        matrix = rgbmatrix.RGBMatrix(
            width=width, height=height, bit_depth=bit_depth,
            tile=tile_down, serpentine=False,
            rgb_pins=[board.GP2, board.GP3, board.GP4,
                    board.GP5, board.GP6, board.GP7],
            addr_pins=[board.GP8, board.GP9, board.GP10],
            clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13)

        self.display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False, rotation=90)

    def draw_time(self):
        self.hours = adafruit_display_text.label.Label(
            LARGE_FONT,
            color=0x008888,
            x=-1,
            y=10)
        
        colon = adafruit_display_text.label.Label(
            LARGE_FONT,
            color=0x008888,
            x=25,
            y=10,
            text=":")

        self.mins = adafruit_display_text.label.Label(
            LARGE_FONT,
            color=0x008888,
            x=33,
            y=10)

        self.message = adafruit_display_text.label.Label(
            SMALL_FONT,
            color=0x880000,
            x=48,
            y=24)
        
        g = displayio.Group()
        g.append(self.hours)
        g.append(colon)
        g.append(self.mins)
        g.append(self.message)
        self.display.show(g)

    def update(self):
        now = time.struct_time(time.localtime())
        self.hours.text = f"{now.tm_hour}"
        self.mins.text = f"{now.tm_min}"
        self.message.text = f"{now.tm_sec:02}"

    def scroll(self, line):
        line.x = line.x - 1
        line_width = line.bounding_box[2]
        if line.x < -line_width:
            line.x = self.display.width
