#!/bin/python
import argparse
import sys
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(
    prog='song-theme',
    description='Command Line utility for modyifying theme tags in OpenLyrics XML files.'
)

parser.add_argument('mode', choices=['add', 'rm'])
parser.add_argument('theme')
parser.add_argument('file_list', nargs='*', default=sys.stdin)

args = parser.parse_args()

MODE = args.mode
THEME = args.theme
try:
    file_list = args.file_list.read().strip().split("\n")
except:
    file_list = args.file_list

# print(file_list)



for file_name in file_list:
    tree = ET.parse(file_name)
    song = tree.getroot()
    properties = song.find("properties")
    
    
    # create <themes> element if it doesn't yet exist
    themes = properties.find("themes")
    if themes == None:
        themes = ET.SubElement(properties, "themes")

    current_themes = [x.text for x in themes] if len(themes) else []
    if MODE == "add" and THEME not in current_themes:
        theme = ET.SubElement(themes, "theme")
        theme.text = THEME
        print(f"Theme '{THEME}' added to {file_name}.")
    elif MODE == "rm":
        for theme in themes:
            if theme.text == THEME:
                print(f"Theme '{THEME}' removed from {file_name}.")
                themes.remove(theme)

    # ET.dump(song)
    tree.write(file_name, encoding='unicode')


# print(files)