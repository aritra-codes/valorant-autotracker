import constants as c
import helpers as h
from selenium_youtube import upload_video

def main() -> None:
    google_sheet_name = h.get_setting(*c.GOOGLE_SHEETS_NAME_SETTING_LOCATOR)
    sheet = h.get_sheet(google_sheet_name).sheet1

    puuid = h.get_setting(*c.PUUID_SETTING_LOCATOR)
    affinity = h.get_setting(*c.AFFINITY_SETTING_LOCATOR)

    matches = h.get_new_matches(puuid, affinity, h.get_latest_match_id(sheet))
    matches.reverse()

    if matches:
        mmr_changes = h.get_mmr_changes(puuid, affinity, len(matches))
        mmr_changes.reverse()

        for index, match in enumerate(matches):
            match = h.format_match_info(match, puuid)
    
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
