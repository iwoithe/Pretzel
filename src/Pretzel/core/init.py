import os.path


def init_logging():
    if not os.path.exists("data/debug.log"):
        with open("data/debug.log", mode="x"):
            pass

    return