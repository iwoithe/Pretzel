import os.path
import easysettings

from Pretzel.core.paths import *
from Pretzel.core import database


settings = easysettings.load_json_settings(settings_file)


def exists(file: str) -> bool:
    """ Checks if the file (or directory) exists

    :param file: the file or directory
    :type file: str

    :return: bool """

    if os.path.exists(file):
        return True
    else:
        return False


def create_file(file: str, content=None):
    with open(file, mode="x"):
        pass

    if content:
        with open(file, mode="w") as f:
            f.write(content)


def create_dir(dir: str):
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass


def init_dirs():
    # TODO: Wrap in a if exists() block?
    # The base directories (avoid the FileNotFoundError)
    base = os.path.join(dirs.user_data_dir, "../../")
    create_dir(base)
    base2 = os.path.join(dirs.user_data_dir, "../")
    create_dir(base2)
    # The directories
    create_dir(dirs.user_data_dir)
    # Databases dir
    create_dir(database_dir)
    # Logging dir
    create_dir(log_dir)

    return


def init_files():
    # Settings
    if not os.path.exists(settings_file):
        settings_text = read_default_settings()
        create_file(settings_file, content=settings_text)

    # Database
    settings.set("Database Path", database_file)
    settings.save()
    database.init.initialize_databases(path=database_file)

    # Logging
    if not os.path.exists(log_file):
        create_file(log_file)

    return