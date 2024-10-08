from configparser import RawConfigParser, NoSectionError, NoOptionError
import os

import valorant_autotracker.constants as c

APP_DATA_PATH = os.getenv("APPDATA")
APP_SETTINGS_DIR = os.path.join(APP_DATA_PATH, "aritra-codes/Valorant AutoTracker")
os.makedirs(APP_SETTINGS_DIR, exist_ok=True)

SETTINGS_INI_PATH = os.path.join(APP_SETTINGS_DIR, c.SETTINGS_INI_FILENAME)

class InvalidSettingsError(Exception):
    pass

def init_config() -> RawConfigParser:
    config = RawConfigParser()
    files = config.read(SETTINGS_INI_PATH)

    if not files:
        make_default_settings_file(c.DEFAULT_SETTINGS)

        print("Settings file not found. A new settings file with the default settings has been created.")
    
        config.read(SETTINGS_INI_PATH)

    return config

def get_setting(section: str, name: str, integer: bool=False, floatp: bool=False, boolean: bool=False) -> str | int | float | bool:
    config = init_config()

    c_kwargs = {"section": section, "option": name}

    try:
        if integer:
            return config.getint(**c_kwargs)
        if floatp:
            return config.getfloat(**c_kwargs)
        if boolean:
            return config.getboolean(**c_kwargs)

        return config.get(**c_kwargs)
    except (NoSectionError, NoOptionError) as e:
        raise InvalidSettingsError(f"'{name}' setting not found. Please check and save your settings.") from e
    except ValueError as e:
        raise InvalidSettingsError(f"'{name}' setting is not valid. Please check and save your settings.") from e

def edit_setting(section: str, name: str, value: str | int | float | bool) -> None:
    config = init_config()

    config.set(section, name, value)

    with open(SETTINGS_INI_PATH, "w", encoding="utf-8") as file:
        config.write(file)

def delete_setting(section: str, name: str) -> None:
    config = init_config()
    
    config.remove_option(section, name)

    with open(SETTINGS_INI_PATH, "w", encoding="utf-8") as file:
        config.write(file)

def make_default_settings_file(settings: dict[str, dict[str, str | int | float | bool]]) -> None:
    config = RawConfigParser()

    for section, section_settings in settings.items():
        config[section] = section_settings

    with open(SETTINGS_INI_PATH, "w", encoding="utf-8") as file:
        config.write(file)