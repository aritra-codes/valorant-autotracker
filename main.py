import constants as c
import helpers as h

def main() -> None:
    google_sheet_name = h.get_setting(*c.GOOGLE_SHEETS_NAME_SETTING_LOCATOR)
    sheet = h.get_google_sheet(google_sheet_name).sheet1

    puuid = h.get_setting(*c.PUUID_SETTING_LOCATOR)
    affinity = h.get_setting(*c.AFFINITY_SETTING_LOCATOR)

    matches = h.get_new_matches(puuid, affinity, h.get_latest_match_id(sheet))

    if matches:
        use_google_sheets = h.get_setting(*c.USE_GOOGLE_SHEETS_SETTING_LOCATOR, boolean=True)

        spreadsheet_format = h.get_setting(*c.SPREADSHEET_FORMAT_LOCATOR).split(",")

        mmr_changes = h.get_mmr_changes(puuid, affinity, len(matches))

        for index, match in enumerate(matches):
            match = h.format_match_info(match, puuid, mmr_changes[index])

            formatted_match = [match.get(row_heading, "") for row_heading in spreadsheet_format]

            if use_google_sheets:
                sheet.insert_row(formatted_match, 2, 'USER_ENTERED')

if __name__ == "__main__":
    main()
