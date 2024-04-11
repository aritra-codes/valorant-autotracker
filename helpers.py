from os import listdir
from datetime import datetime, timedelta

import gspread
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet as GoogleWorksheet
from oauth2client.service_account import ServiceAccountCredentials
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet as ExcelWorksheet
import requests
from configparser import RawConfigParser

import constants as c
import selenium_youtube

def get_excel_workbook(path: str) -> Workbook:
    workbook = load_workbook(path)

    return workbook

def insert_values_to_excel_sheet(workbook: Workbook, path: str, row: int, values: list[str]) -> None:
    sheet: ExcelWorksheet = workbook.active
    sheet.insert_rows(row)

    for index, value in enumerate(values):
        cell = sheet.cell(row, index + 1)
        cell.value = value

    workbook.save(path)

def append_values_to_excel_sheet(workbook: Workbook, path: str, values: list[str]) -> None:
    sheet: ExcelWorksheet = workbook.active
    sheet.append(values)

    workbook.save(path)

def get_google_sheet(name: str) -> Spreadsheet:
    creds = ServiceAccountCredentials.from_json_keyfile_name(get_setting(*c.GOOGLE_SERVICE_ACCOUNT_KEY_JSON_PATH_LOCATOR), c.SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(name)

    return sheet

def get_latest_match_id(sheet: ExcelWorksheet | GoogleWorksheet) -> str:
    return sheet.cell(2, 1).value

def find_puuid(name: str, tag: str) -> str:
    request = requests.get(c.ACCOUNT_URL(name, tag), timeout=c.TIMEOUT).json()
    return request["data"]["puuid"]

def get_matches(puuid: str, affinity: str, size: int=10) -> list:
    request = requests.get(c.MATCHES_URL(puuid, affinity), {"mode": "competitive", "size": size}, timeout=c.TIMEOUT).json()
    return request["data"]

def get_new_matches(puuid: str, affinity: str, latest_match_id: str) -> list | None:
    index = 0

    for index, match in enumerate(matches := get_matches(puuid, affinity)):
        if match["metadata"]["matchid"] == latest_match_id:
            new_matches = matches[:index]
            new_matches.reverse()

            return new_matches

    return None

def get_mmr_changes(puuid: str, affinity: str, size: int) -> list:
    request = requests.get(c.MMR_HISTORY_URL(puuid, affinity), {"size": size}, timeout=c.TIMEOUT).json()
    mmr_changes = [match["last_mmr_change"] for match in request["data"]]
    mmr_changes.reverse()

    return mmr_changes

def convert_valorant_date(unformatted_date: str) -> datetime:
    datetime_obj = datetime.strptime(unformatted_date, c.VALORANT_DATE_FORMAT)
    return datetime_obj - timedelta(minutes=57)

def format_match_info(match_info: dict, puuid: str, mmr_change: str) -> dict[str, str]:
    meta = match_info["metadata"]
    player = next(player for player in match_info["players"]["all_players"] if player["puuid"] == puuid)
    stats = player["stats"]
    team = match_info["teams"][player["team"].lower()]

    date_started_obj = convert_valorant_date(meta["game_start_patched"])
    headshot_percentage = round((stats["headshots"] / (stats["headshots"] + stats["bodyshots"] + stats["legshots"])) * 100)
    average_damage_per_round = round(player["damage_made"] / meta["rounds_played"])

    formatted_match_info = {"match_id": meta["matchid"], 
                            "date_started": date_started_obj.strftime(r"%d/%m/%Y"),
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
        video_location = find_video_path(date_started_obj)
        firefox_profile_path = get_setting(*c.FIREFOX_PROFILE_SETTING_LOCATOR)
        visibility = get_setting(*c.VIDEO_VISIBILITY_SETTING_LOCATOR)
        
        video_link = selenium_youtube.upload_video(firefox_profile_path,
                                                   video_location,
                                                   format_video_title(formatted_match_info),
                                                   visibility=visibility)
        formatted_match_info["video_link"] = video_link

    return formatted_match_info

"""def compare_datetime_without_seconds(a: datetime, b: datetime) -> bool:
    a.replace(second=0)
    b.replace(second=0)

    return a == b"""

def find_video_path(match_datetime: datetime) -> str:
    recording_start_delay = get_setting(*c.RECORDING_START_DELAY_SETTING_LOCATOR, floatp=True)
    match_datetime += timedelta(seconds=recording_start_delay)

    directory = get_setting(*c.VIDEO_DIRECTORY_SETTING_LOCATOR)
    filename_format = get_setting(*c.FILENAME_FORMAT_SETTING_LOCATOR)

    for filename in reversed(listdir(directory)):

        if filename.startswith(match_datetime.strftime(filename_format)) or filename.startswith((match_datetime - timedelta(minutes=1)).strftime(filename_format)):
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
