
import time, threading

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

"""
OUTPUT ON AN SSD1306 LCD. 
Probably needs raspberry pi.
"""

class LCDScreen(object):


    def init_lcd(self):
        # Raspberry Pi pin configuration:
        RST = None     # on the PiOLED this pin isnt used

        self.cur_text = "Idle"

        # Note the following are only used with SPI:
        DC = 23
        SPI_PORT = 0
        SPI_DEVICE = 0

        # 128x32 display with hardware I2C:
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

        # Initialize library.
        self.disp.begin()

        # Clear display.
        self.disp.clear()
        self.disp.display()

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        self.width = self.disp.width
        self.height = self.disp.height

        self.thread = threading.Thread(target=LCDScreen.screen_routine, args=(self,))
        self.thread.start()

    @staticmethod
    def screen_routine(screen_obj):
        
        print("Entered ")
        image = Image.new('1', (screen_obj.width, screen_obj.height))
        draw = ImageDraw.Draw(image)
        screen_obj.font = ImageFont.load_default()

        while True:
 
            # print("Draw loop:" + screen_obj.cur_text)
            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, screen_obj.width, screen_obj.height), outline=0, fill=0)

            draw.text((0, 5), screen_obj.cur_text, font=screen_obj.font, fill=255)

            screen_obj.disp.image(image)
            screen_obj.disp.display()
            time.sleep(1)

    def print_on_lcd(self, text):
        self.cur_text = text





