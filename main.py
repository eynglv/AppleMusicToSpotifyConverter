#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 19:40:00 2020

@author: elvyyang
"""


'''
Step 1: Parse through Library.xml to get {song_name:artist}
Step 2: return xml to Json
Step 3: Open login Spotify
Step 4: search for song
Step 5: add song to spotify library ("liked songs")
'''

import json 
import requests
import ast
from xmlToDict import fileName as file
from credentials import spotify_user_id
from refresh import Refresh


class saveSongs:
    def __init__(self):
        self.spotify_id = spotify_user_id
        self.spotify_token = ""
        
    def callRefresh(self):
        refreshCaller = Refresh()
        self.spotify_token = refreshCaller.refresh()

    def find_spotify_id_from_json(self):
        global failure
        failure = []
        idArray={}
        idList = []
        
        with open(file,'r') as reader:
            contents = reader.read()
            fileDict = ast.literal_eval(contents)
        
        for i in fileDict:
            song_id = saveSongs.findSongs(self, i, fileDict[i])
            if song_id == None:
                failure.append(i)
            else:
                idList.append(song_id)
    
        idArray["ids"] = idList
            
        fileName = "song_to_id.json"
        with open(fileName, "w") as write_file:
            json.dump(idArray, write_file)
        
        failureText = "failure.json"
        with open(failureText, "w") as write_file:
            json.dump(failure, write_file)
        
    
        saveSongs.runSaveTracks(self,idArray)
        
    def findSongs(self, song_name, artist):
        query = "https://api.spotify.com/v1/search?query={}+{}&type=track&offset=0&limit=20".format(
            song_name,
            artist 
        )
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_token)
            }
        )
        response_json = response.json()
        try:
            songs = response_json["tracks"]["items"] 
            song_id = songs[0]["id"]
            return song_id
        except:
            failure.append(song_name)
            #failed songs
                
        
    def runSaveTracks (self, idArray):
        #saveTracks query has a limit of 50 songs
        ind2 = 50 
        ind1 = 0
        while ind2<len(idArray["ids"]):
            saveSongs.saveTracks(self, idArray["ids"][ind1:ind2])
            ind1+=50
            ind2+=50
            
    def saveTracks(self, idArray):
        query = "https://api.spotify.com/v1/me/tracks"
        request_data = json.dumps(idArray)
        try: 
            response = requests.put(
                query,
                data=request_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(self.spotify_token)
                }
            )
            response_json = response.json()
            return response_json
        except:
            print (response.text)



         
save_Songs = saveSongs()
save_Songs.callRefresh()
save_Songs.find_spotify_id_from_json()



