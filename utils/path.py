import os

def list_all_files(path: str=".") -> list[str]:
    files = []

    for entry in os.listdir(path):
        if os.path.isdir(entry_path := os.path.join(path, entry)):
            files += list_all_files(entry_path)
        else:
            files.append(entry)

    return files