""" Provides current series tracking model """

import ConfigParser
import os


class CurrentSeries(object):
    """ Tracks the currently selected series """

    SETTINGS_FILE = os.path.join(os.getenv('HOME'), '.play_next')

    def __init__(self):
        """ Loads the settings from the file """
        # The settings are stored in a dict internally, which makes it easy to
        # filter the lines in the settings file.
        self.settings = {
            'show': None,
            'episode': None
        }
        with open(self.SETTINGS_FILE) as settings:
            for line in settings:
                name, value = [e.strip() for e in line.split('=', 1)]
                if name in self.settings:
                    self.settings[name] = value if len(value) else None

    def get_show(self):
        """ The show folder, containing all episodes (directly or indirectly) """
        return self.settings['show']

    def get_episode(self):
        """ The current episode file """
        return self.settings['episode']

    def set_show(self, show):
        """ Set the show folder """
        self.settings['show'] = show

    def set_episode(self, episode):
        """ Set the current episode """
        self.settings['episode'] = episode

    def get_episode_list(self):
        """ All episodes reachable """
        # It may be appropriate to turn this into a generator, but that would
        # prevent sorting.
        if self.get_show() is None:
            raise Exception('Cannot produce episode list, show currently unset')

        return sorted([
            os.path.join(d, f)
            for (d, _, files) in os.walk(self.get_show())
            for f in files
        ])

    def find_previous(self):
        """ Look one episode back.
            Returns None when moving past the start of the list """
        if self.get_episode() is None:
            return self.get_episode_list()[-1]

        last_episode = None
        for episode in self.get_episode_list():
            if episode == self.get_episode():
                return last_episode
            last_episode = episode

        raise Exception("Cannot find {episode} in {show}".format(**self.settings))

    def find_next(self):
        """ Look one episode forwards.
            Returns None when moving past the end of the list """
        if self.get_episode() is None:
            return self.episode_list()[0]

        next_episode = False
        for episode in self.get_episode_list():
            if next_episode:
                return episode
            if episode == self.get_episode():
                next_episode = True
        if next_episode:
            return None

        raise Exception("Cannot find {episode} in {show}".format(**self.settings))

    def go_previous(self):
        """ Move one episode backwards. """
        self.settings['episode'] = self.find_previous()

    def go_next(self):
        """ Move one episode forwards. """
        self.settings['episode'] = self.find_next()

    def write(self):
        """ Writes the current state back to the settings file """
        with open(self.SETTINGS_FILE, 'w') as settings:
            for (name, value) in self.settings.items():
                if value is None:
                    settings.write("{name} =\n".format(name=name))
                else:
                    settings.write("{name} = {value}\n".format(name=name, value=value))

# vim: set ai et sw=4 syntax=python :
