import easysettings


def get_database_path():
    settings = easysettings.load_json_settings("data/settings.json")
    path = settings.get("Database Path")
    return path
