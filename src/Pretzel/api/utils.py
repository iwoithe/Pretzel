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


import json

def register(classes: list) -> bool:
    """ :param classes: The classes to register.
        :type classes: list

        This registers the given classes. It returns a boolean value that represents
        whether or not registering was successful or not

        You will find a list of plugins that Pretzel knows about in 'settings.json'
        The plugin info is stored in a dictionary. It looks like below:

            "Plugins": [
                {
                    "Name": "Notes Dock",
                    "Registered": false,
                    "File Path": "data/plugins/notesdock/notesdockplugin.py"
                },
                {
                    "Name": "Hello World",
                    "Registered": true,
                    "File Path": "data/plugins/helloworld/helloworldplugin.py
                }
            ]

        See documentation for more help. """

    with open("data/settings.json", "r") as f:
        settings = json.loads(f.read())

    for cls in classes:
        cls.register()

        settings["Plugins"].append(
            {
                "Name": cls.name,
                "Registered": False,
                "File Path": cls.file_path
            }
        )

        with open("data/settings.json", "w") as f:
            json.dump(settings, f, indent=4)

        return True

def unregister(classes: list) -> bool:
    """
    :param classes: The classes to unregister.

    This returns a boolean value that represents whether or not
    unregistering was successful or not """

    for cls in classes:
        pass