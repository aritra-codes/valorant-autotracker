from enum import Enum

from selenium.webdriver.common.by import By

# HenrikDev-API
PUUID = "f356715e-1c24-58e8-b77b-40af0cd03bda"
AFFINITY = "eu"
VALORANT_API_DOMAIN = "https://api.henrikdev.xyz/valorant"
def ACCOUNT_URL(name: str, tag: str) -> str:
    return f"{VALORANT_API_DOMAIN}/v1/account/{"%20".join(name.split())}/{tag}"
def MATCHES_URL(puuid: str, affinity: str) -> str:
    return f"{VALORANT_API_DOMAIN}/v3/by-puuid/matches/{affinity}/{puuid}"
def MMR_HISTORY_URL(puuid: str, affinity: str) -> str:
    return f"{VALORANT_API_DOMAIN}/v1/by-puuid/lifetime/mmr-history/{affinity}/{puuid}"
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

# Google Sheets
SHEET_NAME = "Valorant Comp Matches"
KEY_FILE_NAME = "service_account_key.json"
SCOPE = scope = ['https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]

# Recording clients
INSIGHTS_DIRECTORY = "C:/Users/Aritra/Videos/Overwolf/Insights Capture"
INSIGHTS_FILENAME_FORMAT = r"VALORANT %m-%d-%Y_%H-%M"

# Selenium
TIMEOUT = 60
class Visibility(Enum):
    PUBLIC: str = "public"
    PRIVATE: str = "private"
    UNLISTED: str = "unlisted"
VIDEO_UPLOAD_LOCATOR = (By.XPATH, '//*[@id="content"]/input')
TITLE_FIELD_LOCATOR = (By.XPATH, '//ytcp-video-title//div[@id="textbox"]')
DESCRIPTION_FIELD_LOCATOR = (By.XPATH, '//ytcp-video-description//div[@id="textbox"]')
NOT_FOR_KIDS_RADIO_LOCATOR = (By.XPATH, '//tp-yt-paper-radio-button[@name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')
NEXT_BUTTON_LOCATOR = (By.ID, "next-button")
SAVE_BUTTON_LOCATOR = (By.ID, "done-button")
CLOSE_BUTTON_LOCATOR = (By.ID, "close-button")
def VISIBILITY_RADIO_LOCATOR(visibility: Visibility) -> tuple[str, str]:
    return (By.XPATH, f'//tp-yt-paper-radio-button[@name="{visibility.name}"]')
UPLOAD_PROGRESS_LOCATOR = (By.XPATH, '//span[@class="progress-label style-scope ytcp-video-upload-progress"]')
LINK_ANCHOR_LOCATOR = (By.XPATH, '//a[@class="style-scope ytcp-video-info"]')

SETTINGS_FILE_NAME = "settings.ini"
