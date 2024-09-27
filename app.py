from utils.settings import get_setting
import valorant_autotracker.constants as c
from valorant_autotracker.gui import main as gui
from valorant_autotracker.main import main as script

def main():
    if get_setting(*c.USE_GUI_SETTING_LOCATOR, boolean=True):
        gui()
    else:
        script()

if __name__ == "__main__":
    main()
