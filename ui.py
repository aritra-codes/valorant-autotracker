from customtkinter import (set_appearance_mode, set_default_color_theme, 
                           CTk, CTkLabel, CTkEntry, CTkButton, CTkFrame, 
                           CTkImage, filedialog, END, CTkSwitch, StringVar, 
                           CTkSlider, CTkComboBox, CTkOptionMenu)
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

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x350")
        self.iconbitmap("logo.ico")
        self.title("Valorant Match Tracker")
        self.resizable(False,False)
                     
        self.frame = CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame.columnconfigure(0, weight=1)

        self.run = CTkButton(self.frame, text="Run", width=140, 
                             height=40, image=run_image,
                             font=default_font, command=self.run)
        self.run.grid(row=0, column=0, pady=(80,10))

        self.settings_button = CTkButton(self.frame, text="Settings", width=140, 
                                         height=40, image=settings_image,
                                         font=default_font, command=self.open_settings)
        self.settings_button.grid(row=1, column=0)

    def run(self):
        # Main function below (**remove comment when you want to test**)
        #main()
        print("Main function will be executed here!")

    def open_settings(self):
        settings_window = SettingsWindow()
        settings_window.mainloop()

class HoverButton(CTkButton):
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

    def on_leave(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class SettingsWindow(Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("800x660")
        self.title("Settings")
        self.iconbitmap("logo.ico")
        
        self.frame = CTkFrame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
          
        self.video_header = CTkLabel(self.frame, text="Video", 
                                     font=("Calibri Bold",18))
        self.video_header.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")

        self.switch_var = StringVar(value="off")
        self.switch_label = CTkLabel(self.frame, text="Auto-Upload Videos",
                                     font=default_font)
        self.switch_label.grid(row=1, column=0, pady=(10,0), padx=10, sticky="w")
        self.switch_onoff = CTkSwitch(self.frame, text="", command=self.switch1,
                                      variable=self.switch_var, onvalue="on",
                                      offvalue="off")
        self.switch_onoff.grid(row=1, column=1, pady=(10,0), sticky="w")

        self.firefox_profile_label = CTkLabel(self.frame, text="Firefox Profile Path",
                                              font=default_font)
        self.firefox_profile_label.grid(row=2, column=0, pady=(10,0), padx=10, sticky="w")
        self.firefox_entry = CTkEntry(self.frame, font=default_font, width=500,
                                     placeholder_text="Firefox profile path (C:/...)")
        self.firefox_entry.grid(row=2, column=1, pady=(10,0), columnspan=4)
        self.firefox_change = CTkButton(self.frame, text="Change  ", font=default_font,
                                       width=70, command=self.firefoxprofile_change_function,
                                       image=change_dir)
        self.firefox_change.grid(row=2, column=5, pady=(10,0), padx=5)

        self.visibility_label = CTkLabel(self.frame, text="Visibility",
                                         font=default_font)
        self.visibility_label.grid(row=3, column=0, padx=10, pady=(10,0),
                                   sticky="w")
        self.visibility_list = ["Private","Unlisted","Public"]

        self.visibility_dropdown = CTkOptionMenu(self.frame, values=self.visibility_list,
                                               command=self.visibility_function, 
                                               font=default_font, button_color="grey",
                                               button_hover_color="dark grey",
                                               fg_color="white", text_color="black")
        self.visibility_dropdown.grid(row=3, column=1, padx=2, pady=(10,0), sticky="w")

        self.switch_var2 = StringVar(value="off")
        self.switch_label_2 = CTkLabel(self.frame, text="Auto-Select Videos",
                                       font=default_font)
        self.switch_label_2.grid(row=4, column=0, pady=(10,0), padx=10, sticky="w")
        self.switch_onoff2 = CTkSwitch(self.frame, text="", command=self.switch2,
                                       variable=self.switch_var2, onvalue="on",
                                       offvalue="off")
        self.switch_onoff2.grid(row=4, column=1, pady=(10,0), sticky="w")

        self.viddir_label = CTkLabel(self.frame, text="Video Directory",
                                     font=default_font)
        self.viddir_label.grid(row=5, column=0, padx=10, pady=(10,0), sticky="w")
        self.viddir_entry = CTkEntry(self.frame, font=default_font, width=500,
                                     placeholder_text="Video directory (C:/...)")
        self.viddir_entry.grid(row=5, column=1, pady=(10,0), columnspan=4)
        self.viddir_change = CTkButton(self.frame, text="Change  ", font=default_font,
                                       width=70, command=self.viddir_change_function,
                                       image=change_dir)
        self.viddir_change.grid(row=5, column=5, pady=(10,0), padx=5)

        self.filename_format_label = CTkLabel(self.frame, text="Filename Format",
                                              font=default_font)
        self.filename_format_label.grid(row=6, column=0, padx=10, pady=(10,0), sticky="w")
        self.filename_format_entry = CTkEntry(self.frame, font=default_font, 
                                              placeholder_text="Enter filename format",
                                              width=200)
        self.filename_format_entry.grid(row=6, column=1, pady=(10,0), sticky="ew")
        self.filename_hover_button = HoverButton(self.frame, text="", image=question_image,
                                                 tooltip_text="Filename format should be...",
                                                 width=15, fg_color="transparent",
                                                 hover_color="grey")
        self.filename_hover_button.grid(row=6, column=2, pady=(10,0), sticky="w")

        self.recording_delay_label = CTkLabel(self.frame, text="Recording Delay",
                                              font=default_font)
        self.recording_delay_label.grid(row=7, column=0, padx=10, pady=(10,0),
                                        sticky="w")
        self.recording_delay_slider = CTkSlider(self.frame, from_=0, to=60,
                                                number_of_steps=60,
                                                command=self.slider)
        self.recording_delay_slider.grid(row=7, column=1, pady=(10,0), sticky="ew")
        self.recording_delay_slider.set(0)
        self.slider_value = CTkEntry(self.frame, font=default_font,
                                     width=5, justify="center")
        self.slider_value.insert(END, "0")
        self.slider_value.grid(row=7, column=2, pady=(10,0), padx=(10,10), sticky="ew")
        self.secs_label = CTkLabel(self.frame, text="secs",
                                   font=default_font)
        self.secs_label.grid(row=7, column=3, pady=(10,0), sticky="w")

        self.valorant_header = CTkLabel(self.frame, text="Valorant", 
                                     font=("Calibri Bold",18))
        self.valorant_header.grid(row=8, column=0, padx=10, pady=(15,0), sticky="w")

        self.username_label = CTkLabel(self.frame, text="Username",
                                       font=default_font)
        self.username_label.grid(row=9, column=0, padx=10, pady=(10,0), sticky="w")
        self.username_entry = CTkEntry(self.frame, font=default_font,
                                       placeholder_text="Enter username")
        self.username_entry.grid(row=9, column=1, pady=(10,0), sticky="ew")

        self.tag_label = CTkLabel(self.frame, text="Tag", font=default_font)
        self.tag_label.grid(row=10, column=0, padx=10, pady=(10,0), sticky="w")
        self.tag_entry = CTkEntry(self.frame, font=default_font,
                                  placeholder_text="Enter tag")
        self.tag_entry.grid(row=10, column=1, pady=(10,0), sticky="ew")

        self.puuid_label = CTkLabel(self.frame, text="PUUID", font=default_font)
        self.puuid_label.grid(row=11, column=0, padx=10, pady=(10,0), sticky="w")
        self.puuid_entry = CTkEntry(self.frame, font=default_font,
                                    placeholder_text="Enter/Find PUUID")
        self.puuid_entry.grid(row=11, column=1, pady=(10,0), sticky="ew",
                              columnspan=3)
        self.puuid_find = CTkButton(self.frame, text="Find PUUID", 
                                    font=default_font, image=find_image,
                                    command=self.find_puuid_function, width=110)
        self.puuid_find.grid(row=11, column=4, pady=(10,0), padx=5, sticky="w")

        self.region_label = CTkLabel(self.frame, text="Region", font=default_font)
        self.region_label.grid(row=12, column=0, padx=10, pady=(10,0), sticky="w")
        self.region_list = ["Europe (EU)", "North America (NA)", 
                            "Latin America (LATAM)", "Brazil (BR)", 
                            "Southeast Asia/Asia-Pacific (AP)", "Korea (KR)"]
        self.region_dropdown = CTkOptionMenu(self.frame, values=self.region_list,
                                               command=self.region_function, 
                                               font=default_font, button_color="grey",
                                               button_hover_color="dark grey",
                                               fg_color="white", text_color="black",
                                               width=250)
        self.region_dropdown.grid(row=12, column=1, pady=(10,0), sticky="w", columnspan=2)

        self.save_button = CTkButton(self.frame, text="Save", font=default_font,
                                     width=100, image=save_image)
        self.save_button.grid(row=13, column=0, padx=10, pady=(20,0), sticky="w")

        self.donation_button = CTkButton(self.frame, text="Why not consider donating?",
                                         font=default_font, image=donate_image,
                                         command=self.donate_function)
        self.donation_button.grid(row=13, column=1, pady=(20,0), sticky="w")
        
        self.check_info()

    def check_info(self):
        autoupload_video = h.get_setting(*c.AUTOUPLOAD_VIDEOS_SETTING_LOCATOR)
        firefox_profile_dir = h.get_setting(*c.FIREFOX_PROFILE_SETTING_LOCATOR)
        autoselect_video = h.get_setting(*c.AUTOSELECT_VIDEOS_SETTING_LOCATOR)
        video_directory = h.get_setting(*c.VIDEO_DIRECTORY_SETTING_LOCATOR)
        filename_format = h.get_setting(*c.FILENAME_FORMAT_SETTING_LOCATOR)
        recording_delay = h.get_setting(*c.RECORDING_START_DELAY_SETTING_LOCATOR)
        puuid_setting_locator = h.get_setting(*c.PUUID_SETTING_LOCATOR)
        region_setting = h.get_setting(*c.AFFINITY_SETTING_LOCATOR)

        if autoupload_video == "True":
            self.switch_var.set("on")
            self.switch1()
        else:
            self.switch_var.set("off")
            self.switch1()

        if firefox_profile_dir: 
            self.firefox_entry.delete(0,END)
            self.firefox_entry.insert(END, firefox_profile_dir)
        else:
            pass

        if autoselect_video == "True":
            self.switch_var2.set("on")
            self.switch2()
        else:
            self.switch_var2.set("off")
            self.switch2()

        if video_directory:
            self.viddir_entry.delete(0,END)
            self.viddir_entry.insert(END, video_directory)
        else:
            pass

        if filename_format:
            self.filename_format_entry.delete(0,END)
            self.filename_format_entry.insert(END, filename_format)
        else:
            pass

        if recording_delay:
            self.slider_value.delete(0,END)
            self.slider_value.insert(END, recording_delay)
            self.recording_delay_slider.set(int(recording_delay))
        else:
            pass

        if puuid_setting_locator:
            self.puuid_entry.delete(0,END)
            self.puuid_entry.insert(END,puuid_setting_locator)
        else:
            pass

        if region_setting:
            self.region_dropdown.set(c.REGION_OPTIONS[region_setting])
        else:
            pass
        
    def switch1(self):
        self.val = self.switch_onoff.get()
        if self.val == "off":
            self.firefox_entry.configure(state="disabled")
            self.firefox_change.configure(state="disabled")
            self.firefox_profile_label.configure(text_color = "grey")
            self.firefox_entry.configure(placeholder_text_color="#c9c9c9",
                                         text_color="grey")
            self.visibility_label.configure(text_color = "grey")
            self.visibility_dropdown.configure(state="disabled")
        elif self.val == "on":
            self.firefox_entry.configure(state="normal")
            self.firefox_change.configure(state="normal")
            self.firefox_profile_label.configure(text_color = "black")
            self.firefox_entry.configure(placeholder_text_color="grey",
                                         text_color="black")
            self.visibility_label.configure(text_color = "black")
            self.visibility_dropdown.configure(state="normal")

    def switch2(self):
        self.val2 = self.switch_onoff2.get()
        if self.val2 == "off":
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

        elif self.val2 == "on":
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

    def visibility_function(self, visibility):
        print(visibility)

    def viddir_change_function(self):
        self.file = filedialog.askdirectory(title="Open")
        self.viddir_entry.delete(0,END)
        self.viddir_entry.insert(END, self.file)
    
    def firefoxprofile_change_function(self):
        self.file2 = filedialog.askdirectory(title="Open")
        self.firefox_entry.delete(0, END)
        self.firefox_entry.insert(END, self.file2)

    def slider(self, value):
        intvalue = int(value)
        self.slider_value.delete(0, END)
        self.slider_value.insert(END, intvalue)
    
    def region_function(self, region):
        print(region)

    def find_puuid_function(self):
        name_entry = self.username_entry.get()
        tag_entry = self.tag_entry.get()
        if not name_entry:
            messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid username.")
        elif not tag_entry:
            messagebox.showerror(title="Invalid Input", 
                                 message=f"Please enter a valid tag.")
        self.puuid = h.find_puuid(name_entry, tag_entry)
        self.puuid_entry.delete(0, END)
        self.puuid_entry.insert(END, self.puuid)
    
    def donate_function(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()