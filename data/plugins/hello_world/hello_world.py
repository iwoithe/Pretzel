# A simple demo of how to write a simple plugin for Pretzel

from api import utils, types

class HelloWorldPlugin(types.Plugin):
    name = "Hello World"
    version = "0.0.1"
    author = "iwoithe"
    description = "A simple Hello World plugin "

    def __init__(self, *args, **kwargs):
        pass

    def exec(self):
        print("Hello World!")

def register():
    classes = [HelloWorldPlugin]

    utils.register(classes)

def unregister():
    pass