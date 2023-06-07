import board
import displayio
import framebufferio
import rgbmatrix
import adafruit_display_text.label
from adafruit_bitmap_font import bitmap_font

font = bitmap_font.load_font("fonts/LeagueSpartan-Bold-16.bdf", displayio.Bitmap)

class Screen:
    display = None

    def __init__(self):
        displayio.release_displays()

        bit_depth = 3
        base_width = 32
        base_height = 16
        chain_across = 1
        tile_down = 4

        width = base_width * chain_across
        height = base_height * tile_down

        matrix = rgbmatrix.RGBMatrix(
            width=width, height=height, bit_depth=bit_depth,
            tile=tile_down, serpentine=False,
            rgb_pins=[board.GP2, board.GP4, board.GP6,
                    board.GP3, board.GP5, board.GP7],
            addr_pins=[board.GP12, board.GP11, board.GP10],
            clock_pin=board.GP9, latch_pin=board.GP8, output_enable_pin=board.GP13)

        self.display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False, rotation=90)

    def draw_text(self):
        self.line1 = adafruit_display_text.label.Label(
            font,
            color=0x330033,
            text="23:02")
        self.line1.x = 3
        self.line1.y = 17

        g = displayio.Group()
        g.append(self.line1)
        self.display.show(g)

    def scroll(self, line):
        line.x = line.x - 1
        line_width = line.bounding_box[2]
        if line.x < -line_width:
            line.x = self.display.width
