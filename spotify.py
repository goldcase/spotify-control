#!/usr/bin/python

import subprocess, datetime

__author__ = "Johnny Chang"
NAME = "Johnny"

def write_to_log(string):
    """
    Writes to log with current time.
    """
    with open("spotify.log", "a") as f:
        f.write("{0}:\t{1}\n".format(datetime.datetime.now(), string))

class switch(object):
    """
    Class to emulate switch statements.
    """
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """
        Return the match method once.
        """
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

def check_and_open_spotify():
    """
    Opens Spotify if it isn't already open.
    """
    out = subprocess.check_output(['osascript', '-e', 'application "Spotify" is running'])
    if out == "false":
        subprocess.call(['osascript', '-e', 'tell application "Spotify" to activate'])
        write_to_log("OPENED SPOTIFY")

def help_message():
    """
    Returns available commands.
    """
    return """The available commands are:
        help (you know this already)
        play
        pause
        skip
        next
        previous
        count current
        output current
        louder
        softer
        mute
        unmute
        """

def tell_spotify(this):
    """
    Wrapper around certain commands for Spotify.
    play, pause, skip, etc.
    """
    check_and_open_spotify()

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
            break
        if case("louder"):
            break
        if case("softer"):
            break
        if case("mute"):
            break
        if case("unmute"):
            break
#        if case("shuffle"):
#            spotify_do.format("shuffling enabled")
#            break

    subprocess.call(command, shell=True)
    write_to_log("EXECUTED `{0}` ON REQUEST `{1}`".format(command, this))

print "Hello, {0}. Anything you want me to do today?\n".format(NAME)

while 1:
    cmd = raw_input("Enter your command, or `help` if you don't know anything: \n").lower()
    if cmd == "help":
        print help_message()
    else:
        tell_spotify(cmd)
