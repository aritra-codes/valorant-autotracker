import os
import sys
import threading
from tkinter import Toplevel, messagebox, scrolledtext
import webbrowser

from customtkinter import (set_appearance_mode, set_default_color_theme,
                           CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame,
                           filedialog, END, CTkBaseClass,
                           CTkOptionMenu, CTkScrollableFrame)

from utils.misc import get_key_from_value, get_ctk_image
from utils.path import get_resource_path
from utils.settings import (get_setting, edit_setting, make_default_settings_file,
                            InvalidSettingsError)
import valorant_autotracker.constants as c
from valorant_autotracker.gui_classes import (SettingsTooltip, SettingsButton, SettingsEntry,
                                              SettingsHeader, SettingsLabel, SettingsOptionMenu,
                                              SettingsSlider, SettingsSwitch)
import valorant_autotracker.helpers as h
from valorant_autotracker.main import main as script

set_appearance_mode("light") # Set theme
set_default_color_theme(c.DEFAULT_COLOR_THEME)

# Define the image path for all images used
change_dir = get_ctk_image(c.FOLDER_IMAGE_PATH, c.FOLDER_IMAGE_PATH)
find_image = get_ctk_image(c.FIND_IMAGE_PATH["dark"], c.FIND_IMAGE_PATH["light"])
save_image = get_ctk_image(c.SAVE_IMAGE_PATH, c.SAVE_IMAGE_PATH)
reset_image = get_ctk_image(c.RESET_IMAGE_PATH, c.RESET_IMAGE_PATH)
return_image = get_ctk_image(c.RETURN_IMAGE_PATH, c.RETURN_IMAGE_PATH)
pencil_image = get_ctk_image(c.PENCIL_IMAGE_PATH, c.PENCIL_IMAGE_PATH)
run_image = get_ctk_image(c.RUN_IMAGE_PATH["dark"], c.RUN_IMAGE_PATH["light"])
settings_image = get_ctk_image(c.SETTINGS_IMAGE_PATH["dark"], c.SETTINGS_IMAGE_PATH["light"])
github_image = get_ctk_image(c.GITHUB_IMAGE_PATH, c.GITHUB_IMAGE_PATH)

class PrintLogger():
    """File like object"""
    def __init__(self, textbox):  # Pass reference to text widget
        sys.stdout = self
        sys.stderr = self
        self.textbox = textbox  # Keep reference

    def write(self, text):
        """Writes output to textbox"""
        self.textbox.configure(state="normal")  # Make field editable
        self.textbox.insert(END, f"{text}\n")  # Write text to textbox
        self.textbox.see(END)  # Scroll to end
        self.textbox.configure(state="disabled")  # Make field readonly

    # Needed for file-like object
    def flush(self):
        pass

class App(CTk):
    """Main application class"""
    def __init__(self):
        super().__init__()

        self.geometry(c.MAIN_WINDOW_RESOLUTION) # Set the window size (can be resizable)
        self.iconbitmap(get_resource_path(c.LOGO_IMAGE_PATH)) # Set logo
        self.title(c.APP_TITLE)

        # Create a frame
        self.frame = CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)

        # Create a button to run the main script
        self.run = CTkButton(self.frame, text="Run",
                             width=200, height=40,
                             image=run_image,
                             font=c.DEFAULT_FONT,
                             command=self.thread_script)
        self.run.pack(pady=(20,0))

        # Create a button to open settings window (class)
        settings_button = CTkButton(self.frame, text="Settings",
                                    width=200, height=40,
                                    image=settings_image,
                                    font=c.DEFAULT_FONT,
                                    command=self.open_settings)
        settings_button.pack(pady=(10,0))

        # Create a Github follow button
        github = CTkButton(self.frame,
                           text="Follow us on Github",
                           width=200, height=40,
                           image=github_image,
                           font=c.DEFAULT_FONT,
                           command=self.open_github_profiles)
        github.pack(pady=(10,0))

        # Entry box displays console output
        output_label = CTkLabel(self.frame, text="Output:", font=c.DEFAULT_FONT)
        output_label.pack(pady=(10,0))

        output_entry = scrolledtext.ScrolledText(self.frame, bd=1,
                                                 font=("Consolas", 9),
                                                 height=8)
        output_entry.pack(expand=True, fill="both", pady=(10,20), padx=20)
        output_entry.configure(state="disabled")

        PrintLogger(output_entry) # Ref to entry box for console output

    def thread_script(self):
        def run_script():
            self.run.configure(text="Running...", fg_color="#325882", state="disabled")
            try:
                script()
            except Exception as e:
                print(e)
            self.run.configure(text="Run", fg_color="#3A7EBF",state="normal")

        threading.Thread(target=run_script).start()

    def open_settings(self):
        """Opens the settings and minimises the main window"""
        self.state(newstate="iconic")
        SettingsWindow(self).mainloop()
        

    def maximise(self):
        self.state(newstate="normal")

    def open_github_profiles(self):
        webbrowser.open("https://github.com/lmdrums")
        webbrowser.open("https://github.com/aritra-codes")

def input_entry(entry: CTkEntry, value):
    entry.delete(0, END)
    entry.insert(END, value)

def filedialog_to_entry(entry: CTkEntry,
                        filetypes: list[tuple[str, str]]=None,
                        directory: bool=False) -> None:
    if directory:
        path = filedialog.askdirectory(title="Open")
    else:
        if not filetypes:
            filetypes = []

        path = filedialog.askopenfilename(title="Open", filetypes=filetypes)

    if path:
        input_entry(entry, path)

def validate_integer(value: str, label_text: str, minimum: int=None, maximum: int=None) -> bool:
    try:
        value = int(value)
    except ValueError:
        messagebox.showerror(title="Invalid Input",
                             message=f"{label_text}: Please enter an integer.")
        return False

    if minimum and not value >= minimum:
        messagebox.showerror(title="Invalid Integer",
                             message=f"{label_text}: Please enter an integer >= {minimum}.")
        return False
    if maximum and not value <= maximum:
        messagebox.showerror(title="Invalid Integer",
                             message=f"{label_text}: Please enter an integer <= {maximum}.")
        return False

    return True

def validate_path(value: str, label_text: str,
                  filetypes: list[tuple[str, str]]=None, directory: bool=False) -> bool:
    if directory:
        if not os.path.isdir(value):
            messagebox.showerror(title="Invalid Directory",
                                 message=f"{label_text}: Directory was not found.\nPlease enter a valid directory.")
            return False
    else:
        if not os.path.isfile(value):
            messagebox.showerror(title="Invalid File",
                                 message=f"{label_text}: File was not found.\nPlease enter a valid file path.")
            return False

        if filetypes:
            exts = [os.path.splitext(filetype[1])[1] for filetype in filetypes]

            if os.path.splitext(value)[1] not in exts:
                messagebox.showerror(title="Invalid File Type",
                                     message=f"{label_text}: File must be {"/".join(exts)}.")
                return False

    return True

class SettingsWindow(Toplevel):
    """Settings window"""
    def __init__(self, parent):
        super().__init__()

        self.parent: App = parent # Ref to parent window
        self.row: int = 0
        self.settings: list[CTkBaseClass] = []

        def increment_row(increment: int=1):
            self.row += increment

        self.geometry(c.SETTINGS_WINDOW_RESOLUTION)
        self.title(c.SETTINGS_TITLE)
        self.iconbitmap(get_resource_path(c.LOGO_IMAGE_PATH))

        self.frame = CTkScrollableFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        save_button = SettingsButton(self,
                                     text="Save All",
                                     width=100,
                                     image=save_image,
                                     command=self.save_settings)
        save_button.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="ew")

        reset = SettingsButton(self,
                               text="Reset to Default",
                               image=reset_image,
                               command=self.reset_settings, width=160)
        reset.grid(row=self.row, column=1, padx=(0,10), pady=(10,0), sticky="w")

        return_button = SettingsButton(self, text="Close and Return",
                                       width=150,
                                       image=return_image,
                                       fg_color="#e00b0b",
                                       hover_color="dark red",
                                       command=self.return_to_main)
        return_button.grid(row=self.row, column=1, pady=(10,0), sticky="e")

        increment_row()

        # General section

        self.general_header = SettingsHeader(self, text="General")
        self.general_header.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        increment_row()

        mdy_dates_label = SettingsLabel(self, text="Use M/D/Y Dates")
        mdy_dates_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        mdy_dates_switch = SettingsSwitch(self, mdy_dates_label,
                                          c.USE_MDY_DATES_SETTING_LOCATOR)
        mdy_dates_switch.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        increment_row()

        # Valorant section

        valorant_header = SettingsHeader(self, text="Valorant")
        valorant_header.grid(row=self.row, column=0, padx=10, pady=(15,0), sticky="w")

        increment_row()

        api_key_label = SettingsLabel(self, text="API Key")
        api_key_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        api_key_entry = SettingsEntry(self, api_key_label,
                                      c.API_KEY_SETTING_LOCATOR,
                                      placeholder_text="Enter API Key")
        api_key_entry.grid(row=self.row, column=1, pady=(10,0), sticky="ew")

        increment_row()

        def save_api_key() -> None:
            try:
                api_key_entry.save()
            except InvalidSettingsError:
                pass
            else:
                messagebox.showinfo(title="Success", message="API Key has been saved.")

        api_key_save = SettingsButton(self, text="Save API Key  ",
                                      width=100,
                                      image=save_image,
                                      command=save_api_key)
        api_key_save.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        increment_row()

        username_label = SettingsLabel(self, text="Username")
        username_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        username_entry = CTkEntry(self.frame,
                                  font=c.DEFAULT_FONT,
                                  placeholder_text="Enter username (for PUUID and Region)")
        username_entry.grid(row=self.row, column=1, pady=(10,0), sticky="ew")

        increment_row()

        tag_label = SettingsLabel(self, text="Tag")
        tag_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        tag_entry = CTkEntry(self.frame,
                             font=c.DEFAULT_FONT,
                             placeholder_text="Enter tag (for PUUID and Region)")
        tag_entry.grid(row=self.row, column=1, pady=(10,0), sticky="ew")

        increment_row()

        def find_puuid_region(name: str, tag: str):
            """Finds user PUUID and region based on username and tag"""
            if not name:
                messagebox.showerror(title="Invalid Input",
                                     message="Please enter a valid username.")
                return
            if not tag:
                messagebox.showerror(title="Invalid Input",
                                     message="Please enter a valid tag.")
                return

            api = h.ValorantAPI(get_setting(*c.API_KEY_SETTING_LOCATOR))

            try:
                puuid = api.find_puuid(name, tag)
                region = api.find_region(name, tag)
            except c.APIError as e:
                messagebox.showerror(title="API Error", message=e)
            else:
                input_entry(self.puuid_entry, puuid)

                self.region_dropdown.set(c.REGION_OPTIONS[region])

        puuid_find = CTkButton(self.frame,
                               text="Find PUUID and Region  ",
                               font=c.DEFAULT_FONT,
                               image=find_image,
                               width=110,
                               command=lambda: find_puuid_region(username_entry.get(), tag_entry.get()))
        puuid_find.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        increment_row()

        puuid_label = SettingsLabel(self, text="PUUID")
        puuid_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        self.puuid_entry = SettingsEntry(self, puuid_label,
                                         c.PUUID_SETTING_LOCATOR,
                                         placeholder_text="Enter PUUID")
        self.puuid_entry.grid(row=self.row, column=1, columnspan=3, pady=(10,0), sticky="ew")

        increment_row()

        region_label = SettingsLabel(self, text="Region")
        region_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        self.region_dropdown = SettingsOptionMenu(self, region_label,
                                                  c.AFFINITY_SETTING_LOCATOR,
                                                  c.REGION_OPTIONS,
                                                  width=250)
        self.region_dropdown.grid(row=self.row, column=1, pady=(10,0), sticky="w", columnspan=2)

        increment_row()

        latest_matchid_label = SettingsLabel(self, text="Latest Match ID")
        latest_matchid_label.grid(row=self.row, column=0, padx=10, pady=(10,0),
                                       sticky="w")

        latest_matchid_entry = SettingsEntry(self, latest_matchid_label,
                                             c.LATEST_MATCH_ID_SETTING_LOCATOR,
                                             False,
                                             placeholder_text="Enter Latest Match ID")
        latest_matchid_entry.grid(row=self.row, column=1, columnspan=3, pady=(10,0), sticky="ew")

        latest_matchid_hoverbutton = SettingsTooltip(self.frame,
                                                     tooltip_text="All the matches (limited to 10 latest) after this match will be inserted and/or uploaded.\nIf set to blank, it will return the last ~10 matches.")
        latest_matchid_hoverbutton.grid(row=self.row, column=4, pady=(10,0), sticky="w")
        latest_matchid_hoverbutton.configure(state="disabled")

        increment_row()

        # Video section

        self.video_header = SettingsHeader(self, text="Video")
        self.video_header.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        increment_row()

        autoupload_videos_label = SettingsLabel(self, text="Auto-Upload Videos")
        autoupload_videos_label.grid(row=self.row, column=0, pady=(10,0), padx=10, sticky="w")

        autoupload_videos_switch = SettingsSwitch(self, autoupload_videos_label,
                                                  c.AUTOUPLOAD_VIDEOS_SETTING_LOCATOR)
        autoupload_videos_switch.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        increment_row()

        firefox_profile_label = SettingsLabel(self, text="Firefox Profile Path")
        firefox_profile_label.grid(row=self.row, column=0, pady=(10,0), padx=10, sticky="w")

        firefox_entry = SettingsEntry(self,
                                      firefox_profile_label,
                                      c.FIREFOX_PROFILE_SETTING_LOCATOR,
                                      validate=lambda v, lt: validate_path(v, lt, directory=True),
                                      width=500,
                                      placeholder_text="Firefox profile path (C:/...)")
        firefox_entry.grid(row=self.row, column=1, pady=(10,0), columnspan=4)

        firefox_change = SettingsButton(self, text="Change  ",
                                        width=70,
                                        command=lambda: filedialog_to_entry(firefox_entry, directory=True),
                                        image=change_dir)
        firefox_change.grid(row=self.row, column=5, pady=(10,0), padx=5)

        autoupload_videos_switch.add_child_widget(firefox_entry)
        autoupload_videos_switch.add_child_widget(firefox_change)

        increment_row()

        background_process_label = SettingsLabel(self, text="Background Process")
        background_process_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        background_process_switch = SettingsSwitch(self,
                                                   background_process_label,
                                                   c.BACKGROUND_PROCESS_SETTING_LOCATOR)
        background_process_switch.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        background_process_hoverbutton = SettingsTooltip(self.frame,
                                                         tooltip_text="When turned on, Firefox will open in the background when\nuploading videos and not appear on your screen.")
        background_process_hoverbutton.grid(row=self.row, column=1, padx=40, pady=(10,0), sticky="w")
        background_process_hoverbutton.configure(state="disabled")

        autoupload_videos_switch.add_child_widget(background_process_switch)

        increment_row()

        maxvids_sim_label = SettingsLabel(self, text="Max. Vids Simultaneously")
        maxvids_sim_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")
        maxvids_sim_entry = SettingsEntry(self,
                                          maxvids_sim_label,
                                          c.MAX_VIDEOS_SIMULTANEOUSLY_SETTING_LOCATOR,
                                          validate=lambda v, lt: validate_integer(v, lt, 1),
                                          width=40,
                                          justify="center")
        maxvids_sim_entry.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        maxvids_hoverbutton = SettingsTooltip(self.frame,
                                              tooltip_text="The number of videos that can be uploaded at the same time.")
        maxvids_hoverbutton.grid(row=self.row, column=1, padx=40, pady=(10,0), sticky="w")
        maxvids_hoverbutton.configure(state="disabled")

        autoupload_videos_switch.add_child_widget(maxvids_sim_entry)

        increment_row()

        visibility_label = SettingsLabel(self, text="Visibility")
        visibility_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        visibility_dropdown = SettingsOptionMenu(self, visibility_label,
                                                 c.VIDEO_VISIBILITY_SETTING_LOCATOR,
                                                 c.VIDEO_VISIBILITY_OPTIONS)
        visibility_dropdown.grid(row=self.row, column=1, padx=2, pady=(10,0), sticky="w")

        autoupload_videos_switch.add_child_widget(visibility_dropdown)

        increment_row()

        autoselect_videos_label = SettingsLabel(self, text="Auto-Select Videos\n(Experimental)")
        autoselect_videos_label.grid(row=self.row, column=0, pady=(10,0), padx=10, sticky="w")

        autoselect_videos_switch = SettingsSwitch(self,
                                                  autoselect_videos_label,
                                                  c.AUTOSELECT_VIDEOS_SETTING_LOCATOR)
        autoselect_videos_switch.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        autoupload_videos_switch.add_child_widget(autoselect_videos_switch)

        increment_row()

        viddir_label = SettingsLabel(self, text="Video Directory")
        viddir_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        viddir_entry = SettingsEntry(self,
                                     viddir_label,
                                     c.VIDEO_DIRECTORY_SETTING_LOCATOR,
                                     validate=lambda v, lt: validate_path(v, lt, directory=True),
                                     width=500,
                                     placeholder_text="Video directory (C:/...)")
        viddir_entry.grid(row=self.row, column=1, pady=(10,0), columnspan=4)

        viddir_change = SettingsButton(self, text="Change  ",
                                       width=70,
                                       command=lambda: filedialog_to_entry(viddir_entry, directory=True),
                                       image=change_dir)
        viddir_change.grid(row=self.row, column=5, pady=(10,0), padx=5)

        autoselect_videos_switch.add_child_widget(viddir_entry)
        autoselect_videos_switch.add_child_widget(viddir_change)

        increment_row(2)

        filename_format_label = SettingsLabel(self, text="Filename Format")
        filename_format_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        filename_format_entry = SettingsEntry(self,
                                              filename_format_label,
                                              c.FILENAME_FORMAT_SETTING_LOCATOR,
                                              placeholder_text="Enter filename format",
                                              width=200)
        filename_format_entry.grid(row=self.row, column=1, columnspan=3, pady=(10,0), sticky="ew")

        filename_hover_button = SettingsTooltip(self.frame,
                                                tooltip_text="The format in which the recorded video files are named by the\nrecording client (written in Python datetime format codes).")
        filename_hover_button.grid(row=self.row, column=4, pady=(10,0), sticky="w")

        autoselect_videos_switch.add_child_widget(filename_format_entry)

        increment_row(-1)

        def insert_filename_format(recording_client: str):
            recording_client = get_key_from_value(c.RECORDING_CLIENT_OPTIONS, recording_client)

            filename_format_entry.configure(state="normal")
            input_entry(filename_format_entry, "")

            if not recording_client == "custom":
                filename_format = c.RECORDING_CLIENT_FILENAME_FORMATS[recording_client]
                input_entry(filename_format_entry, filename_format)

                filename_format_entry.save() # Won't save otherwise
                filename_format_entry.configure(state="disabled")

        recording_client_label = SettingsLabel(self, text="Recording Client")
        recording_client_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        recording_client_dropdown = SettingsOptionMenu(self,
                                                       recording_client_label,
                                                       c.RECORDING_CLIENT_SETTING_LOCATOR,
                                                       c.RECORDING_CLIENT_OPTIONS,
                                                       command=insert_filename_format)
        recording_client_dropdown.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        autoselect_videos_switch.add_child_widget(recording_client_dropdown)

        increment_row(2)

        recording_delay_label = SettingsLabel(self, text="Recording Delay")
        recording_delay_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        recording_delay_entry = SettingsEntry(self,
                                              recording_delay_label,
                                              c.RECORDING_START_DELAY_SETTING_LOCATOR,
                                              validate=lambda v, lt: validate_integer(v, lt, 0),
                                              width=40,
                                              justify="center")
        recording_delay_entry.grid(row=self.row, column=2, pady=(10,0), padx=(10,10), sticky="w")

        secs_label = SettingsLabel(self, text="secs")
        secs_label.grid(row=self.row, column=3, pady=(10,0), sticky="w")

        recording_delay_slider = SettingsSlider(self,
                                                secs_label,
                                                to=60,
                                                number_of_steps=60,
                                                command=lambda v: input_entry(recording_delay_entry, int(v)))
        recording_delay_slider.grid(row=self.row, column=1, pady=(10,0), sticky="ew")

        try:
            recording_delay_slider.set(int(recording_delay_entry.get()))
        except ValueError:
            recording_delay_slider.set(0)

        slider_hoverbutton = SettingsTooltip(self.frame,
                                             tooltip_text="How long it takes for the recording to start after the start of the match.")
        slider_hoverbutton.grid(row=self.row, column=3, padx=25, pady=(10,0))
        slider_hoverbutton.configure(state="disabled")

        autoselect_videos_switch.add_child_widget(recording_delay_slider)
        autoselect_videos_switch.add_child_widget(recording_delay_entry)

        increment_row()

        # Spreadsheet section

        spreadsheet_header = SettingsHeader(self, text="Spreadsheet")
        spreadsheet_header.grid(row=self.row, column=0, padx=10, pady=(15,0), sticky="w")

        increment_row()

        spreadsheet_format_label = SettingsLabel(self, text="Spreadsheet Format")
        spreadsheet_format_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        self.spreadsheet_format_button = SettingsButton(self,
                                                        text="Edit  ",
                                                        image=pencil_image,
                                                        command=self.open_spreadsheet_format)
        self.spreadsheet_format_button.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        spreadsheet_format_hoverbutton = SettingsTooltip(self.frame,
                                                         tooltip_text="What information will be in each column of your spreadsheet(s).")
        spreadsheet_format_hoverbutton.grid(row=self.row, column=1, padx=140, pady=(10,0), sticky="w")
        spreadsheet_format_hoverbutton.configure(state="disabled")

        increment_row()

        insert_r2_label = SettingsLabel(self, text="Insert at Row 2")
        insert_r2_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        self.insert_r2_switch = SettingsSwitch(self,
                                               insert_r2_label,
                                               c.INSERT_TO_ROW_2_LOCATOR)
        self.insert_r2_switch.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        self.insert_r2_hoverbutton = SettingsTooltip(self.frame,
                                                     tooltip_text="When turned on, new matches will be inserted at the 2nd row of your\nspreadsheet instead of being appended to the bottom.")
        self.insert_r2_hoverbutton.grid(row=self.row, column=1, padx=40, pady=(10,0), sticky="w")
        self.insert_r2_hoverbutton.configure(state="disabled")

        increment_row()

        googlesheet_label = SettingsLabel(self, text="Google Sheets")
        googlesheet_label.grid(row=self.row, column=0, pady=(10,0), padx=10, sticky="w")

        googlesheet_switch = SettingsSwitch(self,
                                            googlesheet_label,
                                            c.WRITE_TO_GOOGLE_SHEETS_SETTING_LOCATOR)
        googlesheet_switch.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        increment_row()

        spreadsheet_name_label = SettingsLabel(self, text="Spreadsheet Name")
        spreadsheet_name_label.grid(row=self.row, column=0, pady=(10,0), padx=10, sticky="w")

        spreadsheet_name_entry = SettingsEntry(self, spreadsheet_name_label,
                                               c.GOOGLE_SHEETS_NAME_SETTING_LOCATOR,
                                               placeholder_text="Enter spreadsheet name (Google Sheets)")
        spreadsheet_name_entry.grid(row=self.row, column=1, columnspan=3, pady=(10,0), sticky="ew")

        googlesheet_switch.add_child_widget(spreadsheet_name_entry)

        increment_row()

        google_key_filetypes = [("JSON Files (*.json)", "*.json")]

        google_service_key_label = SettingsLabel(self, text="Google Service Acc. Key")
        google_service_key_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        google_service_key_entry = SettingsEntry(self,
                                                 google_service_key_label,
                                                 c.GOOGLE_SERVICE_ACCOUNT_KEY_JSON_PATH_LOCATOR,
                                                 validate=lambda v, lt: validate_path(v, lt, google_key_filetypes),
                                                 placeholder_text="Location of key (C:/...)")
        google_service_key_entry.grid(row=self.row, column=1, columnspan=4, pady=(10,0), sticky="ew")

        google_key_change = SettingsButton(self,
                                           text="Change  ",
                                           width=70,
                                           command=lambda: filedialog_to_entry(google_service_key_entry, google_key_filetypes),
                                           image=change_dir)
        google_key_change.grid(row=self.row, column=5, pady=(10,0), padx=5)

        googlesheet_switch.add_child_widget(google_service_key_entry)
        googlesheet_switch.add_child_widget(google_key_change)

        increment_row()

        excel_label = SettingsLabel(self, text="Excel")
        excel_label.grid(row=self.row, column=0, pady=(10,0), padx=10, sticky="w")
        excel_switch = SettingsSwitch(self, excel_label, c.WRITE_TO_EXCEL_FILE_SETTING_LOCATOR)
        excel_switch.grid(row=self.row, column=1, pady=(10,0), sticky="w")

        increment_row()

        excel_filetypes = [("Excel Workbook (*.xlsx)", "*.xlsx"),
                           ("Excel Macro-Enabled Workbook (*.xlsm)", "*.xlsm"),
                           ("Excel Template (*.xltx)", "*.xltx"),
                           ("Excel Macro-Enabled Template (*.xltm)", "*.xltm")]

        excel_file_path_label = SettingsLabel(self, text="Excel File Path")
        excel_file_path_label.grid(row=self.row, column=0, padx=10, pady=(10,0), sticky="w")

        excel_file_path_dir = SettingsEntry(self,
                                            excel_file_path_label,
                                            c.EXCEL_FILE_PATH_SETTING_LOCATOR,
                                            validate=lambda v, lt: validate_path(v, lt, excel_filetypes),
                                            placeholder_text="Location of excel spreadsheet (C:/...)")
        excel_file_path_dir.grid(row=self.row, column=1, columnspan=4, pady=(10,0), sticky="ew")

        excel_change = SettingsButton(self, text="Change  ",
                                      width=70,
                                      command=lambda: filedialog_to_entry(excel_file_path_dir, excel_filetypes),
                                      image=change_dir)
        excel_change.grid(row=self.row, column=5, pady=(10,0), padx=5)

        excel_switch.add_child_widget(excel_file_path_dir)
        excel_switch.add_child_widget(excel_change)

        increment_row()

        def create_excel_spreadsheet():
            """Creates a new Excel Spreadsheet"""
            path = filedialog.asksaveasfilename(initialfile="Valorant.xlsx", defaultextension=".xlsx", filetypes=excel_filetypes)

            if path:
                h.make_default_excel_file(path)

                input_entry(excel_file_path_dir, path)

        create_excel_button = SettingsButton(self,
                                             text="Create Excel Spreadsheet  ",
                                             image=pencil_image,
                                             command=create_excel_spreadsheet)
        create_excel_button.grid(row=self.row, column=1, padx=5, pady=10, sticky="w")

        excel_switch.add_child_widget(create_excel_button)

    def return_to_main(self) -> None:
        """Destroys the settings window and returns back to main"""
        self.destroy()
        self.parent.maximise()

    def open_spreadsheet_format(self) -> bool:
        """Opens the spreadsheet format window"""
        SpreadsheetFormat().mainloop()

    def save_settings(self) -> None:
        """Saves all new settings"""
        try:
            for widget in self.settings:
                if widget.cget("state") != "disabled":
                    widget.save()
        except InvalidSettingsError:
            return False
        else:
            messagebox.showinfo(title="Success", message="Settings have been saved.")
            return True

    def reset_settings(self) -> None:
        """Resets settings to default"""
        reset_confirmation = messagebox.askquestion(title="Confirmation",
                                                    message="Are you sure you would like to reset to default settings?\nAll current settings will be wiped.",
                                                    icon="warning")
        if reset_confirmation == "yes":
            make_default_settings_file(c.DEFAULT_SETTINGS)

            # Reloads the window
            SettingsWindow.destroy(self)
            SettingsWindow(self.parent).mainloop()

class SpreadsheetFormat(Toplevel):
    """Spreadsheet format window"""
    def __init__(self):
        super().__init__()
        self.geometry(c.SPREADSHEET_FORMAT_SETTINGS_WINDOW_RESOLUTION)
        self.title(c.SPREADSHEET_FORMAT_SETTINGS_TITLE)
        self.iconbitmap(get_resource_path(c.LOGO_IMAGE_PATH))

        self.frame = CTkScrollableFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.dropdown_menus_list = []
        self.format_columns_list = []

        self.row_count: int = -1

        self.spreadsheet_format_label = CTkLabel(self.frame, text="Spreadsheet Format\n(Columns)",
                                                 font=c.DEFAULT_FONT)
        self.spreadsheet_format_label.grid(row=0, column=0, padx=(10,20), pady=(10,0),
                                           sticky="w")
        self.spreadsheet_format_list = list(c.SPREADSHEET_FORMAT_OPTIONS.values())

        self.plus_button = CTkButton(self.frame, text="+", font=c.DEFAULT_FONT,
                                     command=self.add_boxes, width=20, corner_radius=20)
        self.plus_button.grid(row=0, column=3, padx=10, pady=(10,0), sticky="e")

        self.minus_button = CTkButton(self.frame, text="-", font=c.DEFAULT_FONT,
                                      command=self.subtract_boxes, width=20, corner_radius=20)
        self.minus_button.grid(row=0, column=4, padx=0, pady=(10,0), sticky="w")

        self.save_button = CTkButton(self.frame, text="Save and Close", font=c.DEFAULT_FONT,
                                     width=110, image=save_image, command=self.save_format_changes)
        self.save_button.grid(row=1, column=0, padx=10, pady=(20,0), sticky="w")
        spreadsheet_format = get_setting(*c.SPREADSHEET_FORMAT_LOCATOR)

        # If there is data in the spreadsheet format setting, add rows in window
        if spreadsheet_format:
            items = spreadsheet_format.split(",")
            for item in items:
                current_setting = c.SPREADSHEET_FORMAT_OPTIONS[item]

                self.add_boxes(current_setting) # Adds dropdown menus

    def add_boxes(self, value: str="-") -> None:
        count = len(self.dropdown_menus_list) + 1
        final_count = self.row_count + count
        index = count - 1

        count_number = CTkLabel(self.frame, text=f"{count}.", font=c.DEFAULT_FONT)
        count_number.grid(row=final_count, column=1, pady=(10,0),
                          padx=10, sticky="w")
        dropdown_menu = CTkOptionMenu(self.frame,
                                      values=self.spreadsheet_format_list,
                                      command=lambda new_value: self.edit_column(index, new_value),
                                      font=c.DEFAULT_FONT, button_color="grey",
                                      button_hover_color="dark grey",
                                      fg_color="white", text_color="black")
        dropdown_menu.configure(state="normal")
        dropdown_menu.set(value)
        self.edit_column(index, value)
        dropdown_menu.grid(row=final_count, column=2, pady=(10,0),
                           sticky="ew")
        self.dropdown_menus_list.append((count_number, dropdown_menu))

    def subtract_boxes(self) -> None:
        count = len(self.dropdown_menus_list) + 1

        if count > 1:
            last_dropdown_menu = self.dropdown_menus_list.pop()

            for element in last_dropdown_menu:
                element.grid_forget()
                element.destroy()

            self.format_columns_list.pop()

    def edit_column(self, index: int, value: str) -> None:
        formatted_value = get_key_from_value(c.SPREADSHEET_FORMAT_OPTIONS, value)

        try:
            self.format_columns_list[index] = formatted_value
        except IndexError:
            self.format_columns_list.append(formatted_value)

    def save_format_changes(self) -> None:
        format_settings_change = ",".join(self.format_columns_list)
        format_setting = get_setting(*c.SPREADSHEET_FORMAT_LOCATOR)

        if format_settings_change != format_setting:
            edit_setting(*c.SPREADSHEET_FORMAT_LOCATOR, format_settings_change)

        messagebox.showinfo(title="Success", message="Settings have been saved.")
        self.destroy()

def main():
    App().mainloop()

if __name__ == "__main__":
    main()
