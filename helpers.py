from os import listdir
from datetime import datetime, timedelta
import sys
from typing import NoReturn, Literal
import threading
from time import sleep

import gspread
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet as GoogleWorksheet
from oauth2client.service_account import ServiceAccountCredentials
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet as ExcelWorksheet
import requests
from configparser import RawConfigParser
from tkinter import filedialog, messagebox
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException

import constants as c
import selenium_youtube

def get_excel_workbook(path: str) -> Workbook:
    workbook = load_workbook(path)

    return workbook

def insert_row_to_excel_sheet(workbook: Workbook, path: str, row: int, values: list) -> None:
    sheet: ExcelWorksheet = workbook.active
    sheet.insert_rows(row)

    sheet._current_row = row - 1
    sheet.append(values)

    workbook.save(path)

def append_row_to_excel_sheet(workbook: Workbook, path: str, values: list) -> None:
    sheet: ExcelWorksheet = workbook.active
    sheet.append(values)

    workbook.save(path)

def get_google_sheet(name: str) -> Spreadsheet:
    creds = ServiceAccountCredentials.from_json_keyfile_name(get_setting(*c.GOOGLE_SERVICE_ACCOUNT_KEY_JSON_PATH_LOCATOR), c.SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(name)

    return sheet

def get_latest_match_id() -> str:
    return get_setting(*c.LATEST_MATCH_ID_SETTING_LOCATOR)
    
def update_latest_match_id(match_id: str) -> None:
    edit_setting(*c.LATEST_MATCH_ID_SETTING_LOCATOR, match_id)

def manage_henrikdev_api_errors(status_code: int) -> Literal[True] | NoReturn:
    match status_code:
        case 200:
            return True
        case 400:
            sys.exit("Request error by the client. Make sure you have set a valid PUUID and region in the settings.")
        case 403:
            sys.exit("Forbidden to connect to the Riot API (most likely due to maintenance reasons). Please try again later.")
        case 404:
            sys.exit("Player not found, invalid puuid. Make sure you have set a valid PUUID and region in the settings.")
        case 408:
            sys.exit("Timeout while fetching riot data. Please try again.")
        case 410:
            sys.exit("Endpoint is deprecated. Please contact the developer.")
        case 429:
            sys.exit("Rate limit reached. Please try again later.")
        case 500:
            sys.exit("Internal server error. Make sure you have set a valid PUUID and region in the settings.")
        case 501:
            sys.exit("API Version not implemented. Please contact the developer.")
        case 503:
            sys.exit("Riot API seems to be down, API unable to connect. Please try again later.")
        case _:
            sys.exit("An error has occured.")

def find_puuid(name: str, tag: str) -> str:
    request = requests.get(c.ACCOUNT_BY_NAME_URL(name, tag)).json()
    return request["data"]["puuid"]

def get_matches(puuid: str, affinity: str, size: int=10) -> list:
    request = requests.get(c.MATCHES_URL(puuid, affinity), {"mode": "competitive", "size": size}, timeout=c.TIMEOUT).json()

    manage_henrikdev_api_errors(request["status"])

    return request["data"]

def get_new_matches(puuid: str, affinity: str, latest_match_id: str) -> list:
    index = 0

    for index, match in enumerate(matches := get_matches(puuid, affinity)):
        if match["metadata"]["matchid"] == latest_match_id:
            new_matches = matches[:index]
            new_matches.reverse()

            return new_matches

    matches.reverse()
    return matches

def get_mmr_changes(puuid: str, affinity: str, size: int) -> list:
    request = requests.get(c.MMR_HISTORY_URL(puuid, affinity), {"size": size}, timeout=c.TIMEOUT).json()

    manage_henrikdev_api_errors(request["status"])

    mmr_changes = [match["last_mmr_change"] for match in request["data"]]
    mmr_changes.reverse()

    return mmr_changes

def convert_valorant_date(unformatted_date: str) -> datetime:
    datetime_obj = datetime.strptime(unformatted_date, c.VALORANT_DATE_FORMAT)
    return datetime_obj - timedelta(minutes=57)

def format_match_info(match_info: dict, puuid: str, mmr_change: str) -> dict[str, str | int]:
    meta = match_info["metadata"]
    player = next(player for player in match_info["players"]["all_players"] if player["puuid"] == puuid)
    stats = player["stats"]
    team = match_info["teams"][player["team"].lower()]

    date_started_datetime = convert_valorant_date(meta["game_start_patched"])
    headshot_percentage = round((stats["headshots"] / (stats["headshots"] + stats["bodyshots"] + stats["legshots"])) * 100)
    average_damage_per_round = round(player["damage_made"] / meta["rounds_played"])

    formatted_match_info = {"match_id": meta["matchid"], 
                            "date_started": date_started_datetime.strftime(r"%d/%m/%Y"),
                            "rank": player["currenttier_patched"],
                            "mmr_change": mmr_change,
                            "rounds_won": team["rounds_won"], 
                            "rounds_lost": team["rounds_lost"], 
                            "tracker_link": f"https://tracker.gg/valorant/match/{meta["matchid"]}",
                            "map": meta["map"],
                            "agent": player["character"],
                            "kills": stats["kills"],
                            "deaths": stats["deaths"],
                            "assists": stats["assists"],
                            "headshot_percentage": headshot_percentage,
                            "average_damage_per_round": average_damage_per_round}

    if get_setting(*c.AUTOUPLOAD_VIDEOS_SETTING_LOCATOR, boolean=True):
        while (threading.active_count() - 1) >= get_setting(*c.MAX_VIDEOS_SIMULTANEOUSLY_SETTING_LOCATOR, integer=True):
            sleep(c.UPLOAD_POLL_FREQUENCY)

        try:
            formatted_match_info["video_link"] = upload_video(formatted_match_info, date_started_datetime)
        except FileNotFoundError as e:
            print(e)

    return formatted_match_info

def upload_video(match_info: dict[str, str | int], date_started_datetime: datetime) -> str:
    firefox_profile_path = get_setting(*c.FIREFOX_PROFILE_SETTING_LOCATOR)
    title = format_video_title(match_info)
    visibility = get_setting(*c.VIDEO_VISIBILITY_SETTING_LOCATOR)
    background = get_setting(*c.BACKGROUND_PROCESS_SETTING_LOCATOR, boolean=True)

    if get_setting(*c.AUTOSELECT_VIDEOS_SETTING_LOCATOR, boolean=True):
        try:
            video_path = autofind_video_path(date_started_datetime)
        except FileNotFoundError:
            video_path = input_file_path(f"Autofind error, open video for {title}")
    else:
        video_path = input_file_path(f"Open video for {title}")
    
    if video_path:
        while True:
            try:
                video_link = selenium_youtube.upload_video(firefox_profile_path,
                                                video_path,
                                                title,
                                                visibility=visibility,
                                                background=background)
            except (NoSuchWindowException, NoSuchElementException):
                reupload_msgbox = messagebox.askquestion("Reupload Video?", f"An error has occured, would you like to reupload the video for {title}?")

                if reupload_msgbox == "no":
                    break
            else:
                break
    else:
        raise FileNotFoundError(f"No video path found for '{title}', skipping upload...")
    
    return video_link

def input_file_path(title: str) -> str:
    file_path = filedialog.askopenfilename(title=title)

    return file_path

def compare_datetimes_lazily(a: datetime, b: datetime) -> bool:
    t_kwargs = {"second": 0, "microsecond": 0}

    return a.replace(**t_kwargs) == b.replace(**t_kwargs)

def autofind_video_path(match_datetime: datetime) -> str:
    recording_start_delay = get_setting(*c.RECORDING_START_DELAY_SETTING_LOCATOR, floatp=True)
    match_datetime += timedelta(seconds=recording_start_delay)

    directory = get_setting(*c.VIDEO_DIRECTORY_SETTING_LOCATOR)
    filename_format = get_setting(*c.FILENAME_FORMAT_SETTING_LOCATOR)

    for filename in reversed(listdir(directory)):
        try:
            video_datetime = datetime.strptime(filename, filename_format)
        except ValueError:
            continue

        if compare_datetimes_lazily(video_datetime, match_datetime) or compare_datetimes_lazily(video_datetime, (match_datetime - timedelta(minutes=1))):
            return f"{directory}/{filename}"

    raise FileNotFoundError

def format_video_title(formatted_match_info: dict) -> str:
    return f"VALORANT {formatted_match_info["date_started"]} {formatted_match_info["map"]} {formatted_match_info["agent"]} {formatted_match_info["rank"].replace(" ", "")}"

def get_setting(section: str, name: str, integer: bool=False, floatp: bool=False, boolean: bool=False) -> str | int | float | bool:
    config = RawConfigParser()
    config.read(c.SETTINGS_FILE_NAME)

    c_kwargs = {"section": section, "option": name, "fallback": None}
    
    if integer:
        return config.getint(**c_kwargs)
    elif floatp:
        return config.getfloat(**c_kwargs)
    elif boolean:
        return config.getboolean(**c_kwargs)
    else:
        return config.get(**c_kwargs)
    
def edit_setting(section: str, name: str, value: str | int | float | bool):
    config = RawConfigParser()
    config.read(c.SETTINGS_FILE_NAME)

    config.set(section, name, value)

    with open(c.SETTINGS_FILE_NAME, "w") as file:
        config.write(file)

def get_key_from_value(dictionary: dict, value):
    return list(dictionary.keys())[list(dictionary.values()).index(value)]
