from configparser import RawConfigParser
import constants as c

config = RawConfigParser()

config[c.VIDEO_SETTING_SECTION_NAME] = {
    "autoupload_videos": True,
    "firefox_profile_path": "C:/Users/Aritra/AppData/Roaming/Mozilla/Firefox/Profiles/pubangy1.selenium",
    "max_videos_simultaneously": 2,
    "video_visibility": "unlisted",
    "autoselect_videos": True,
    "video_directory": "C:/Users/Aritra/Videos/Overwolf/Insights Capture",
    "recording_client": "insights_capture",
    "filename_format": c.RECORDING_CLIENT_FILENAME_FORMATS["insights_capture"],
    "recording_start_delay": 0
}

config[c.VALORANT_SETTING_SECTION_NAME] = {
    "puuid": "f356715e-1c24-58e8-b77b-40af0cd03bda",
    "region": "eu",
    "latest_match_id": "a889e40d-872f-4f41-93be-077eb2fff489"
}

config[c.SPREADSHEET_SETTING_SECTION_NAME] = {
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