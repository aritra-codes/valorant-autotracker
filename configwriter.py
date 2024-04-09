from configparser import ConfigParser
import constants as c

config = ConfigParser()

config["RECORDING"] = {
    "video_directory": c.INSIGHTS_DIRECTORY
}

with open(c.SETTINGS_FILE_NAME, "w") as file:
    config.write(file)