from gspread.worksheet import Worksheet as GoogleWorksheet
from openpyxl import Workbook as ExcelWorkbook

import constants as c
import helpers as h

def main() -> None:
    def get_google_sheets_sheet() -> GoogleWorksheet:
        sheet_name = h.get_setting(*c.GOOGLE_SHEETS_NAME_SETTING_LOCATOR)
        sheet = h.get_google_sheet(sheet_name).sheet1

        return sheet

    def get_excel_workbook() -> tuple[ExcelWorkbook, str]:
        file_path = h.get_setting(*c.EXCEL_FILE_PATH_SETTING_LOCATOR)
        workbook = h.get_excel_workbook(file_path)

        return workbook, file_path

    sheet_to_read = h.get_setting(*c.SPREADSHEET_TO_READ_SETTING_LOCATOR)
    match sheet_to_read:
        case "google_sheets":
            sheet = get_google_sheets_sheet()
        case "excel_file":
            sheet = get_excel_workbook()[0].active

    puuid = h.get_setting(*c.PUUID_SETTING_LOCATOR)
    affinity = h.get_setting(*c.AFFINITY_SETTING_LOCATOR)

    matches = h.get_new_matches(puuid, affinity, h.get_latest_match_id(sheet))

    if matches:
        write_to_google_sheets = h.get_setting(*c.WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR, boolean=True)
        write_to_excel_file = h.get_setting(*c.WRITE_TO_EXCEL_FILE_SETTING_LOCATOR, boolean=True)

        if write_to_google_sheets:
            google_sheets_sheet = get_google_sheets_sheet()
        if write_to_excel_file:
            excel_workbook, excel_file_path = get_excel_workbook()

        insert_to_row_2 = h.get_setting(*c.INSERT_TO_ROW_2_LOCATOR, boolean=True)

        spreadsheet_format = h.get_setting(*c.SPREADSHEET_FORMAT_LOCATOR).split(",")

        mmr_changes = h.get_mmr_changes(puuid, affinity, len(matches))

        for index, match in enumerate(matches):
            match = h.format_match_info(match, puuid, mmr_changes[index])

            formatted_match = [match.get(row_heading, "") for row_heading in spreadsheet_format]

            if write_to_google_sheets:
                h_kwargs = {"values": formatted_match, "value_input_option": 'USER_ENTERED'}

                if insert_to_row_2:
                    google_sheets_sheet.insert_row(**h_kwargs, index=2)
                else:
                    google_sheets_sheet.append_row(**h_kwargs, table_range="A1")
            if write_to_excel_file:
                h_kwargs = {"workbook": excel_workbook, "path": excel_file_path, "values": formatted_match}

                if insert_to_row_2:
                    h.insert_values_to_excel_sheet(**h_kwargs, row=2)
                else:
                    h.append_values_to_excel_sheet(**h_kwargs)

if __name__ == "__main__":
    main()
