from utils.settings import get_setting
from valorant_autotracker.gui import main as gui
from valorant_autotracker.main import main as script

def main():
    if get_setting("GENERAL", "use_gui", boolean=True):
        gui()
    else:
        script()

if __name__ == "__main__":
    main()