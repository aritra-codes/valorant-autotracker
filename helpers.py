from os import listdir
from datetime import datetime, timedelta

import gspread
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
import requests
from configparser import RawConfigParser

import constants as c

def get_sheet(name: str) -> Spreadsheet:
    creds = ServiceAccountCredentials.from_json_keyfile_name(get_setting(*c.GOOGLE_SERVICE_ACCOUNT_KEY_JSON_PATH), c.SCOPE)
    client = gspread.authorize(creds)

    return client.open(name)

def get_latest_match_id(sheet: Worksheet) -> str:
    return sheet.cell(2, 1).value

def find_puuid(name: str, tag: str) -> str:
    request = requests.get(c.ACCOUNT_URL(name, tag), timeout=c.TIMEOUT).json()
    return request["data"]["puuid"]

def get_matches(puuid: str, affinity: str, size: int=10) -> dict:
    request = requests.get(c.MATCHES_URL(puuid, affinity), {"mode": "competitive", "size": size}, timeout=c.TIMEOUT).json()
    return request["data"]

def get_new_matches(puuid: str, affinity: str, latest_match_id: str) -> list | None:
    index = 0

    for index, match in enumerate(matches := get_matches(puuid, affinity)):
        if match["metadata"]["matchid"] == latest_match_id:
            return matches[:index]

    return None

def get_mmr_changes(puuid: str, affinity: str, size: int) -> list:
    request = requests.get(c.MMR_HISTORY_URL(puuid, affinity), {"size": size}, timeout=c.TIMEOUT).json()
    return [match["last_mmr_change"] for match in request["data"]]

def convert_valorant_date(unformatted_date: str) -> datetime:
    datetime_obj = datetime.strptime(unformatted_date, r"%A, %B %d, %Y %I:%M %p")
    return datetime_obj - timedelta(minutes=57)

def format_match_info(match_info: dict, puuid: str) -> dict:
    meta = match_info["metadata"]
    player = next(player for player in match_info["players"]["all_players"] if player["puuid"] == puuid)
    stats = player["stats"]
    team = match_info["teams"][player["team"].lower()]

    date_started_obj = convert_valorant_date(meta["game_start_patched"])
    headshot_percentage = round((stats["headshots"] / (stats["headshots"] + stats["bodyshots"] + stats["legshots"])) * 100)
    average_damage_per_round = round(player["damage_made"] / meta["rounds_played"])

    return {"match_id": meta["matchid"], 
            "date_started_obj":  date_started_obj,
            "date_started": date_started_obj.strftime(r"%d/%m/%Y"),
            "rank": player["currenttier_patched"], 
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

"""def compare_datetime_without_seconds(a: datetime, b: datetime) -> bool:
    a.replace(second=0)
    b.replace(second=0)

    return a == b"""

def find_video_path(match_datetime: datetime) -> str:
    directory = get_setting(*c.VIDEO_DIRECTORY_SETTING_LOCATOR)
    filename_format = get_setting(*c.FILENAME_FORMAT_SETTING_LOCATOR)

    for filename in reversed(listdir(directory)):

        if filename.startswith(match_datetime.strftime(filename_format)) or filename.startswith((match_datetime - timedelta(minutes=1)).strftime(filename_format)):
            return f"{directory}/{filename}"

    raise FileNotFoundError

def format_video_title(formatted_match_info: dict) -> str:
    return f"VALORANT {formatted_match_info["date_started_obj"].strftime(r"%Y-%m-%d")} {formatted_match_info["map"]} {formatted_match_info["agent"]} {formatted_match_info["rank"].replace(" ", "")}"

def get_setting(profile: str, name: str):
    config = RawConfigParser()
    config.read(c.SETTINGS_FILE_NAME)

    return config.get(profile, name)