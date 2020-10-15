# chichi
A small tool to keep external USB drives spinning. Useful for space farming.

Usage:

# To add a new folder
python chichi.py -d "folder/path"

python chichi.py -d "E:\ChiaFarm"

You can also edit the settings.json file and add all folders there directly. This is how it looks like:

{"directories": ["f:\\ChiaFarm\\", "g:\\ChiaFarm\\", "h:\\ChiaFarm\\", "i:\\ChiaFarm\\"]}

Use double backslashes, not single.

# To start spinning all drives
python chichi.py

