""" Provides the control methods for the player """

import os
import subprocess

from .models import CurrentSeries

def do_play():
    """ Plays the next video """
    series = CurrentSeries()
    episode = series.get_episode()
    series.go_next()
    series.write()

    if episode is None:
        print "Unable to play, no available video"
    else:
        subprocess.call(['mplayer', episode])

def do_back():
    """ Moves back one video """
    series = CurrentSeries()
    series.go_previous()

    if series.get_episode() is None:
        print "Unable to move back, at first episode"
    else:
        series.write()

def do_set():
    """ Set the current directory as the source of videos """
    series = CurrentSeries()
    series.set_show(os.getcwd())
    series.go_first()
    series.write()

# vim: set ai et sw=4 syntax=python :
