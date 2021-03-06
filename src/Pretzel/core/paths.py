import os
import appdirs


app_name = "Pretzel"
version = "0.0.1"


dirs = appdirs.AppDirs(appname=app_name, version=version, roaming=True)
data_dir = dirs.user_data_dir

# Specific files
settings_file = os.path.join(data_dir, "settings.json")
# Database
database_dir = os.path.join(data_dir, "Databases")
# TODO: Decide on final name on the default database (data, default or pretzel)
database_file = os.path.join(database_dir, "pretzel.db")
# Logging
log_dir = os.path.join(data_dir, "Logs")
log_file = os.path.join(log_dir, "debug.log")


def read_default_settings(file: str = "data/pretzel/default_settings.json") -> str:
    """ Reads and returns the settings"""
    with open(file) as f:
        text = f.read()

    return text
