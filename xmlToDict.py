#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 10:51:32 2020

@author: elvyyang
"""
'''
Converts library data from xml to json
Json file represents {song_name: artist}
'''

import json
from bs4 import BeautifulSoup
import re

song_info={}
library = "Library.xml"
with open(library) as fp:    
    soup = BeautifulSoup(fp, "lxml-xml")
    songCompList = []
    for value in soup.find_all("key"):
        artistList = []
        if value.get_text() == "Name":
            song_name = value.next_sibling.get_text()
            if "(feat" in song_name:
                ind = song_name.index("(feat")
                song_name = song_name[:ind]
            for k in song_name.split("\n"):
                song_name = " ".join(re.findall(r"[a-zA-Z0-9]+", k))
            songCompList.append(song_name)
        elif value.get_text() == "Artist":
            artist = value.next_sibling.get_text()
            artistList.append(artist)
            try:
                song_info[songCompList[-1]] = artistList[0]
            except:
                pass
    # try:
    #     song_info.pop("Lemonade Film")
    # except:
    #     pass

fileName = "song_to_artist.json" 
with open(fileName, "w") as write_file:
    json.dump(song_info, write_file)
                
#is it necessary to have a Chinese/foreign language parser? ace

    




    


    
    
    


