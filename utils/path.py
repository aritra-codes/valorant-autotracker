import os
import sys

def list_all_files(path: str=".") -> list[str]:
    files = []

    for entry in os.listdir(path):
        if os.path.isdir(entry_path := os.path.join(path, entry)):
            files += list_all_files(entry_path)
        else:
            files.append(entry)

    return files

def get_resource_path(relative_path: str="") -> str:
    """Gets absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_project_directory() -> str:
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, os.pardir)
    except Exception:
        return os.path.abspath(".")