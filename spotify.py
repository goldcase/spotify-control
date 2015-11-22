#!/usr/bin/python

import os, datetime

__author__ = "Johnny Chang"

def write_to_log(string):
    with open("spotify.log", "a") as f:
        f.write("{0}:\t{1}".format(datetime.datetime.now(), string))

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once."""
        yield self.match
        raise StopIteration

    def match(self, *args):
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

def tell_spotify(this):
    spotify_do = """osascript -e 'tell application "Spotify" to {0}'"""
    for case in switch(this):
        if case("play"):
            command = spotify_do.format("play")
            break
        if case("pause"):
            command = spotify_do.format("pause")
            break
        if case("skip") or case("next"):
            command = spotify_do.format("next track")
            break
        if case("previous"):
            command = spotify_do.format("previous track")
            break
        if case("count current"):
            command = spotify_do.format("played count of current track")
            break
        if case("output current"):
            command = spotify_do.format("set output to name of current track & \" by \" & artist of current track")
#        if case("shuffle"):
#            spotify_do.format("shuffling enabled")
#            break

    os.system(command)
    write_to_log("EXECUTED `{0}` ON REQUEST `{1}`".format(command, this))

tell_spotify("skip")
