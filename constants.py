from selenium.webdriver.common.by import By

# Custom errors
class APIError(Exception):
    pass
class FirefoxProfileNotFoundError(Exception):
    pass
class VideoUploadError(Exception):
    pass
class InvalidGoogleServiceAccountKeyError(Exception):
    pass
class VideoDirectoryNotFoundError(Exception):
    pass
class InvalidSettingsError(Exception):
    pass

# HenrikDev-API
VALORANT_API_DOMAIN = "https://api.henrikdev.xyz/valorant"
def ACCOUNT_BY_NAME_URL(name: str, tag: str) -> str:
    return f"{VALORANT_API_DOMAIN}/v1/account/{"%20".join(name.split())}/{tag}"
def ACCOUNT_BY_PUUID_URL(puuid: str) -> str:
    return f"/valorant/v1/by-puuid/account/{puuid}"
def MATCHES_URL(puuid: str, affinity: str) -> str:
    return f"{VALORANT_API_DOMAIN}/v3/by-puuid/matches/{affinity}/{puuid}"
def MMR_HISTORY_URL(puuid: str, affinity: str) -> str:
    return f"{VALORANT_API_DOMAIN}/v1/by-puuid/lifetime/mmr-history/{affinity}/{puuid}"
VALORANT_DATE_FORMAT = r"%A, %B %d, %Y %I:%M %p"
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

# Google Sheets
SCOPE = scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]

# Selenium
TIMEOUT = 60
UPLOAD_POLL_FREQUENCY = 60
VIDEO_UPLOAD_LOCATOR = (By.XPATH, '//*[@id="content"]/input')
TITLE_FIELD_LOCATOR = (By.XPATH, '//ytcp-video-title//div[@id="textbox"]')
DESCRIPTION_FIELD_LOCATOR = (By.XPATH, '//ytcp-video-description//div[@id="textbox"]')
NOT_FOR_KIDS_RADIO_LOCATOR = (By.XPATH, '//tp-yt-paper-radio-button[@name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')
NEXT_BUTTON_LOCATOR = (By.ID, "next-button")
SAVE_BUTTON_LOCATOR = (By.ID, "done-button")
CLOSE_BUTTON_LOCATOR = (By.ID, "close-button")
def VISIBILITY_RADIO_LOCATOR(visibility: str) -> tuple[str, str]:
    return (By.XPATH, f'//tp-yt-paper-radio-button[@name="{visibility.upper()}"]')
UPLOAD_PROGRESS_LOCATOR = (By.XPATH, '//span[@class="progress-label style-scope ytcp-video-upload-progress"]')
LINK_ANCHOR_LOCATOR = (By.XPATH, '//a[@class="style-scope ytcp-video-info"]')

# Settings
SETTINGS_FILE_PATH = "settings.ini"
VIDEO_SETTING_SECTION_NAME = "VIDEO"
AUTOUPLOAD_VIDEOS_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "autoupload_videos")
FIREFOX_PROFILE_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "firefox_profile_path")
BACKGROUND_PROCESS_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "background_process")
MAX_VIDEOS_SIMULTANEOUSLY_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "max_videos_simultaneously")
VIDEO_VISIBILITY_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "video_visibility")
AUTOSELECT_VIDEOS_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "autoselect_videos")
VIDEO_DIRECTORY_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "video_directory")
RECORDING_CLIENT_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "recording_client")
FILENAME_FORMAT_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "filename_format")
RECORDING_START_DELAY_SETTING_LOCATOR = (VIDEO_SETTING_SECTION_NAME, "recording_start_delay")

VALORANT_SETTING_SECTION_NAME = "VALORANT"
PUUID_SETTING_LOCATOR = (VALORANT_SETTING_SECTION_NAME, "puuid")
AFFINITY_SETTING_LOCATOR = (VALORANT_SETTING_SECTION_NAME, "region")
LATEST_MATCH_ID_SETTING_LOCATOR = (VALORANT_SETTING_SECTION_NAME, "latest_match_id")

SPREADSHEET_SETTING_SECTION_NAME = "SPREADSHEET"
SPREADSHEET_FORMAT_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "spreadsheet_format")
INSERT_TO_ROW_2_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "insert_to_row_2")
WRITE_TO_EXCEL_FILE_SETTING_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "write_to_excel_file")
EXCEL_FILE_PATH_SETTING_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "excel_file_path")
WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "write_to_google_sheets")
GOOGLE_SHEETS_NAME_SETTING_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "google_sheets_sheet_name")
GOOGLE_SERVICE_ACCOUNT_KEY_JSON_PATH_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "google_service_account_key_json_path")

# UI
RECORDING_CLIENT_FILENAME_FORMATS = {
    "insights_capture": r"VALORANT %m-%d-%Y_%H-%M-%S-%f.mp4",
    "medal": r"placeholder.mp4",
    "outplayed": r"placeholder.mp4"
}
RECORDING_CLIENT_OPTIONS = {
    "": "Custom",
    "insights_capture": "Insights Capture",
    "medal": "Medal",
    "outplayed": "Outplayed"
}
VIDEO_VISIBILITY_OPTIONS = {
    "public": "Public",
    "private": "Private",
    "unlisted": "Unlisted"
}
REGION_OPTIONS = {
    "eu": "Europe (EU)",
    "na": "North America (NA)",
    "latam": "Latin America (LATAM)",
    "br": "Brazil (BR)",
    "ap": "Southeast Asia/Asia-Pacific (AP)",
    "kr": "Korea (KR)"
}
SPREADSHEET_FORMAT_OPTIONS = {
    "": "-",
    "match_id": "Match ID",
    "date_started": "Date Started",
    "rank": "Rank",
    "mmr_change": "MMR Change",
    "rounds_won": "Rounds Won",
    "rounds_lost": "Rounds Lost",
    "tracker_link": "Tracker Link",
    "video_link": "Video Link",
    "map": "Map",
    "agent": "Agent",
    "kills": "Kills",
    "deaths": "Deaths",
    "assists": "Assists",
    "headshot_percentage": "Headshot %",
    "average_damage_per_round": "ADR"
}
