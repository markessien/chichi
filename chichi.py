import os
import sys
import time
import glob
import json
import random
import asyncio
import logging
import argparse
import threading

from typing import List
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field

"""
DRIVE KEEP ALIVE FOR CHIA FARMING
"""

# Logging
log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

@dataclass
class Settings():
    directories: List[str] = field(default_factory=list)

    def as_json(self):
        return json.dumps({"directories" : settings.directories})

    def from_json(self, f):
        j = json.load(f)
        settings.directories = j["directories"]

settings = Settings()

def read_from_file(selected_file):

    # Get the filesize, so we can read a random offset
    file_size = Path(selected_file).stat().st_size

    # We will be reading 2 megabytes from the file
    two_mb = 2000000

    # Make sure file is greater than 2mb so we don't read more than we can chew
    if file_size > two_mb:

        # Get a random start offset
        start_offset = random.randint(0, file_size - two_mb)

        try:
            with open(selected_file, 'rb') as f:
                f.seek(start_offset)
                f.read(two_mb)

                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")

                print(current_time + " - Read " + selected_file[0:5] + "..." + selected_file[-10:])  # + data.decode("ascii", errors="ignore")[1:20]) <-- last bit can be used to check bytes
        except:
            print("File " + selected_file[-10:] + " is locked")

def xorinox_drivekeepalive():
    """
        Keeps external drives up by using the algorithm described
        by Xorinox. Every two seconds, a random file from the
        added folders is picked and a random offset read.
    """
    while True:
        
        # Loop over all directories
        for folder in settings.directories:

            file_list = glob.glob(os.path.join(folder, '*.plot')) # get all plot files 
            
            # Check if we have any plot files. If not, skip
            if len(file_list) == 0:
                continue

            # pick a random file index from result list
            file_nmbr = random.randint(0, len(file_list) - 1) 

            # And then select that file from the results
            selected_file = os.path.join(folder, file_list[file_nmbr])

            x = threading.Thread(target=read_from_file, args=(selected_file,))
            x.start()

        time.sleep(3)

def save_settings():
    """
        Save the settings back to the settings.json file
    """

    with open("./settings.json", "w") as f:
        f.write(settings.as_json())

def load_settings():
    """
        Load the saved settings from the settings.json file
    """
    random.seed()

    try:
        with open("./settings.json", "r") as f:
            settings.from_json(f)

    except:
        log.info("No settings file")

def add_directory(full_dir):
    
    # Use consistent final slash
    full_dir = os.path.join(full_dir, '')

    # Look if folder is already there
    for d in settings.directories:
        if d == full_dir:
            log.info("Folder already found")
            return

    settings.directories.append(full_dir)
    log.info("Added directory: %s", full_dir)
    save_settings()

if __name__ == '__main__':

    load_settings()

    parser = argparse.ArgumentParser(description='Helps keep external USB drives spinning')
    parser.add_argument("-d", "--dir", help='Add a directory')
    
    args = parser.parse_args()

    if args.dir:
        add_directory(args.dir)
    else:
        xorinox_drivekeepalive()
