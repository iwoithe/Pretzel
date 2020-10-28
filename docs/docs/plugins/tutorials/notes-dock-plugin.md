# Note Dock Plugin

## Introduction

This tutorial shows you how to create a note dock plugin for Pretzel.

## Note

If you want this plugin and can't be bothered to follow this tutorial, you can find the completed plugin in ``data/plugins/notesdock/notesdockplugin.py`` from which you can install it.

## Planning

For all plugins, it is a good idea to plan out what you are going to create before you start.

This plugin will add a notes dock where you can write notes for any reason. You can also write a todo list in it. The content can be in either plain text or Markdown and is automatically saved to a file under ``data`` in the Pretzel directory.

## Writing the Plugin

With Pretzel's API, you can use *any* third party package from PyPi. This opens up many opportunities for plugins.

To begin with, create a new file called ``notedockplugin.py``. Next, add the following code to import the required libraries.

```python

from PyQt5 import uic
from PyQt5.QtWidgets import QDockWidget

from pretzel.api.types import Plugin
from pretzel.api.utils import register

```

Note that we imported Pretzel's API by using ``from pretzel.api ...`` - not ``from pretzel ...``. This is so that you can access Pretzel's internal code. For example, if you want to use the ``Menu``'s utility methods, simply type ``from pretzel.ui.menu.utils import fill_widget``. As another example, if you want to use the item's model (if you don't understand what that is, don't worry as I will write api documentation not just for Pretzel's API, but for the entire code base), simply import ``from core.models.items import ItemModel``. It's really that easy!


Next, we'll add the skeleton code for the ``NotesDockPlugin`` class.

```python

class NotesDockPlugin(Plugin, QDockWidget):

	name = "Notes Dock Plugin"
	version = "0.0.1"
	author = "iwoithe"
	description = "Adds a dock where you can write notes, create a todo list. Either write in plain text or markdown."
	
	def __init__(self, *args, parent=None, **kwargs):
		super().__init__(*args, **kwargs)
		
		if parent:
			self.parent = parent
	
	def setup(self):
		""" This method sets up the GUI """
		pass
	
	def exec(self):
		""" This method runs the plugin"""
		pass
	
	def register(self):
		""" Use this method to create any required configuration files """
		pass
	
	def unregister(self):
		""" Use this method to delete any configuration files """
		pass

```


```python

from pretzel.api.types import Plugin
from pretzel.api.utils import register

class HelloWorld(Plugin):
	
	name = "Hello World Plugin"
	version = "0.0.1"
	author = "iwoithe"
	description = "A simple hello world plugin for Pretzel."
	warning = "This example may change at any time as the api is not currently stable."

	def __init__(self, *args, parent=None, **kwargs):
		super().__init__(*args, **kwargs)
		
		if parent:
			self.parent = parent
		
		self.exec()
	
	def exec(self):
		print("Hello World!")
		
	def register(self):
		""" Use this method to create any configuration files etc. """
		pass
	
	def unregister(self):
		""" Use this method to undo what you say in register """
		pass


# Create an instance of the plugin
hello_world_plugin = HelloWorld()

# Register the plugin
register(classes=[hello_world_plugin])

```

=== "Python 2"

	```python2
	print "Hello World"
	```

=== "Python 3"
	
	```python3
	print("Hello World")
	```
