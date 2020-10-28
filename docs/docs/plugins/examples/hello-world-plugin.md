# Hello World Plugin

This example shows you how to create a simple hello world plugin.

```python

from pretzel.api import register, Plugin

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
