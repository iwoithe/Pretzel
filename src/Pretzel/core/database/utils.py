import easysettings

from Pretzel.core.paths import settings_file


def get_database_path():
    settings = easysettings.load_json_settings(settings_file)
    path = settings.get("Database Path")
    return path
