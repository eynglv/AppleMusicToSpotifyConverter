#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 21:15:49 2020

@author: elvyyang
"""

from credentials import refresh_token, base_64
import requests
import json

class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64
    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": refresh_token},
                                 headers={"Authorization": "Basic " + base_64})
        response_json = response.json()

        return response_json["access_token"]
    
token = Refresh()
token.refresh()
        