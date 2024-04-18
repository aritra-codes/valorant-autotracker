from customtkinter import (set_appearance_mode, set_default_color_theme, 
                           CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, 
                           CTkImage, filedialog, END, CTkSwitch, StringVar, 
                           CTkSlider, CTkOptionMenu, CTkScrollableFrame)
from PIL import Image
import os
from tkinter import Toplevel, Label, messagebox, scrolledtext
import sys
import threading

# Import local packages
from main import main
import helpers as h
import constants as c

set_appearance_mode("light") # Set theme to light
set_default_color_theme("dark-blue") # Set colour theme to dark blue (for buttons etc.)
default_font = ("Calibri", 14) # Default font to be used throughout program

image_path = os.path.join(os.path.dirname
                                  (os.path.realpath(__file__)), "images") # Define the image path for all images used
question_image = CTkImage(light_image=Image.open(os.path.join(image_path, "question_mark_dark.png")),
                          dark_image=Image.open(os.path.join(image_path, "question_mark.png"))) # Question image for Hoverbuttons

change_dir = CTkImage(light_image=Image.open(os.path.join(image_path, "folder.png")),
                      dark_image=Image.open(os.path.join(image_path, "folder.png"))) # Change directory/file image (folder)
        
find_image = CTkImage(light_image=Image.open(os.path.join(image_path, "find_dark.png")),
                      dark_image=Image.open(os.path.join(image_path, "find.png"))) # Find image (find PUUID)

save_image = CTkImage(light_image=Image.open(os.path.join(image_path, "save_file.png")),
                      dark_image=Image.open(os.path.join(image_path, "save_file.png"))) # Save image

reset_image = CTkImage(light_image=Image.open(os.path.join(image_path, "reset.png")),
                      dark_image=Image.open(os.path.join(image_path, "reset.png"))) # Reset (settings) image

class PrintLogger():  # Create file like object
    def __init__(self, textbox):  # Pass reference to text widget
        sys.stdout = self
        sys.stderr = self
        self.textbox = textbox  # Keep ref   

    def write(self, text):
        self.textbox.configure(state="normal")  # Make field editable
        self.textbox.insert(END, f"{text}\n")  # Write text to textbox
        self.textbox.see(END)  # Scroll to end
        self.textbox.configure(state="disabled")  # Make field readonly

    def flush(self):  # Needed for file like object
        pass

class App(CTk): # Main application class
    def __init__(self):
        super().__init__()
        self.image_path = os.path.join(os.path.dirname
                                  (os.path.realpath(__file__)), "images") # Image path
        self.run_image = CTkImage(light_image=Image.open(os.path.join(self.image_path, "run_dark.png")),
                                        dark_image=Image.open(os.path.join(self.image_path, "run.png"))) # Run image 

        self.settings_image = CTkImage(light_image=Image.open(os.path.join(self.image_path, "settings_dark.png")),
                                dark_image=Image.open(os.path.join(self.image_path, "settings.png"))) # Settings image

        self.paypal_image = CTkImage(light_image=Image.open(os.path.join(image_path, "paypal.png")),
                      dark_image=Image.open(os.path.join(image_path, "paypal.png"))) # Donation button image

        self.geometry("1000x700") # Set the window size (can be resizable)
        self.iconbitmap("logo.ico") # Set logo (Valorant)
        self.title("Valorant Match Tracker") # Set title
        
        # Create a frame
        self.frame = CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)

        # Create a button to run the main script
        self.run = CTkButton(self.frame, text="Run", width=200, 
                             height=40, image=self.run_image,
                             font=default_font, command=self.thread_main)
        self.run.pack(pady=(20,0))

        # Create a button to open settings window (class)
        self.settings_button = CTkButton(self.frame, text="Settings", width=200, 
                                         height=40, image=self.settings_image,
                                         font=default_font, command=self.open_settings)
        self.settings_button.pack(pady=(10,0))

        # Create a donation button
        self.paypal_donate = CTkButton(self.frame, text="Why not consider donating?", width=200, 
                                         height=40, image=self.paypal_image,
                                         font=default_font, command=self.donate_function)
        self.paypal_donate.pack(pady=(10,0))

        # Entry box displays console output
        self.output_label = CTkLabel(self.frame, text="Output:", font=default_font)
        self.output_label.pack(pady=(10,0))

        self.output_entry = scrolledtext.ScrolledText(self.frame, bd=1,
                                                      font=("Cascadia Code", 9),
                                                      height=8)
        self.output_entry.pack(expand=True, fill="both", pady=(10,20), padx=20)
        self.output_entry.configure(state="disabled")

        PrintLogger(self.output_entry) # Ref to entry box for console output

    def thread_main(self):
        def run_main():
            try:
                main()
            except Exception as e:
                print(e)

        thread = threading.Thread(target=run_main)
        thread.start()

    # Opens the settings window
    def open_settings(self):
        settings_window = SettingsWindow()
        settings_window.mainloop()

    def donate_function(self):
        pass # ADD FUNCTION HERE

class HoverButton(CTkButton): # Creates a class for hover button (question mark)
    def __init__(self, master, text, tooltip_text, image, width, fg_color,
                 hover_color, **kw):
        CTkButton.__init__(self, master, text=text, image=image, width=width, 
                           fg_color=fg_color, hover_color=hover_color, **kw)
        self.tooltip = None
        self.tooltip_text = tooltip_text
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event=None):
        self.tooltip = Toplevel(self)
        x, y, _, _ = self.bbox("insert")
        x += self.winfo_rootx() + 25
        y += self.winfo_rooty() + 25
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = Label(self.tooltip, text=self.tooltip_text, bg="white", relief="solid", borderwidth=0.5)
        label.pack()

    # Destroys hoverbutton
    def on_leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class SettingsWindow(Toplevel): # Settings window (Toplevel)
    def __init__(self):
        super().__init__()
        # Window attributes
        self.geometry("820x660")
        self.title("Settings")
        self.iconbitmap("logo.ico")

        # Create a frame for settings     
        self.frame = CTkScrollableFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Create and place all the objects of settings window
        self.save_button = CTkButton(self.frame, text="Save", font=default_font,
                                     width=100, image=save_image, command=self.save_settings)
        self.save_button.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")

        self.reset = CTkButton(self.frame, text="Reset to Default",
                                         font=default_font, image=reset_image,
                                         command=self.reset_function, width=160)
        self.reset.grid(row=0, column=1, pady=(10,0), sticky="w")

        self.video_header = CTkLabel(self.frame, text="Video", 
                                     font=("Calibri Bold",18))
        self.video_header.grid(row=1, column=0, padx=10, pady=(10,0), sticky="w")

        self.switch_var = StringVar(value="off")
        self.switch_label = CTkLabel(self.frame, text="Auto-Upload Videos",
                                     font=default_font)
        self.switch_label.grid(row=2, column=0, pady=(10,0), padx=10, sticky="w")
        self.switch_onoff = CTkSwitch(self.frame, text="", command=self.switch1,
                                      variable=self.switch_var, onvalue="on",
                                      offvalue="off")
        self.switch_onoff.grid(row=2, column=1, pady=(10,0), sticky="w")

        self.firefox_profile_label = CTkLabel(self.frame, text="Firefox Profile Path",
                                              font=default_font)
        self.firefox_profile_label.grid(row=3, column=0, pady=(10,0), padx=10, sticky="w")
        self.firefox_entry = CTkEntry(self.frame, font=default_font, width=500,
                                     placeholder_text="Firefox profile path (C:/...)")
        self.firefox_entry.grid(row=3, column=1, pady=(10,0), columnspan=4)
        self.firefox_change = CTkButton(self.frame, text="Change  ", font=default_font,
                                       width=70, command=self.firefoxprofile_change_function,
                                       image=change_dir)
        self.firefox_change.grid(row=3, column=5, pady=(10,0), padx=5)

        self.background_process_label = CTkLabel(self.frame, text="Background Process",
                                                 font=default_font)
        self.background_process_label.grid(row=4, column=0, padx=10, pady=(10,0),
                                           sticky="w")
        self.background_process_var = StringVar(value="off")
        self.background_process_switch = CTkSwitch(self.frame, text="", 
                                                   variable=self.background_process_var,
                                                   onvalue="on", offvalue="off")
        self.background_process_switch.grid(row=4, column=1, pady=(10,0), sticky="w")
        self.background_process_hoverbutton = HoverButton(self.frame, text="", image=question_image,
                                                 tooltip_text="When turned on, Firefox will open in the background when\nuploading videos and not appear on your screen.",
                                                 width=15, fg_color="transparent",
                                                 hover_color="grey")
        self.background_process_hoverbutton.grid(row=4, column=1, padx=40, pady=(10,0), sticky="w")
        self.background_process_hoverbutton.configure(state="disabled")

        self.maxvids_sim_label = CTkLabel(self.frame, text="Max. Vids Simultaneously",
                                          font=default_font)
        self.maxvids_sim_label.grid(row=5, column=0, padx=10, pady=(10,0),
                                    sticky="w")
        self.maxvids_sim_entry = CTkEntry(self.frame, font=default_font,
                                          width=40, justify="center",
                                          placeholder_text="Enter int.")
        self.maxvids_sim_entry.grid(row=5, column=1, pady=(10,0), sticky="w")

        self.maxvids_hoverbutton = HoverButton(self.frame, text="", image=question_image,
                                                 tooltip_text="The number of videos that can be uploaded at the same time.",
                                                 width=15, fg_color="transparent",
                                                 hover_color="grey")
        self.maxvids_hoverbutton.grid(row=5, column=1, padx=40, pady=(10,0), sticky="w")
        self.maxvids_hoverbutton.configure(state="disabled")

        self.visibility_label = CTkLabel(self.frame, text="Visibility",
                                         font=default_font)
        self.visibility_label.grid(row=6, column=0, padx=10, pady=(10,0),
                                   sticky="w")
        self.visibility_list = list(c.VIDEO_VISIBILITY_OPTIONS.values())

        self.visibility_dropdown = CTkOptionMenu(self.frame, values=self.visibility_list,
                                               font=default_font, button_color="grey",
                                               button_hover_color="dark grey",
                                               fg_color="white", text_color="black")
        self.visibility_dropdown.grid(row=6, column=1, padx=2, pady=(10,0), sticky="w")

        self.switch_var2 = StringVar(value="off")
        self.switch_label_2 = CTkLabel(self.frame, text="Auto-Select Videos",
                                       font=default_font)
        self.switch_label_2.grid(row=7, column=0, pady=(10,0), padx=10, sticky="w")
        self.switch_onoff2 = CTkSwitch(self.frame, text="", command=self.switch2,
                                       variable=self.switch_var2, onvalue="on",
                                       offvalue="off")
        self.switch_onoff2.grid(row=7, column=1, pady=(10,0), sticky="w")

        self.viddir_label = CTkLabel(self.frame, text="Video Directory",
                                     font=default_font)
        self.viddir_label.grid(row=8, column=0, padx=10, pady=(10,0), sticky="w")
        self.viddir_entry = CTkEntry(self.frame, font=default_font, width=500,
                                     placeholder_text="Video directory (C:/...)")
        self.viddir_entry.grid(row=8, column=1, pady=(10,0), columnspan=4)
        self.viddir_change = CTkButton(self.frame, text="Change  ", font=default_font,
                                       width=70, command=self.viddir_change_function,
                                       image=change_dir)
        self.viddir_change.grid(row=8, column=5, pady=(10,0), padx=5)

        self.recording_client_label = CTkLabel(self.frame, text="Recording Client",
                                               font=default_font)
        self.recording_client_label.grid(row=9, column=0, padx=10, pady=(10,0),
                                         sticky="w")

        self.filename_format_list = list(c.RECORDING_CLIENT_OPTIONS.values())
        self.filename_format_optionmenu = CTkOptionMenu(self.frame, font=default_font,
                                                        values=self.filename_format_list,
                                                        button_color="grey",
                                                        button_hover_color="dark grey",
                                                        fg_color="white", text_color="black",
                                                        command=self.filename_format_options)
        self.filename_format_optionmenu.grid(row=9, column=1, pady=(10,0), sticky="w")

        self.filename_format_label = CTkLabel(self.frame, text="Filename Format",
                                              font=default_font)
        self.filename_format_label.grid(row=10, column=0, padx=10, pady=(10,0), sticky="w")
        self.filename_format_entry = CTkEntry(self.frame, font=default_font, 
                                              placeholder_text="Enter filename format",
                                              width=200)
        self.filename_format_entry.grid(row=10, column=1, pady=(10,0), sticky="ew",
                                        columnspan=3)
        self.filename_hover_button = HoverButton(self.frame, text="", image=question_image,
                                        tooltip_text="The format in which the recorded video files are named by the\nrecording client (written in Python datetime format codes).",
                                        width=15, fg_color="transparent",
                                        hover_color="grey")
        self.filename_hover_button.grid(row=10, column=4, pady=(10,0), sticky="w")

        self.recording_delay_label = CTkLabel(self.frame, text="Recording Delay",
                                              font=default_font)
        self.recording_delay_label.grid(row=11, column=0, padx=10, pady=(10,0),
                                        sticky="w")
        self.recording_delay_slider = CTkSlider(self.frame, from_=0, to=60,
                                                number_of_steps=60,
                                                command=self.slider)
        self.recording_delay_slider.grid(row=11, column=1, pady=(10,0), sticky="ew")
        self.recording_delay_slider.set(0)
        self.slider_value = CTkEntry(self.frame, font=default_font,
                                     width=40, justify="center")
        self.slider_value.insert(END, "0")
        self.slider_value.grid(row=11, column=2, pady=(10,0), padx=(10,10), sticky="ew")
        self.secs_label = CTkLabel(self.frame, text="secs",
                                   font=default_font)
        self.secs_label.grid(row=11, column=4, pady=(10,0), sticky="w")

        self.slider_hoverbutton = HoverButton(self.frame, text="", image=question_image,
                                                 tooltip_text="How long it takes for the recording to start after the start of the match.",
                                                 width=15, fg_color="transparent",
                                                 hover_color="grey")
        self.slider_hoverbutton.grid(row=11, column=4, padx=25, pady=(10,0), sticky="w")
        self.slider_hoverbutton.configure(state="disabled")

        self.valorant_header = CTkLabel(self.frame, text="Valorant", 
                                     font=("Calibri Bold",18))
        self.valorant_header.grid(row=12, column=0, padx=10, pady=(15,0), sticky="w")

        self.username_label = CTkLabel(self.frame, text="Username",
                                       font=default_font)
        self.username_label.grid(row=13, column=0, padx=10, pady=(10,0), sticky="w")
        self.username_entry = CTkEntry(self.frame, font=default_font,
                                       placeholder_text="Enter username (for PUUID)")
        self.username_entry.grid(row=13, column=1, pady=(10,0), sticky="ew")

        self.tag_label = CTkLabel(self.frame, text="Tag", font=default_font)
        self.tag_label.grid(row=14, column=0, padx=10, pady=(10,0), sticky="w")
        self.tag_entry = CTkEntry(self.frame, font=default_font,
                                  placeholder_text="Enter tag (for PUUID)")
        self.tag_entry.grid(row=14, column=1, pady=(10,0), sticky="ew")

        self.puuid_label = CTkLabel(self.frame, text="PUUID", font=default_font)
        self.puuid_label.grid(row=15, column=0, padx=10, pady=(10,0), sticky="w")
        self.puuid_entry = CTkEntry(self.frame, font=default_font,
                                    placeholder_text="Enter/Find PUUID")
        self.puuid_entry.grid(row=15, column=1, pady=(10,0), sticky="ew",
                              columnspan=3)
        self.puuid_find = CTkButton(self.frame, text="Find PUUID", 
                                    font=default_font, image=find_image,
                                    command=self.find_puuid_function, width=110)
        self.puuid_find.grid(row=15, column=4, pady=(10,0), padx=5, sticky="w")

        self.region_label = CTkLabel(self.frame, text="Region", font=default_font)
        self.region_label.grid(row=16, column=0, padx=10, pady=(10,0), sticky="w")
        self.region_list = list(c.REGION_OPTIONS.values())
        self.region_dropdown = CTkOptionMenu(self.frame, values=self.region_list, 
                                               font=default_font, button_color="grey",
                                               button_hover_color="dark grey",
                                               fg_color="white", text_color="black",
                                               width=250)
        self.region_dropdown.grid(row=16, column=1, pady=(10,0), sticky="w", columnspan=2)

        self.latest_matchid_label = CTkLabel(self.frame, text="Latest Match ID",
                                             font=default_font)
        self.latest_matchid_label.grid(row=17, column=0, padx=10, pady=(10,0),
                                       sticky="w")
        self.latest_matchid_entry = CTkEntry(self.frame, font=default_font,
                                             placeholder_text="Enter Latest Match ID")
        self.latest_matchid_entry.grid(row=17, column=1, pady=(10,0), sticky="ew",
                                       columnspan=3)

        self.spreadsheet_header = CTkLabel(self.frame, text="Spreadsheet", 
                                     font=("Calibri Bold",18))
        self.spreadsheet_header.grid(row=18, column=0, padx=10, pady=(15,0), sticky="w")

        self.spreadsheet_format_label = CTkLabel(self.frame, text="Spreadsheet Format",
                                                 font=default_font)
        self.spreadsheet_format_label.grid(row=19, column=0, padx=10, pady=(10,0),
                                           sticky="w")
        
        self.spreadsheet_format_button = CTkButton(self.frame, text="Edit",
                                                   font=default_font, 
                                                   command=self.spreadsheet_format_function)
        self.spreadsheet_format_button.grid(row=19, column=1, pady=(10,0), sticky="w")

        self.spreadsheet_format_hoverbutton = HoverButton(self.frame, text="", image=question_image,
                                                 tooltip_text="What information will be in each column of your spreadsheet(s).",
                                                 width=15, fg_color="transparent",
                                                 hover_color="grey")
        self.spreadsheet_format_hoverbutton.grid(row=19, column=1, padx=140, pady=(10,0), sticky="w")
        self.spreadsheet_format_hoverbutton.configure(state="disabled")

        self.insert_r2_label = CTkLabel(self.frame, text="Insert at Row 2",
                                        font=default_font)
        self.insert_r2_label.grid(row=20, column=0, padx=10, pady=(10,0),
                                  sticky="w")
        self.insert_r2_switch_var = StringVar(value="off")
        self.insert_r2_switch  = CTkSwitch(self.frame, text="",
                                           variable=self.insert_r2_switch_var, onvalue="on",
                                           offvalue="off")
        self.insert_r2_switch.grid(row=20, column=1, pady=(10,0),
                                   sticky="w")
        
        self.insert_r2_hoverbutton = HoverButton(self.frame, text="", image=question_image,
                                            tooltip_text="When turned on, new matches will be inserted at the 2nd row of your\nspreadsheet instead of being appended to the bottom.",
                                            width=15, fg_color="transparent",
                                            hover_color="grey")
        self.insert_r2_hoverbutton.grid(row=20, column=1, padx=40, pady=(10,0),
                                        sticky="w")
        self.insert_r2_hoverbutton.configure(state="disabled")

        self.switch_var_spreadsheet = StringVar(value="off")
        self.switch_googlesheet_label = CTkLabel(self.frame, text="Google Sheets",
                                       font=default_font)
        self.switch_googlesheet_label.grid(row=21, column=0, pady=(10,0), padx=10, sticky="w")
        self.switch_googlesheet = CTkSwitch(self.frame, text="", command=self.googlesheet_switch,
                                       variable=self.switch_var_spreadsheet, onvalue="on",
                                       offvalue="off")
        self.switch_googlesheet.grid(row=21, column=1, pady=(10,0), sticky="w")

        self.spreadsheet_name_label = CTkLabel(self.frame, text="Spreadsheet Name",
                                               font=default_font)
        self.spreadsheet_name_label.grid(row=22, column=0, pady=(10,0), padx=10,
                                         sticky="w")
        self.spreadsheet_name_entry = CTkEntry(self.frame, font=default_font,
                                               placeholder_text="Enter spreadsheet name (Google Sheets)")
        self.spreadsheet_name_entry.grid(row=22, column=1, pady=(10,0), sticky="ew",
                                         columnspan=3)
        
        self.google_service_key_label = CTkLabel(self.frame, text="Google Service Acc. Key",
                                                 font=default_font)
        self.google_service_key_label.grid(row=23, column=0, padx=10, pady=(10,0),
                                           sticky="w")
        self.google_service_key_entry = CTkEntry(self.frame, font=default_font,
                                                 placeholder_text="Location of key (C:/...)")
        self.google_service_key_entry.grid(row=23, column=1, pady=(10,0), sticky="ew",
                                           columnspan=4)
        self.google_key_dirchange = CTkButton(self.frame, text="Change  ", font=default_font,
                                       width=70, command=self.google_key_dirchange_function,
                                       image=change_dir)
        self.google_key_dirchange.grid(row=23, column=5, pady=(10,0), padx=5)

        self.excel_switch_var = StringVar(value="off")
        self.excel_switch_label = CTkLabel(self.frame, text="Excel",
                                       font=default_font)
        self.excel_switch_label.grid(row=24, column=0, pady=(10,0), padx=10, sticky="w")
        self.switch_excel = CTkSwitch(self.frame, text="", command=self.excel_switch,
                                       variable=self.excel_switch_var, onvalue="on",
                                       offvalue="off")
        self.switch_excel.grid(row=24, column=1, pady=(10,0), sticky="w")

        self.excel_file_path_label = CTkLabel(self.frame, text="Excel File Path",
                                        font=default_font)
        self.excel_file_path_label.grid(row=25, column=0, padx=10, pady=10,
                                  sticky="w")

        self.excel_file_path_dir = CTkEntry(self.frame, font=default_font,
                                            placeholder_text="Location of excel spreadsheet (C:/...)")
        self.excel_file_path_dir.grid(row=25, column=1, pady=10, sticky="ew",
                                      columnspan=4)
        self.excel_change = CTkButton(self.frame, text="Change  ", font=default_font,
                                width=70, command=self.excel_dir_change,
                                image=change_dir)
        self.excel_change.grid(row=25, column=5, pady=10, padx=5)

        self.check_info() # When settings window set up, check_info function to input current settings

    def check_info(self):
        # Collect all settings
        self.autoupload_video = h.get_setting(*c.AUTOUPLOAD_VIDEOS_SETTING_LOCATOR, boolean=True)
        self.firefox_profile_dir = h.get_setting(*c.FIREFOX_PROFILE_SETTING_LOCATOR)
        self.bg_process = h.get_setting(*c.BACKGROUND_PROCESS_SETTING_LOCATOR, boolean=True)
        self.max_vids = h.get_setting(*c.MAX_VIDEOS_SIMULTANEOUSLY_SETTING_LOCATOR)
        self.visibility = h.get_setting(*c.VIDEO_VISIBILITY_SETTING_LOCATOR)
        self.autoselect_video = h.get_setting(*c.AUTOSELECT_VIDEOS_SETTING_LOCATOR, boolean=True)
        self.video_directory = h.get_setting(*c.VIDEO_DIRECTORY_SETTING_LOCATOR)
        self.recording_client = h.get_setting(*c.RECORDING_CLIENT_SETTING_LOCATOR)
        self.filename_format = h.get_setting(*c.FILENAME_FORMAT_SETTING_LOCATOR)
        self.recording_delay = h.get_setting(*c.RECORDING_START_DELAY_SETTING_LOCATOR)
        self.puuid_setting_locator = h.get_setting(*c.PUUID_SETTING_LOCATOR)
        self.region_setting = h.get_setting(*c.AFFINITY_SETTING_LOCATOR)
        self.latest_match = h.get_setting(*c.LATEST_MATCH_ID_SETTING_LOCATOR)
        self.spreadsheet_name = h.get_setting(*c.GOOGLE_SHEETS_NAME_SETTING_LOCATOR)
        self.service_account_json = h.get_setting(*c.GOOGLE_SERVICE_ACCOUNT_KEY_JSON_PATH_LOCATOR)
        self.spreadsheet_row2 = h.get_setting(*c.INSERT_TO_ROW_2_LOCATOR, boolean=True)
        self.write_to_excel = h.get_setting(*c.WRITE_TO_EXCEL_FILE_SETTING_LOCATOR, boolean=True)
        self.excel_file_path = h.get_setting(*c.EXCEL_FILE_PATH_SETTING_LOCATOR)
        self.write_to_googlesheets = h.get_setting(*c.WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR, boolean=True)
        
        # Insert vals into all entries, dropdowns etc.
        if self.max_vids:
            self.maxvids_sim_entry.delete(0,END)
            self.maxvids_sim_entry.insert(END, self.max_vids)
        else:
            pass
        if self.autoupload_video is True:
            self.switch_var.set("on")
            self.switch1()
        else:
            self.switch_var.set("off")
            self.switch1()

        if self.firefox_profile_dir: 
            self.firefox_entry.delete(0,END)
            self.firefox_entry.insert(END, self.firefox_profile_dir)
        else:
            pass

        if self.bg_process is True:
            self.background_process_var.set("on")
        else:
            self.background_process_var.set("off")
        
        if self.visibility:
            self.visibility_dropdown.set(c.VIDEO_VISIBILITY_OPTIONS[self.visibility])
        else:
            pass        

        if self.autoselect_video is True:
            self.switch_var2.set("on")
            self.switch2()
        else:
            self.switch_var2.set("off")
            self.switch2()

        if self.video_directory:
            self.viddir_entry.delete(0,END)
            self.viddir_entry.insert(END, self.video_directory)
        else:
            pass

        if self.recording_client:
            self.filename_format_optionmenu.set(c.RECORDING_CLIENT_OPTIONS[self.recording_client])
            self.filename_format_entry.delete(0,END)
            self.filename_format_entry.insert(END, (c.RECORDING_CLIENT_FILENAME_FORMATS[self.recording_client]))
            self.filename_format_entry.configure(state="disabled")
        else:
            self.filename_format_optionmenu.set(c.RECORDING_CLIENT_OPTIONS[self.recording_client])
            self.filename_format_entry.configure(state="normal")
            if self.filename_format:
                self.filename_format_entry.delete(0,END)
                self.filename_format_entry.insert(END, self.filename_format)

        if self.recording_delay:
            self.slider_value.delete(0,END)
            self.slider_value.insert(END, self.recording_delay)
            self.recording_delay_slider.set(int(self.recording_delay))
        else:
            pass

        if self.puuid_setting_locator:
            self.puuid_entry.delete(0,END)
            self.puuid_entry.insert(END, self.puuid_setting_locator)
        else:
            pass

        if self.region_setting:
            self.region_dropdown.set(c.REGION_OPTIONS[self.region_setting])
        else:
            pass

        if self.latest_match:
            self.latest_matchid_entry.delete(0,END)
            self.latest_matchid_entry.insert(END, self.latest_match)
        else:
            pass

        if self.spreadsheet_name:
            self.spreadsheet_name_entry.delete(0,END)
            self.spreadsheet_name_entry.insert(END, self.spreadsheet_name)
        else:
            pass

        if self.service_account_json:
            self.google_service_key_entry.delete(0,END)
            self.google_service_key_entry.insert(END, self.service_account_json)
        else:
            pass

        if self.spreadsheet_row2 is True:
            self.insert_r2_switch_var.set("on")
        else:
            self.insert_r2_switch_var.set("off")

        if self.write_to_excel is True:
            self.excel_switch_var.set("on")
            self.excel_switch()
        else:
            self.excel_switch_var.set("off")
            self.excel_switch()
        
        if self.excel_file_path:
            self.excel_file_path_dir.delete(0,END)
            self.excel_file_path_dir.insert(END, self.excel_file_path)
        else:
            pass

        if self.write_to_googlesheets is True:
            self.switch_var_spreadsheet.set("on")
            self.googlesheet_switch()
        else:
            self.switch_var_spreadsheet.set("off")
            self.googlesheet_switch()

    
    def switch1(self): # Auto-upload setting switch
        self.val = self.switch_onoff.get() # Get switch val
        if self.val == "off": # If switch is off, disable all objects under auto-upload
            self.firefox_entry.configure(state="disabled")
            self.firefox_change.configure(state="disabled")
            self.firefox_profile_label.configure(text_color = "grey")
            self.firefox_entry.configure(placeholder_text_color="#c9c9c9",
                                         text_color="grey")
            self.background_process_label.configure(text_color = "grey")
            self.background_process_switch.configure(state="disabled")
            self.maxvids_sim_label.configure(text_color = "grey")
            self.maxvids_sim_entry.configure(state="disabled",
                                             text_color="grey")
            self.visibility_label.configure(text_color = "grey")
            self.visibility_dropdown.configure(state="disabled")
        elif self.val == "on": # If switch is on, enable all objects
            self.firefox_entry.configure(state="normal")
            self.firefox_change.configure(state="normal")
            self.firefox_profile_label.configure(text_color = "black")
            self.firefox_entry.configure(placeholder_text_color="grey",
                                         text_color="black")
            self.background_process_label.configure(text_color = "black")
            self.background_process_switch.configure(state="normal")
            self.maxvids_sim_label.configure(text_color = "black")
            self.maxvids_sim_entry.configure(state="normal",
                                             text_color="black")
            self.visibility_label.configure(text_color = "black")
            self.visibility_dropdown.configure(state="normal")

    def switch2(self): # Auto-select vids setting switch
        self.val2 = self.switch_onoff2.get() # Get switch val
        if self.val2 == "off": # If switch is off, disable all objects under auto-select
            self.viddir_label.configure(text_color="grey")
            self.viddir_entry.configure(state="disabled", 
                                        placeholder_text_color="#c9c9c9",
                                        text_color="grey")
            self.viddir_change.configure(state="disabled")
            self.filename_format_label.configure(text_color="grey")
            self.filename_format_entry.configure(state="disabled",
                                                 placeholder_text_color="#c9c9c9",
                                                 text_color="grey")
            self.recording_delay_label.configure(text_color="grey")
            self.recording_delay_slider.configure(state="disabled")
            self.secs_label.configure(text_color="grey")
            self.slider_value.configure(state="disabled",
                                        text_color="grey")
            self.filename_hover_button.configure(state="disabled")
            self.recording_client_label.configure(text_color="grey")
            self.filename_format_optionmenu.configure(state="disabled")
        elif self.val2 == "on": # If switch is on, enable all objects
            self.viddir_label.configure(text_color="black")
            self.viddir_entry.configure(state="normal",
                                        placeholder_text_color="grey",
                                        text_color="black")
            self.viddir_change.configure(state="normal")
            self.filename_format_label.configure(text_color="black")
            self.filename_format_entry.configure(state="normal",
                                                 placeholder_text_color="grey",
                                                 text_color="black")
            self.recording_delay_label.configure(text_color="black")
            self.recording_delay_slider.configure(state="normal")
            self.secs_label.configure(text_color="black")
            self.slider_value.configure(state="normal",
                                        text_color="black")
            self.filename_hover_button.configure(state="disabled")
            self.recording_client_label.configure(text_color="black")
            self.filename_format_optionmenu.configure(state="normal")

    def viddir_change_function(self): # Change the video directory
        self.file = filedialog.askdirectory(title="Open")
        self.viddir_entry.delete(0,END)
        self.viddir_entry.insert(END, self.file)

    def filename_format_options(self, recording_client):
        if recording_client == "Custom": # If the recording_client is set to custom, clear the format entry box
            self.filename_format_entry.configure(state="normal")
            self.filename_format_entry.delete(0,END)
        else: # All others, disable format entry box and insert default format for that recording client
            self.filename_format_entry.configure(state="normal")
            recording_client_new = h.get_key_from_value(c.RECORDING_CLIENT_OPTIONS, recording_client)
            filename_format = c.RECORDING_CLIENT_FILENAME_FORMATS[recording_client_new]
            self.filename_format_entry.delete(0,END)
            self.filename_format_entry.insert(END, filename_format)
            self.filename_format_entry.configure(state="disabled")
         
    def firefoxprofile_change_function(self): # Change firefox profile directory
        self.file2 = filedialog.askdirectory(title="Open")
        self.firefox_entry.delete(0, END)
        self.firefox_entry.insert(END, self.file2)

    def slider(self, value): # Changes the value of the slider entry box
        intvalue = int(value)
        self.slider_value.delete(0, END)
        self.slider_value.insert(END, intvalue)
    
    def find_puuid_function(self): # Finds user PUUID based on username and tag
        name_entry = self.username_entry.get()
        tag_entry = self.tag_entry.get()
        if not name_entry:
            messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid username.")
            return
        elif not tag_entry:
            messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid tag.")
            return
        self.puuid = h.find_puuid(name_entry, tag_entry)
        self.puuid_entry.delete(0, END)
        self.puuid_entry.insert(END, self.puuid)
    
    def google_key_dirchange_function(self): # Change the path to Google key (.json files)
        self.jsonfile = filedialog.askopenfilename(title="Open", filetypes=[("JSON Files (*.json)", "*.json")])
        self.google_service_key_entry.delete(0, END)
        self.google_service_key_entry.insert(END, self.jsonfile)

    def spreadsheet_format_function(self): # Opens the spreadsheet format window
        edit_app = SpreadsheetFormat()
        edit_app.mainloop()
    
    def googlesheet_switch(self): # Write to Google Sheets switch
        self.googlesheet_val = self.switch_var_spreadsheet.get()
        if self.googlesheet_val == "off": # If switch is off, disable all objects under G.Sheets
            self.spreadsheet_name_label.configure(text_color="grey")
            self.spreadsheet_name_entry.configure(state="disabled",
                                                 placeholder_text_color="#c9c9c9",
                                                 text_color="grey")
            self.google_service_key_label.configure(text_color="grey")
            self.google_service_key_entry.configure(state="disabled",
                                                 placeholder_text_color="#c9c9c9",
                                                 text_color="grey")
            self.google_key_dirchange.configure(state="disabled")
        elif self.googlesheet_val == "on": # If switch is on, enable all objects
            self.spreadsheet_name_label.configure(text_color="black")
            self.spreadsheet_name_entry.configure(state="normal",
                                                 placeholder_text_color="grey",
                                                 text_color="black")
            self.google_service_key_label.configure(text_color="black")
            self.google_service_key_entry.configure(state="normal",
                                                 placeholder_text_color="grey",
                                                 text_color="black")
            self.google_key_dirchange.configure(state="normal")

    def excel_switch(self): # Write to Excel switch
        self.excel_val = self.excel_switch_var.get()
        if self.excel_val == "off": # If switch is off, disable all objects under Excel
            self.excel_file_path_label.configure(text_color="grey")
            self.excel_file_path_dir.configure(state="disabled",
                                                 placeholder_text_color="#c9c9c9",
                                                 text_color="grey")
            self.excel_change.configure(state="disabled")
        elif self.excel_val == "on": # If switch is on, enable all objects
            self.excel_file_path_label.configure(text_color="black")
            self.excel_file_path_dir.configure(state="normal",
                                                 placeholder_text_color="grey",
                                                 text_color="black")
            self.excel_change.configure(state="normal")

    def excel_dir_change(self): # Change file path for Excel Spreadsheet
        self.excelfile = filedialog.askopenfilename(title="Open", filetypes=[
            ("Excel Workbook (*.xlsx)", "*.xlsx"),
            ("Excel Macro-Enabled Workbook (*.xlsm)", "*.xlsm"),
            ("Excel Template (*.xltx)", "*.xltx"),
            ("Excel Macro-Enabled Template (*.xltm)", "*.xltm")
            ])
        self.excel_file_path_dir.delete(0, END)
        self.excel_file_path_dir.insert(END, self.excelfile)

    def save_settings(self): # Saves all new settings
        if self.val == "on":
            if self.autoupload_video is not True: # Changes auto-upload vid switch val
                h.edit_setting(*c.AUTOUPLOAD_VIDEOS_SETTING_LOCATOR, "True")
            if not self.firefox_entry.get():
                messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid Firefox Profile Path.")
                return
            if os.path.exists(self.firefox_entry.get()):
                if self.firefox_entry.get() != self.firefox_profile_dir: # Changes Firefox profile directory
                    h.edit_setting(*c.FIREFOX_PROFILE_SETTING_LOCATOR, self.firefox_entry.get())
            else:
                firefox_retry = messagebox.askokcancel(title="Invalid File", 
                message=f"Firefox Profile Path: This directory was not found.\nPlease select a valid directory.",
                icon="error")
                if firefox_retry is True:
                    self.firefoxprofile_change_function()
                else:
                    return 
                
        if self.visibility_dropdown.get() != c.VIDEO_VISIBILITY_SETTING_LOCATOR: # Changes visibility dropdown val
            visibility_new = h.get_key_from_value(c.VIDEO_VISIBILITY_OPTIONS, self.visibility_dropdown.get())
            h.edit_setting(*c.VIDEO_VISIBILITY_SETTING_LOCATOR, visibility_new)

        self.background_process_setting = self.background_process_switch.get()
        if self.background_process_setting == "off": # Changes background process switch val
            if self.bg_process is True:
                h.edit_setting(*c.BACKGROUND_PROCESS_SETTING_LOCATOR, "False")
            elif self.background_process_setting == "on":
                if self.bg_process is not True:
                    h.edit_setting(*c.BACKGROUND_PROCESS_SETTING_LOCATOR, "True")
                
        if self.maxvids_sim_entry.get():
            try: # Integer testing for max. vids entry box
                max_vids = int(self.maxvids_sim_entry.get())
            except ValueError:
                messagebox.showerror(title="Invalid Input", message="Max. Vids Simultaneously: Please enter a valid integer.")
                return
        else:
            messagebox.showerror(title="Invalid Input", message="Max. Vids Simultaneously: Please enter a valid integer.")
            return

        if max_vids != c.MAX_VIDEOS_SIMULTANEOUSLY_SETTING_LOCATOR: # Changes max. vids setting
            h.edit_setting(*c.MAX_VIDEOS_SIMULTANEOUSLY_SETTING_LOCATOR, max_vids)

        if self.val == "off": # Changes auto-upload vid switch val
            if self.autoupload_video is True:
                h.edit_setting(*c.AUTOUPLOAD_VIDEOS_SETTING_LOCATOR, "False")

        if self.val2 == "on":
            if self.autoselect_video is not True:
                h.edit_setting(*c.AUTOSELECT_VIDEOS_SETTING_LOCATOR, "True")
            if not self.viddir_entry.get():
                messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid video directory.")
                return
            if os.path.exists(self.viddir_entry.get()):
                if self.viddir_entry.get() != self.video_directory: # Changes video directory
                    h.edit_setting(*c.VIDEO_DIRECTORY_SETTING_LOCATOR, self.viddir_entry.get())
            else:
                viddir_retry = messagebox.askokcancel(title="Invalid File", 
                message=f"Video Directory: This directory was not found.\nPlease select a valid directory.",
                icon="error")
                if viddir_retry is True:
                    self.viddir_change_function()
                else:
                    pass
        if self.val2 == "off":
            if self.autoselect_video is True:
                h.edit_setting(*c.AUTOSELECT_VIDEOS_SETTING_LOCATOR, "False")

        recording_client_new = h.get_key_from_value(c.RECORDING_CLIENT_OPTIONS, self.filename_format_optionmenu.get())
        if recording_client_new != self.recording_client: # Changes recording client
            h.edit_setting(*c.RECORDING_CLIENT_SETTING_LOCATOR, recording_client_new)
        
        if self.filename_format_entry.get(): # Changes filename format
            if self.filename_format_entry.get() != c.FILENAME_FORMAT_SETTING_LOCATOR:
                h.edit_setting(*c.FILENAME_FORMAT_SETTING_LOCATOR, self.filename_format_entry.get())
        else:
            messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid filename format.")
            return
        
        if self.slider_value.get():
            try: # Integer testing for slider val entry box
                integer_slider = int(self.slider_value.get())
            except ValueError:
                messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid recording delay (must be an integer).")
                return

            if self.slider_value.get() != self.recording_delay: # Changes recording delay
                h.edit_setting(*c.RECORDING_START_DELAY_SETTING_LOCATOR, self.slider_value.get())
        else:
            messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid recording delay (must be an integer).")
            return

        if not self.puuid_entry.get():
            messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid PUUID.")
            return
        else:
            puuid_setting = h.get_setting(*c.PUUID_SETTING_LOCATOR)
            if self.puuid_entry.get() != puuid_setting: # Changes PUUID
                h.edit_setting(*c.PUUID_SETTING_LOCATOR, self.puuid_entry.get())
            
        translated_region = h.get_key_from_value(c.REGION_OPTIONS, self.region_dropdown.get())
        if translated_region != self.region_setting: # Changes region
            h.edit_setting(*c.AFFINITY_SETTING_LOCATOR, translated_region)

        if self.latest_matchid_entry.get(): # Changes latest Match ID
            if self.latest_matchid_entry.get() != self.latest_match:
                h.edit_setting(*c.LATEST_MATCH_ID_SETTING_LOCATOR, self.latest_matchid_entry.get())
        else:
            messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid latest match ID.")
            return

        r2_setting = self.insert_r2_switch.get()
        if r2_setting == "off": # Changes insert at row 2 setting
            if self.spreadsheet_row2 is True:
                h.edit_setting(*c.INSERT_TO_ROW_2_LOCATOR, "False")
        elif r2_setting == "on":
            if self.spreadsheet_row2 is not True:
                h.edit_setting(*c.INSERT_TO_ROW_2_LOCATOR, "True")

        self.googlesheets_setting = self.switch_googlesheet.get()    
        if self.googlesheets_setting == "off": # Changes write to Google Sheets setting
            if self.write_to_googlesheets is True:
                h.edit_setting(*c.WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR, "False")
        elif self.googlesheets_setting == "on":
            if self.write_to_googlesheets is not True:
                h.edit_setting(*c.WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR, "True")

            if self.spreadsheet_name_entry.get():
                if self.spreadsheet_name_entry.get() != self.spreadsheet_name: # Changes sheet name
                    h.edit_setting(*c.GOOGLE_SHEETS_NAME_SETTING_LOCATOR, self.spreadsheet_name_entry.get())
            else:
               messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid spreadsheet name (Google Sheets).")
            
            if self.google_service_key_entry.get():      
                if os.path.exists(self.google_service_key_entry.get()):
                    if self.google_service_key_entry.get() != self.service_account_json: # Changes Google key
                        h.edit_setting(*c.GOOGLE_SERVICE_ACCOUNT_KEY_JSON_PATH_LOCATOR, self.google_service_key_entry.get())
                else:
                    keydir = messagebox.askokcancel(title="Invalid File", 
                    message=f"JSON File Directory: This directory was not found.\nPlease select a valid directory.",
                    icon="error")
                    if keydir is True:
                        self.google_key_dirchange_function()
                    else:
                        pass
            else:
               messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a path to a valid JSON file.")

        self.excel_setting = self.switch_excel.get()
        if self.excel_setting == "off": # Changes write to Excel setting
            if self.write_to_excel is True:
                h.edit_setting(*c.WRITE_TO_EXCEL_FILE_SETTING_LOCATOR, "False")
        elif self.excel_setting == "on":
            if self.write_to_excel is not True:
                h.edit_setting(*c.WRITE_TO_EXCEL_FILE_SETTING_LOCATOR, "True")
        
            if self.excel_file_path_dir.get():    
                if os.path.exists(self.excel_file_path_dir.get()):
                    if self.excel_file_path_dir.get() != self.excel_file_path: # Changes Excel path
                        h.edit_setting(*c.EXCEL_FILE_PATH_SETTING_LOCATOR, self.excel_file_path_dir.get())
                else:
                    exceldir = messagebox.askokcancel(title="Invalid File", 
                    message=f"Excel File Directory: This directory was not found.\nPlease select a valid directory.",
                    icon="error")
                    if exceldir is True:
                        self.excel_dir_change()
                    else:
                        pass
            else:
                messagebox.showerror(title="Invalid Input", 
                                    message=f"Please enter a path to a valid Excel file.")

        messagebox.showinfo(title="Success", message="Settings have been saved.") # Success message

    def reset_function(self): # Resets settings to default
        self.reset_confirmation = messagebox.askquestion(title="Confirmation", 
                                                      message="Are you sure you would like to reset to default settings?\nAll current settings will be wiped.",
                                                      icon="warning")
        if self.reset_confirmation == "yes":
            h.make_default_settings_file(c.DEFAULT_SETTINGS)
            SettingsWindow.destroy(self) # Reloads the window
            settings = SettingsWindow()
            settings.mainloop()
        else:
            messagebox.showinfo(title="Info", message="This operation has been cancelled.")

class SpreadsheetFormat(Toplevel): # Spreadsheet format window (Toplevel)
    def __init__(self):
        super().__init__()
        self.geometry("500x680")
        self.title("Settings (Spreadsheet Format)")
        self.iconbitmap("logo.ico")
                
        self.frame = CTkScrollableFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Sets up lists
        self.dropdown_menus_list = []
        self.format_columns_list = []

        self.row_count = -1

        # Configures objects in window
        self.spreadsheet_format_label = CTkLabel(self.frame, text="Spreadsheet Format\n(Columns)",
                                                    font=default_font)
        self.spreadsheet_format_label.grid(row=0, column=0, padx=(10,20), pady=(10,0),
                                            sticky="w")
        self.spreadsheet_format_list = list(c.SPREADSHEET_FORMAT_OPTIONS.values())
        
        self.plus_button = CTkButton(self.frame, text="+", font=default_font,
                                        command=self.add_boxes, width=20, corner_radius=20)
        self.plus_button.grid(row=0, column=3, padx=10, pady=(10,0), sticky="e")

        self.minus_button = CTkButton(self.frame, text="-", font=default_font,
                                        command=self.subtract_boxes, width=20, corner_radius=20)
        self.minus_button.grid(row=0, column=4, padx=0, pady=(10,0), sticky="w")

        self.save_button = CTkButton(self.frame, text="Save", font=default_font,
                                     width=100, image=save_image, command=self.save_format_changes)
        self.save_button.grid(row=1, column=0, padx=10, pady=(20,0), sticky="w")
        spreadsheet_format = h.get_setting(*c.SPREADSHEET_FORMAT_LOCATOR)

        if spreadsheet_format: # If there is data in the spreadsheet format setting, add rows in window
            items = spreadsheet_format.split(",")
            for index, item in enumerate(items):
                current_setting = c.SPREADSHEET_FORMAT_OPTIONS[item]
                
                self.add_boxes(current_setting, True if index == 0 else False) # Adds dropdown menus


    def add_boxes(self, value: str="-", disabled: bool=False) -> None:
        count = len(self.dropdown_menus_list) + 1
        self.final_count = self.row_count + count
        index = count - 1

        count_number = CTkLabel(self.frame, text=f"{count}.", font=default_font)
        count_number.grid(row=self.final_count, column=1, pady=(10,0),
                                padx=10, sticky="w")
        dropdown_menu = CTkOptionMenu(self.frame, 
                                values=self.spreadsheet_format_list,
                                command=lambda new_value: self.edit_column(index, new_value),
                                font=default_font, button_color="grey",
                                button_hover_color="dark grey",
                                fg_color="white", text_color="black")
        dropdown_menu.configure(state="normal")
        
        dropdown_menu.set(value)
        self.edit_column(index, value)
        dropdown_menu.grid(row=self.final_count, column=2, pady=(10,0),
                                sticky="ew")
        self.dropdown_menus_list.append((count_number, dropdown_menu))

    def subtract_boxes(self) -> None:
        count = len(self.dropdown_menus_list) + 1

        if count > 1:
            self.final_count = self.row_count + count
            last_dropdown_menu = self.dropdown_menus_list.pop()

            for element in last_dropdown_menu:
                element.grid_forget()
                element.destroy()

            self.format_columns_list.pop()

    def edit_column(self, index: int, value: str) -> None:
        # Looks in the SPREADSHEET_FORMAT_OPTIONS dict for the value and returns the corresponding key (e.g. "Match ID" returns "match_id")
        formatted_value = h.get_key_from_value(c.SPREADSHEET_FORMAT_OPTIONS, value)

        try:
            self.format_columns_list[index] = formatted_value
        except IndexError:
            self.format_columns_list.append(formatted_value)

    def save_format_changes(self): # Saves changes to spreadsheet format
        self.format_settings_change = ",".join(self.format_columns_list)
        self.format_setting_locator = h.get_setting(*c.SPREADSHEET_FORMAT_LOCATOR)

        if self.format_settings_change != self.format_setting_locator:
            h.edit_setting(*c.SPREADSHEET_FORMAT_LOCATOR, self.format_settings_change)

if __name__ == "__main__":
    app = App()
    app.mainloop()