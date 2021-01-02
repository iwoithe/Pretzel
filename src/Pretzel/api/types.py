#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2020 iwoithe <iwoithe@just42.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


# NOTE: The API will change over time. Maintaining plugins
#       will require testing on all released versions of
#       Pretzel.


class Plugin(object):
    """
    The base class of all plugins

    :param name: The name of the plugin
    :type name: str
    :param version: The version of the plugin
    :type version: tuple
    :param author: The author of the plugin
    :type author: str
    :param description: The description of the plugin
    :type description: str
    :param shortcuts: The shortcuts for the plugin
    :type shortcuts: list
    :param README: The (relative) file path to the readme of the plugin
    :type REAMDE: str
    :param file_path: The file path of the plugin
    :type file_path: str

    """

    name = "Plugin"
    version = (0, 0, 1)
    author = "Plugin Author"
    description = "Plugin description"
    shortcuts = []
    README = None

    # This is the easiest way for Pretzel to get the file path. You need to add this line here
    # in every Pretzel plugin.
    file_path = __file__

    def __init__(self, *args, **kwargs):
        pass

    def setup(self):
        """ Creates the GUI etc. """
        pass

    def exec(self):
        """ What the plugin runs
            Note: Not every plugin needs an ``exec()`` method """
        pass

    def register(self):
        """ Create any configuration files required """
        pass

    def unregister(self):
        """ Deletes any configuration files """
        pass


class Operator(Plugin):
    """ The operator class will be used for the command palette (once it has been implemented) """
    def __init__(self, *args, **kwargs):
        pass