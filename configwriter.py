from configparser import RawConfigParser
import constants as c

config = RawConfigParser()

config[c.VIDEO_SETTING_PROFILE_NAME] = {
    "video_directory": c.INSIGHTS_DIRECTORY,
    "filename_format": c.INSIGHTS_FILENAME_FORMAT,
    "firefox_profile_path": "C:/Users/Aritra/AppData/Roaming/Mozilla/Firefox/Profiles/pubangy1.selenium"
}

config[c.VALORANT_SETTING_PROFILE_NAME] = {
    "puuid": "f356715e-1c24-58e8-b77b-40af0cd03bda",
    "affinity": "eu"
}

config[c.GOOGLE_SHEETS_SETTING_PROFILE_NAME] = {
    "sheet_name": "Valorant Comp Matches",
    "service_account_key_json_path": "service_account_key.json"
}

with open(c.SETTINGS_FILE_NAME, "w") as file:
    config.write(file)