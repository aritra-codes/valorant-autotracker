from tkinter import Toplevel, Label, messagebox
from typing import Callable


from customtkinter import (CTkLabel, CTkEntry, CTkButton,
                           END, CTkSwitch, CTkSlider,
                           CTkOptionMenu, IntVar)

from utils.misc import get_key_from_value, get_ctk_image
from utils.settings import get_setting, edit_setting, InvalidSettingsError
import valorant_autotracker.constants as c

question_image = get_ctk_image(c.QUESTION_IMAGE_PATH["dark"], c.QUESTION_IMAGE_PATH["light"])

class SettingsTooltip(CTkButton):
    """Class for hover button (question mark)"""
    def __init__(self, master, tooltip_text, **kw):
        super().__init__(master, text="",
                         width=15, fg_color="transparent",
                         image=question_image,
                         hover_color="grey", **kw)
        self.tooltip = None
        self.tooltip_text = tooltip_text
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, _):
        """Creates tooltip"""
        self.tooltip = Toplevel(self)
        x, y, _, _ = self.bbox("insert")
        x += self.winfo_rootx() + 25
        y += self.winfo_rooty() + 25
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = Label(self.tooltip, text=self.tooltip_text,
                      bg="white", relief="solid",
                      borderwidth=0.5)
        label.pack()

    def on_leave(self, _):
        """Destroys tooltip"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class SettingsSwitch(CTkSwitch):
    def __init__(self, window, label: CTkLabel, setting_locator, *args, **kwargs) -> None:
        self.variable = IntVar()
        super().__init__(window.frame, *args,
                         variable=self.variable,
                         command=self.toggle_child_widgets,
                         text="",
                         **kwargs)

        self.label = label
        self.setting_locator = setting_locator
        self.child_widgets = []
        self.insert_value()

        window.settings.append(self)

    def insert_value(self) -> None:
        self.value = get_setting(*self.setting_locator, boolean=True)
        self.variable.set(self.value)

    def save(self) -> None:
        current_value = self.variable.get()

        if self.value != current_value:
            self.value = current_value
            edit_setting(*self.setting_locator, current_value)

    def enable(self) -> None:
        self.label.configure(text_color="black")
        self.configure(state="normal")

        self.toggle_child_widgets()

    def disable(self) -> None:
        self.label.configure(text_color="grey")
        self.configure(state="disabled")

        self.toggle_child_widgets(False)

    def add_child_widget(self, widget) -> None:
        self.child_widgets.append(widget)
        self.toggle_child_widgets()

    def toggle_child_widgets(self, enable: bool=None) -> None:
        if enable is None:
            enable = self.variable.get()

        if enable:
            for widget in self.child_widgets:
                widget.enable()
        else:
            for widget in self.child_widgets:
                widget.disable()

class SettingsEntry(CTkEntry):
    def __init__(self, window, label: CTkLabel, setting_locator=None,
                 required: bool=True,
                 validate: Callable[[str, str], bool]=None,
                 *args, **kwargs) -> None:
        super().__init__(window.frame, *args, font=c.DEFAULT_FONT, **kwargs)

        self.label = label
        self.setting_locator = setting_locator
        self.required = required
        self.validate = validate
        self.insert_value()

        window.settings.append(self)

    def insert_value(self) -> None:
        if not self.setting_locator:
            return

        self.value = get_setting(*self.setting_locator)
        self.delete(0, END)
        self.insert(END, self.value)

    def save(self) -> None:
        if not self.setting_locator:
            return
        
        current_value = self.get()

        if self.required and not current_value:
            messagebox.showerror(title="Empty Input",
                                message=f"{self.label._text}: Please enter a value.")
            raise InvalidSettingsError
        
        if self.validate and not self.validate(current_value, self.label._text):
            raise InvalidSettingsError

        if self.value != current_value:
            self.value = current_value
            edit_setting(*self.setting_locator, current_value)

    def enable(self) -> None:
        self.label.configure(text_color="black")
        self.configure(state="normal", placeholder_text_color="grey", text_color="black")

    def disable(self) -> None:
        self.label.configure(text_color="grey")
        self.configure(state="disabled", placeholder_text_color="#c9c9c9", text_color="grey")

class SettingsOptionMenu(CTkOptionMenu):
    def __init__(self, window, label: CTkLabel, setting_locator, options: dict, *args, **kwargs) -> None:
        super().__init__(window.frame, *args,
                         values=list(options.values()),
                         button_color="grey", button_hover_color="dark grey",
                         fg_color="white", text_color="black",
                         font=c.DEFAULT_FONT, **kwargs)

        self.label = label
        self.options = options
        self.setting_locator = setting_locator
        self.insert_value()

        window.settings.append(self)

    def insert_value(self) -> None:
        self.value = self.options[get_setting(*self.setting_locator)]
        self.set(self.value)

    def save(self) -> None:
        current_value = self.get()

        if self.value != current_value:
            self.value = current_value
            edit_setting(*self.setting_locator, get_key_from_value(self.options, current_value))

    def enable(self) -> None:
        self.label.configure(text_color="black")
        self.configure(state="normal")

    def disable(self) -> None:
        self.label.configure(text_color="grey")
        self.configure(state="disabled")

class SettingsSlider(CTkSlider):
    def __init__(self, window, label: CTkLabel, setting_locator=None, *args, **kwargs) -> None:
        super().__init__(window.frame, *args, **kwargs)

        self.label = label
        self.setting_locator = setting_locator
        self.insert_value()

        window.settings.append(self)

    def insert_value(self) -> None:
        if not self.setting_locator:
            return

        self.value = get_setting(*self.setting_locator, floatp=True)
        self.set(self.value)

    def save(self) -> None:
        if not self.setting_locator:
            return

        current_value = self.get()

        if self.value != current_value:
            self.value = current_value
            edit_setting(*self.setting_locator, current_value)

    def enable(self) -> None:
        self.label.configure(text_color="black")
        self.configure(state="normal")

    def disable(self) -> None:
        self.label.configure(text_color="grey")
        self.configure(state="disabled")

class SettingsButton(CTkButton):
    def __init__(self, window, *args, **kwargs) -> None:
        super().__init__(window.frame, *args, font=c.DEFAULT_FONT, **kwargs)

    def enable(self) -> None:
        self.configure(state="normal")

    def disable(self) -> None:
        self.configure(state="disabled")

class SettingsHeader(CTkLabel):
    def __init__(self, window, *args, **kwargs) -> None:
        super().__init__(window.frame, *args, font=("Calibri Bold",18), **kwargs)

class SettingsLabel(CTkLabel):
    def __init__(self, window, *args, **kwargs) -> None:
        super().__init__(window.frame, *args, font=c.DEFAULT_FONT, **kwargs)