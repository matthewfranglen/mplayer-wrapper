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

    subprocess.call(['mplayer', episode])

def do_back():
    """ Moves back one video """
    series = CurrentSeries()
    series.go_previous()
    series.write()

def do_set():
    """ Set the current directory as the source of videos """
    series = CurrentSeries()
    series.set_show(os.getcwd())
    series.set_episode(None)
    series.write()

# vim: set ai et sw=4 syntax=python :
