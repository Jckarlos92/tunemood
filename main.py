#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import tagger
import random
import urllib2
import json
import handler
import sign_log
from sign_log import make_secure_val
from google.appengine.ext import db

def check_secure_val(h):
    """
    h: string of format: string|HASH
    returns: string part of given string
    """
    v = h.rsplit('|')[0]
    if h == make_secure_val(v):
        return v
        
class FrontPage(handler.Handler):
    def check_login(self):
        self.a = None
        user = self.request.cookies.get('user_id')
        checked_user = None
        if user:
            checked_user = check_secure_val(user)

        if checked_user:
            user_key = db.Key.from_path('User', int(checked_user))
            self.a = db.get(user_key)

    def get(self):

        self.check_login()
        email = ""
        if self.a:
            email = "Welcome: " + self.a.email

        self.render('prueba.html',user=email)
        
    def post(self):

        self.check_login()
        email = ""
        if self.a:
            email = "Welcome: " + self.a.email

        self.feel_input = self.request.get('feel_input')

        flag = True
        artist_len = 0
        #error shown in case no artist was found
        error = ""
        song_id = ""

        if self.feel_input == "":
            flag = False

        if flag:
            mood_input =  self.feel_input.replace(" ", "+")

            #request and save the response from echonest
            response = urllib2.urlopen('http://developer.echonest.com/api/v4/song/search?api_key=IZOYQ4QQOLHDEGQPK&style=' + mood_input +
                                             '&results=20')

            #reads the content from the response from the url
            content = response.read()
            #decodes the json data and loads it to the data varialbe
            data = json.loads(content.decode("utf8"))

            #length of the artist list return fmor echonest
            artist_len = len(data['response']['songs'])

        if artist_len > 0 and flag:

            data_groov = list()

            while len(data_groov) == 0:

                #generates a random number to select through the dict
                rand_artist = random.randint(0,artist_len - 1)

                #get the artist name frmo the data dict return from the json decoder
                artist_name = data['response']['songs'][rand_artist]['artist_name'].replace(" ", "+")

                #use the tiny song api to request a url
                tiny_song_url = "http://tinysong.com/s/"+artist_name+"?format=json&limit=32&key=d18513f29750be3e771446c3b87e4f4d"

                #get the response from the tiny song api url
                response_groov = urllib2.urlopen(tiny_song_url)

                #read the response from tiny song
                content_groov = response_groov.read()

                #decode the json string and make it a dictionary
                data_groov = json.loads(content_groov)

                if len(data_groov) > 0:

                    #generates a random index for selecting a song
                    rand_song = random.randint(0, len(data_groov) - 1)

                    #gets the grooveshark songID
                    song_id = data_groov[rand_song]['SongID'];

        else:
            error = "No se encontraron canciones"
        
        self.render('prueba.html', song_id = song_id, error = error, user = email);
        

app = handler.webapp2.WSGIApplication([
    ('/', FrontPage),
    ('/signup', sign_log.SignUp),
    ('/login', sign_log.Login),
    ('/logout', sign_log.Logout),
    ('/tag', tagger.Tag),
    (r'/.*',  sign_log.Confirmation),
], debug=True)
