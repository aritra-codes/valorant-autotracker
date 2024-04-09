import constants as c
import helpers as h
from selenium_youtube import upload_video
from datetime import datetime, timedelta

def main():
    sheet = h.get_sheet(c.SHEET_NAME).sheet1

    matches = h.get_new_matches(c.PUUID, c.AFFINITY, h.get_latest_match_id(sheet))

    if matches:
        mmr_changes = h.get_mmr_changes(c.PUUID, c.AFFINITY, len(matches))

        for index, match in enumerate(matches):
            match = h.format_match_info(match)
    
            video_location = h.find_video_path(match["date_started_obj"])

            formatted_match = [match["match_id"],
                                match["date_started"],
                                match["rank"],
                                mmr_changes[index],
                                match["rounds_won"],
                                match["rounds_lost"],
                                match["tracker_link"],
                                upload_video(video_location, h.format_video_title(match), visibility=c.Visibility.UNLISTED),
                                match["map"],
                                match["agent"],
                                match["kills"],
                                match["deaths"],
                                match["assists"],
                                match["headshot_percentage"],
                                match["average_damage_per_round"]]

            sheet.insert_row(formatted_match, 2, 'USER_ENTERED')

if __name__ == "__main__":
    main()
