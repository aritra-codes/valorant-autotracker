from configparser import RawConfigParser
import constants as c

config = RawConfigParser()

config[c.VIDEO_SETTING_SECTION_NAME] = {
    "autoupload_videos": True,
    "firefox_profile_path": "C:/Users/Aritra/AppData/Roaming/Mozilla/Firefox/Profiles/pubangy1.selenium",
    "autoselect_videos": True,
    "video_directory": c.INSIGHTS_DIRECTORY,
    "filename_format": c.INSIGHTS_FILENAME_FORMAT,
    "recording_start_delay": 0
}

config[c.VALORANT_SETTING_SECTION_NAME] = {
    "puuid": "f356715e-1c24-58e8-b77b-40af0cd03bda",
    "region": "eu"
}

config[c.SPREADSHEET_SETTING_SECTION_NAME] = {
    "sheet_name": "Valorant Comp Matches",
    "service_account_key_json_path": "service_account_key.json",
    "spreadsheet_format": "match_id,date_started,rank,mmr_change,rounds_won,rounds_lost,tracker_link,video_link,map,agent,kills,deaths,assists,headshot_percentage,average_damage_per_round"
}

with open(c.SETTINGS_FILE_NAME, "w") as file:
    config.write(file)