#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import subprocess

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib/pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import chia_stats
from waveshare_epd import epd7in5_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

def epaper_update():
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )


    line_gap_small = 20
    line_gap_big = 30
    line_top = 20

    c = chia_stats.get_chia_stats()

    try:
        logging.info("ChiChi E-Paper output starting")

        epd = epd7in5_V2.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()

        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)


        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        # draw.text((50, 20), 'Connected', font = font24, fill = 0)
        # draw.text((50, 50), 'IP: ' + str(IP), font = font24, fill = 0)
        # draw.text((50, 80), 'Total Gigs: 134GB', font = font24, fill = 0)
        # draw.text((50, 110), 'Plots Loaded: 154', font = font24, fill = 0)
        # draw.text((50, 140), 'Last time Eligible: ', font = font24, fill = 0)
        draw.text((50, 20), 'Net Space: ' + str(c.netspace), font = font24, fill = 0)
        draw.text((50, 20 + (line_gap_big*2)), 'My Space: ' + str(round(float(c.loaded_plot_tb), 2)) + "TiB", font = font24, fill = 0)
        draw.text((50, 20 + (line_gap_big*3)), 'Plots Loaded: ' + str(c.loaded_plot_count), font = font24, fill = 0)
        draw.text((50, 20 + (line_gap_big*4)), 'Avg Proof Lookup Time: ' + str(c.avg_proof_time()) + "s", font = font24, fill = 0)
        

        # draw.text((50, 200), 'Last win: ', font = font24, fill = 0)
        # draw.text((50, 230), 'Balance: ', font = font24, fill = 0)

        draw.text((550, line_top), '⊗ Loaded Drives', font = font24, fill = 0)
        for i, plot in enumerate(c.plot_dirs):
            draw.text((550, line_top + line_gap_big + (i*line_gap_small)), "✓ - " + plot, font = font18, fill = 0)
        

        Himage = Himage.rotate(180)

        epd.display(epd.getbuffer(Himage))
        time.sleep(2)
        """
        # Drawing on the Vertical image
        logging.info("2.Drawing on the Vertical image...")
        Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Limage)
        draw.text((2, 0), 'hello world', font = font18, fill = 0)
        draw.text((2, 20), '7.5inch epd', font = font18, fill = 0)
        draw.text((20, 50), u'微雪电子', font = font18, fill = 0)
        draw.line((10, 90, 60, 140), fill = 0)
        draw.line((60, 90, 10, 140), fill = 0)
        draw.rectangle((10, 90, 60, 140), outline = 0)
        draw.line((95, 90, 95, 140), fill = 0)
        draw.line((70, 115, 120, 115), fill = 0)
        draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
        draw.rectangle((10, 150, 60, 200), fill = 0)
        draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
        epd.display(epd.getbuffer(Limage))
        time.sleep(2)

        logging.info("3.read bmp file")
        Himage = Image.open(os.path.join(picdir, '7in5_V2.bmp'))
        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

        logging.info("4.read bmp file on window")
        Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        bmp = Image.open(os.path.join(picdir, '100x100.bmp'))
        Himage2.paste(bmp, (50,10))
        epd.display(epd.getbuffer(Himage2))
        time.sleep(2)

        logging.info("Clear...")
        epd.init()
        epd.Clear()

        logging.info("Goto Sleep...")
        epd.sleep()
        epd.Dev_exit()
        """
        
        # epd.Dev_exit()

    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd7in5.epdconfig.module_exit()
        exit()