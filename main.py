import sys
import threading

import constants as c
import helpers as h

def main() -> None:
    print("Starting script...")

    h.edit_setting(*c.DEFAULT_NUMBER_OF_THREADS, threading.active_count())

    puuid = h.get_setting(*c.PUUID_SETTING_LOCATOR)

    try:
        affinity = c.Affinity[h.get_setting(*c.AFFINITY_SETTING_LOCATOR)]
    except KeyError as e:
        raise c.InvalidSettingsError("'region' setting is not valid. Please check and save your settings.") from e

    latest_match_id = h.get_setting(*c.LATEST_MATCH_ID_SETTING_LOCATOR)
    matches = h.get_new_matches(puuid, affinity, latest_match_id)

    if matches:
        write_to_google_sheets = h.get_setting(*c.WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR,
                                               boolean=True)
        write_to_excel_file = h.get_setting(*c.WRITE_TO_EXCEL_FILE_SETTING_LOCATOR,
                                            boolean=True)

        if write_to_google_sheets:
            google_sheets_sheet_name = h.get_setting(*c.GOOGLE_SHEETS_NAME_SETTING_LOCATOR)
            google_sheets_sheet = h.get_google_sheet(google_sheets_sheet_name).sheet1

            google_sheets_kwargs = {"value_input_option": 'USER_ENTERED'}
        if write_to_excel_file:
            excel_file_path = h.get_setting(*c.EXCEL_FILE_PATH_SETTING_LOCATOR)
            excel_workbook = h.get_excel_workbook(excel_file_path)

            excel_kwargs = {"workbook": excel_workbook, "path": excel_file_path}

        insert_to_row_2 = h.get_setting(*c.INSERT_TO_ROW_2_LOCATOR, boolean=True)
        spreadsheet_format = h.get_setting(*c.SPREADSHEET_FORMAT_LOCATOR).split(",")

        mmr_changes = h.get_mmr_changes(puuid, affinity, len(matches))

        for index, match in enumerate(matches):
            match_info = h.format_match_info(match, puuid, mmr_changes[index])

            try:
                formatted_match = [match_info[column_heading]
                                   for column_heading in spreadsheet_format]
            except KeyError as e:
                raise c.InvalidSettingsError("'spreadsheet_format' setting is not valid. Please check and save your settings.") from e

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

            h.edit_setting(*c.LATEST_MATCH_ID_SETTING_LOCATOR, match_info["match_id"])

        # Waits for all uploads to finish
        default_number_of_threads = h.get_setting(*c.DEFAULT_NUMBER_OF_THREADS, integer=True)
        h.wait_until_number_of_threads_is(default_number_of_threads, c.UPLOAD_POLL_FREQUENCY)

        print("All tasks done.")
    else:
        print("No new matches.")

    print("Closing script...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("Exiting script...")
    except Exception as exc:
        print(exc)
