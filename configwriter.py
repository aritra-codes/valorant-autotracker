from configparser import RawConfigParser
import constants as c

config = RawConfigParser()

config[c.VIDEO_SETTING_SECTION_NAME] = {
    "autoupload_videos": True,
    "firefox_profile_path": "C:/Users/Aritra/AppData/Roaming/Mozilla/Firefox/Profiles/pubangy1.selenium",
    "video_visibility": "unlisted",
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
    "spreadsheet_to_read": "google_sheets",
    "spreadsheet_format": "match_id,date_started,rank,mmr_change,rounds_won,rounds_lost,tracker_link,video_link,map,agent,kills,deaths,assists,headshot_percentage,average_damage_per_round",
    "insert_to_row_2": True,
    "write_to_excel_file": True,
    "excel_file_path": "valorant.xlsx",
    "write_to_google_sheets": True,
    "google_sheets_sheet_name": "Valorant Comp Matches",
    "google_service_account_key_json_path": "service_account_key.json"
}

with open(c.SETTINGS_FILE_NAME, "w") as file:
    config.write(file)