# A simple demo of how to write a simple plugin for Pretzel

def register(parent=None):
    if parent:
        print("Hello World!")
    else:
        print("No parent... plugin won't be embedded into Pretzel")
