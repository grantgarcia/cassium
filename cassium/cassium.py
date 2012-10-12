from __future__ import print_function

import glob
import imp
import os
import re
import sys
import traceback
from threading import Timer
try:
    import cPickle as pickle
except ImportError:
    import pickle

from ircbot import SingleServerIRCBot
from irclib import nm_to_n

# Attempt to get configuration from the current directory
try:
    import config as cfg
except ImportError:
    cfg = None

class Cassium(SingleServerIRCBot):
    """
    """

    plugins = []

    def __init__(self, config=None):
        # config must be given if the import above failed
        if config: cfg = config
        elif not cfg: raise AttributeError("no configuration found")
        # initialize the IRC bot
        SingleServerIRCBot.__init__(self, [(cfg.server, cfg.port)], cfg.nick,
            cfg.realname)
        # import plugins
        for plugin in cfg.autoload:
            self.load_plugin(plugin)

    def load_plugin(self, plugin):
        """Loads or reloads a plugin."""
        # Import the plugin
        this_plugin = __import__(plugin)
        # Search for an existing copy of the plugin
        for i, plugin in enumerate(self.plugins):
            if this_plugin.__name__ == plugin.__name__:
                self.plugins[i] = this_plugin
                print("Reloaded " + this_plugin.__name__)
                break
        # No existing copy found
        else:
            self.plugins.append(this_plugin)
            print("Imported " + this_plugin.__name__)