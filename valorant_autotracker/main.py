import sys
import threading

from selenium_youtube.constants import UPLOAD_POLL_FREQUENCY
from utils.threads import wait_until_number_of_threads_is
from utils.settings import get_setting, edit_setting, delete_setting, InvalidSettingsError
import valorant_autotracker.constants as c
import valorant_autotracker.helpers as h

def main() -> None:
    print("Starting script...")

    edit_setting(*c.DEFAULT_NUMBER_OF_THREADS, threading.active_count()) # Creates temporary setting

    puuid = get_setting(*c.PUUID_SETTING_LOCATOR)

    try:
        affinity = c.Affinity[get_setting(*c.AFFINITY_SETTING_LOCATOR)]
    except KeyError as e:
        raise InvalidSettingsError("'region' setting is not valid. Please check and save your settings.") from e

    api = h.ValorantAPI(get_setting(*c.API_KEY_SETTING_LOCATOR))

    latest_match_id = get_setting(*c.LATEST_MATCH_ID_SETTING_LOCATOR)

    matches = api.get_new_matches(puuid, affinity, latest_match_id)

    if matches:
        write_to_google_sheets = get_setting(*c.WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR,
                                               boolean=True)
        write_to_excel_file = get_setting(*c.WRITE_TO_EXCEL_FILE_SETTING_LOCATOR,
                                            boolean=True)

        if write_to_google_sheets:
            google_sheets_sheet_name = get_setting(*c.GOOGLE_SHEETS_NAME_SETTING_LOCATOR)
            google_sheets_sheet = h.get_google_sheet(google_sheets_sheet_name).sheet1

            google_sheets_kwargs = {"value_input_option": "USER_ENTERED"}
        if write_to_excel_file:
            excel_file_path = get_setting(*c.EXCEL_FILE_PATH_SETTING_LOCATOR)
            excel_workbook = h.get_excel_workbook(excel_file_path)

            excel_kwargs = {"workbook": excel_workbook, "path": excel_file_path}

        insert_to_row_2 = get_setting(*c.INSERT_TO_ROW_2_LOCATOR, boolean=True)
        spreadsheet_format = get_setting(*c.SPREADSHEET_FORMAT_LOCATOR).split(",")

        mmr_changes = api.get_mmr_changes(puuid, affinity, len(matches))

        for match in matches:
            match_id = match["metadata"]["matchid"]
            match_info = h.format_match_info(match, puuid, mmr_changes.get(match_id))

            try:
                formatted_match = [match_info[column_heading]
                                   for column_heading in spreadsheet_format]
            except KeyError as e:
                raise InvalidSettingsError("'spreadsheet_format' setting is not valid. Please check and save your settings.") from e

            if write_to_google_sheets:
                if insert_to_row_2:
                    google_sheets_sheet.insert_row(formatted_match,
                                                   2,
                                                   **google_sheets_kwargs)
                else:
                    google_sheets_sheet.append_row(formatted_match,
                                                   insert_data_option="INSERT_ROWS",
                                                   table_range="A1",
                                                   **google_sheets_kwargs)
            if write_to_excel_file:
                if insert_to_row_2:
                    h.insert_row_to_excel_sheet(values=formatted_match, row=2, **excel_kwargs)
                else:
                    h.append_row_to_excel_sheet(values=formatted_match, **excel_kwargs)

            print(f"Added match '{h.format_video_title(match_info)}' to spreadsheet(s).")

            edit_setting(*c.LATEST_MATCH_ID_SETTING_LOCATOR, match_info["match_id"])

        # Waits for all uploads to finish
        default_number_of_threads = get_setting(*c.DEFAULT_NUMBER_OF_THREADS, integer=True)
        wait_until_number_of_threads_is(default_number_of_threads, UPLOAD_POLL_FREQUENCY)

        print("All tasks done.")
    else:
        print("No new matches.")

    delete_setting(*c.DEFAULT_NUMBER_OF_THREADS) # Deletes temporary setting

    print("Closing script...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Exiting script...")
    except Exception as exc:
        print(exc)
