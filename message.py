from customtkinter import (set_appearance_mode, set_default_color_theme, 
                           CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, 
                           CTkImage, filedialog, END, CTkSwitch, StringVar, 
                           CTkSlider, CTkComboBox, CTkOptionMenu, CTkScrollableFrame)
from PIL import Image
import os
from tkinter import Toplevel, Label, messagebox
#from main import main # Uncomment here for testing!
import helpers as h
import constants as c

set_appearance_mode("light")
set_default_color_theme("dark-blue")
default_font = ("Calibri", 14)

image_path = os.path.join(os.path.dirname
                                  (os.path.realpath(__file__)), "images")
run_image = CTkImage(light_image=Image.open(os.path.join(image_path, "run_dark.png")),
                                   dark_image=Image.open(os.path.join(image_path, "run.png"))) 

settings_image = CTkImage(light_image=Image.open(os.path.join(image_path, "settings_dark.png")),
                          dark_image=Image.open(os.path.join(image_path, "settings.png")))

question_image = CTkImage(light_image=Image.open(os.path.join(image_path, "question_mark_dark.png")),
                          dark_image=Image.open(os.path.join(image_path, "question_mark.png")))

change_dir = CTkImage(light_image=Image.open(os.path.join(image_path, "folder.png")),
                      dark_image=Image.open(os.path.join(image_path, "folder.png")))
        
find_image = CTkImage(light_image=Image.open(os.path.join(image_path, "find_dark.png")),
                      dark_image=Image.open(os.path.join(image_path, "find.png")))

save_image = CTkImage(light_image=Image.open(os.path.join(image_path, "save_file.png")),
                      dark_image=Image.open(os.path.join(image_path, "save_file.png")))

donate_image = CTkImage(light_image=Image.open(os.path.join(image_path, "paypal.png")),
                      dark_image=Image.open(os.path.join(image_path, "paypal.png")))

# CHANGE TO TOPLEVEL IN MAIN UI.PY!!
class SpreadsheetFormat(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("550x680")
        self.title("Settings")
        self.iconbitmap("logo.ico")
                
        self.frame = CTkScrollableFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.dropdown_menus_list = []
        self.format_settings_list = []

        self.row_count = -1
        self.spreadsheet_format_label = CTkLabel(self.frame, text="Spreadsheet Format\n(Columns)",
                                                    font=default_font)
        self.spreadsheet_format_label.grid(row=0, column=0, padx=10, pady=(10,0),
                                            sticky="w")

        self.spreadsheet_format_list = ["Match ID","Date Started","Rank","MMR Change",
                                        "Rounds Won","Rounds Lost","Tracker Link",
                                        "Video Link","Map","Agent","Kills","Deaths",
                                        "Assists","Headshot %","ADR"]
        self.plus_button = CTkButton(self.frame, text="+", font=default_font,
                                        command=self.add_boxes, width=20, corner_radius=20)
        self.plus_button.grid(row=0, column=2, padx=10, pady=(10,0), sticky="e")

        self.minus_button = CTkButton(self.frame, text="-", font=default_font,
                                        command=self.subtract_boxes, width=20, corner_radius=20)
        self.minus_button.grid(row=0, column=3, padx=0, pady=(10,0), sticky="w")

        #------------------------------------------------------

        self.count = 0
        spreadsheet_format = h.get_setting(*c.SPREADSHEET_FORMAT_LOCATOR)

        if spreadsheet_format:
            items = spreadsheet_format.split(",")
            for index, item in enumerate(items):
                current_setting = c.SPREADSHEET_FORMAT_OPTIONS[item]
                
                self.add_boxes(current_setting, True if index == 0 else False)


    def add_boxes(self, value="-", disabled: bool=False):
        self.count += 1
        self.final_count = self.row_count + self.count
        
        index = self.count - 1

        if disabled:
            dropdown_menu = CTkOptionMenu(self.frame, 
                                    values=self.spreadsheet_format_list,
                                    font=default_font, button_color="grey",
                                    button_hover_color="dark grey",
                                    fg_color="white", text_color="black")
            dropdown_menu.configure(state="disabled")
        else:
            dropdown_menu = CTkOptionMenu(self.frame, 
                                    values=self.spreadsheet_format_list,
                                    command=lambda value: self.spreadsheet_format_function(index, value),
                                    font=default_font, button_color="grey",
                                    button_hover_color="dark grey",
                                    fg_color="white", text_color="black")
            dropdown_menu.configure(state="normal")
        
        dropdown_menu.set(value)
        dropdown_menu.grid(row=self.final_count, column=1, pady=(10,0),
                                sticky="ew")
        self.dropdown_menus_list.append(dropdown_menu)
        self.spreadsheet_format_function(self.count - 1, value)

    def subtract_boxes(self):
        #print(len(self.dropdown_menus_list))
        self.minus_button.configure(state="normal")
        if self.count > 1:
            self.count -= 1
            self.final_count = self.row_count + self.count
            last_dropdown_menu = self.dropdown_menus_list.pop()
            last_dropdown_menu.grid_forget()
            last_dropdown_menu.destroy()

            self.format_settings_list.pop()

    def spreadsheet_format_function(self, index, setting):
        # Looks in the SPREADSHEET_FORMAT_OPTIONS dict for the value and returns the corresponding key (e.g. "Match ID" returns "match_id")
        options_dict = c.SPREADSHEET_FORMAT_OPTIONS
        formatted_setting = list(options_dict.keys())[list(options_dict.values()).index(setting)]

        try:
            self.format_settings_list[index] = formatted_setting
        except IndexError:
            self.format_settings_list.append(formatted_setting)

        # Comment below after testing
        print(self.format_settings_list)

if __name__ == "__main__":
    app = SpreadsheetFormat()
    app.mainloop()