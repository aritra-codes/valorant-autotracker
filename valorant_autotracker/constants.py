from enum import Enum

from selenium_youtube.constants import Visibility


# Custom errors
class APIError(Exception):
    pass
class MatchNotFoundError(Exception):
    pass
class FirefoxProfileNotFoundError(Exception):
    pass
class VideoUploadError(Exception):
    pass
class InvalidGoogleServiceAccountKeyError(Exception):
    pass
class VideoDirectoryNotFoundError(Exception):
    pass


# Valorant
class Affinity(Enum):
    eu = "eu"
    na = "na"
    latam = "latam"
    br = "br"
    ap = "ap"
    kr = "kr"


# HenrikDev-API
VALORANT_API_DOMAIN = "https://api.henrikdev.xyz/valorant"
API_REQUEST_TIMEOUT = 60
def ACCOUNT_BY_NAME_URL(name: str, tag: str) -> str:
    return f"{VALORANT_API_DOMAIN}/v1/account/{"%20".join(name.split())}/{tag}"
def ACCOUNT_BY_PUUID_URL(puuid: str) -> str:
    return f"/valorant/v1/by-puuid/account/{puuid}"
def MATCHES_URL(puuid: str, affinity: Affinity) -> str:
    return f"{VALORANT_API_DOMAIN}/v3/by-puuid/matches/{affinity.value}/{puuid}"
def MMR_HISTORY_URL(puuid: str, affinity: Affinity) -> str:
    return f"{VALORANT_API_DOMAIN}/v1/by-puuid/lifetime/mmr-history/{affinity.value}/{puuid}"
VALORANT_DATE_FORMAT = r"%A, %B %d, %Y %I:%M %p"
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


# Google Sheets
SCOPE = scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]

# Settings
GENERAL_SETTING_SECTION_NAME = "GENERAL"
USE_GUI = (GENERAL_SETTING_SECTION_NAME, "use_gui")
USE_MDY_DATES_SETTING_LOCATOR = (GENERAL_SETTING_SECTION_NAME, "use_mdy_dates")
DEFAULT_NUMBER_OF_THREADS = (GENERAL_SETTING_SECTION_NAME, "default_number_of_threads")

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
WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "write_to_google_sheets")
GOOGLE_SHEETS_NAME_SETTING_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "google_sheets_sheet_name")
GOOGLE_SERVICE_ACCOUNT_KEY_JSON_PATH_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "google_service_account_key_json_path")
WRITE_TO_EXCEL_FILE_SETTING_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "write_to_excel_file")
EXCEL_FILE_PATH_SETTING_LOCATOR = (SPREADSHEET_SETTING_SECTION_NAME, "excel_file_path")

DEFAULT_SETTINGS = {
    GENERAL_SETTING_SECTION_NAME: {
        USE_GUI[1]: True,
        USE_MDY_DATES_SETTING_LOCATOR[1]: False
    },
    VIDEO_SETTING_SECTION_NAME: {
        AUTOUPLOAD_VIDEOS_SETTING_LOCATOR[1]: False,
        FIREFOX_PROFILE_SETTING_LOCATOR[1]: "",
        BACKGROUND_PROCESS_SETTING_LOCATOR[1]: True,
        MAX_VIDEOS_SIMULTANEOUSLY_SETTING_LOCATOR[1]: 2,
        VIDEO_VISIBILITY_SETTING_LOCATOR[1]: "private",
        AUTOSELECT_VIDEOS_SETTING_LOCATOR[1]: False,
        VIDEO_DIRECTORY_SETTING_LOCATOR[1]: "",
        RECORDING_CLIENT_SETTING_LOCATOR[1]: "",
        FILENAME_FORMAT_SETTING_LOCATOR[1]: "",
        RECORDING_START_DELAY_SETTING_LOCATOR[1]: 0
    },
    VALORANT_SETTING_SECTION_NAME: {
        PUUID_SETTING_LOCATOR[1]: "",
        AFFINITY_SETTING_LOCATOR[1]: "",
        LATEST_MATCH_ID_SETTING_LOCATOR[1]: ""
    },
    SPREADSHEET_SETTING_SECTION_NAME: {
        SPREADSHEET_FORMAT_LOCATOR[1]: "match_id,date_started,rank,mmr_change,rounds_won,rounds_lost,tracker_link,video_link,map,agent,kills,deaths,assists,headshot_percentage,average_damage_per_round",
        INSERT_TO_ROW_2_LOCATOR[1]: False,
        WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR[1]: False,
        GOOGLE_SHEETS_NAME_SETTING_LOCATOR[1]: "",
        GOOGLE_SERVICE_ACCOUNT_KEY_JSON_PATH_LOCATOR[1]: "",
        WRITE_TO_EXCEL_FILE_SETTING_LOCATOR[1]: False,
        EXCEL_FILE_PATH_SETTING_LOCATOR[1]: ""
    }
}


# UI
LABEL_DICT_KEY = "label"
WIDGET_DICT_KEY = "widget"
INITIAL_VALUE_DICT_KEY = "initial_value"
VALIDATE_FUNCTION_DICT_KEY = "validate_function"
SAVE_FUNCTION_DICT_KEY = "save_function"
DISABLE_FUNCTION_DICT_KEY = "disable_function"

DEFAULT_COLOR_THEME = "dark-blue"
DEFAULT_FONT = ("Calibri", 14)

APP_TITLE = "Valorant AutoTracker"
SETTINGS_TITLE = "Settings"
SPREADSHEET_FORMAT_SETTINGS_TITLE = "Settings (Spreadsheet Format)"

MAIN_WINDOW_RESOLUTION = "1000x700"
SETTINGS_WINDOW_RESOLUTION = "840x660"
SPREADSHEET_FORMAT_SETTINGS_WINDOW_RESOLUTION = "500x680"

IMAGES_FOLDER_PATH = "valorant_autotracker/images"
LOGO_IMAGE_PATH = f"{IMAGES_FOLDER_PATH}/logo.ico"
QUESTION_IMAGE_PATH = {"light": f"{IMAGES_FOLDER_PATH}/question_mark.png",
                       "dark": f"{IMAGES_FOLDER_PATH}/question_mark_dark.png"}
FOLDER_IMAGE_PATH = f"{IMAGES_FOLDER_PATH}/folder.png"
FIND_IMAGE_PATH = {"light": f"{IMAGES_FOLDER_PATH}/find.png",
                   "dark": f"{IMAGES_FOLDER_PATH}/find_dark.png"}
SAVE_IMAGE_PATH = f"{IMAGES_FOLDER_PATH}/save_file.png"
RESET_IMAGE_PATH = f"{IMAGES_FOLDER_PATH}/reset.png"
RUN_IMAGE_PATH = {"light": f"{IMAGES_FOLDER_PATH}/run.png",
                  "dark": f"{IMAGES_FOLDER_PATH}/run_dark.png"}
SETTINGS_IMAGE_PATH = {"light": f"{IMAGES_FOLDER_PATH}/settings.png",
                       "dark": f"{IMAGES_FOLDER_PATH}/settings_dark.png"}
GITHUB_IMAGE_PATH = f"{IMAGES_FOLDER_PATH}/github.png"
RETURN_IMAGE_PATH = f"{IMAGES_FOLDER_PATH}/return.png"
PENCIL_IMAGE_PATH = f"{IMAGES_FOLDER_PATH}/pencil.png"


RECORDING_CLIENT_FILENAME_FORMATS = {
    "": "",
    "custom": "",
    "insights_capture": r"VALORANT %m-%d-%Y_%H-%M-%S-%f.mp4",
    "medal": r"MedalTVValorant%Y%m%d%H%M%S.mkv",
    "outplayed": r"Valorant_%m-%d-%Y_%H-%M-%S-%f.mp4"
}
RECORDING_CLIENT_OPTIONS = {
    "": "-",
    "custom": "Custom",
    "insights_capture": "Insights Capture",
    "medal": "Medal",
    "outplayed": "Outplayed"
}
VIDEO_VISIBILITY_OPTIONS = {
    Visibility.public.name: "Public",
    Visibility.private.name: "Private",
    Visibility.unlisted.name: "Unlisted"
}
REGION_OPTIONS = {
    "": "-",
    Affinity.eu.name: "Europe (EU)",
    Affinity.na.name: "North America (NA)",
    Affinity.latam.name: "Latin America (LATAM)",
    Affinity.br.name: "Brazil (BR)",
    Affinity.ap.name: "Southeast Asia/Asia-Pacific (AP)",
    Affinity.kr.name: "Korea (KR)"
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
