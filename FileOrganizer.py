# File Organizer - Python Project
# Run with: python FileOrganizer.py
# Test first on a sample folder. Files are moved, not copied.

from pathlib import Path
import shutil

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi", ".webm"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".java", ".c", ".cpp", ".js", ".html", ".css"}
}

def category_for(file_path):
    extension = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"

def unique_destination(path):
    if not path.exists():
        return path
    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1

def organize_directory(folder):
    if not folder.exists() or not folder.is_dir():
        print("The directory does not exist or is not a folder.")
        return

    moved = 0
    for item in list(folder.iterdir()):
        if not item.is_file() or item.name == Path(__file__).name:
            continue
        category = category_for(item)
        target_folder = folder / category
        target_folder.mkdir(exist_ok=True)
        destination = unique_destination(target_folder / item.name)
        try:
            shutil.move(str(item), str(destination))
            print(f"Moved: {item.name} -> {category}/{destination.name}")
            moved += 1
        except OSError as error:
            print(f"Could not move {item.name}: {error}")
    print(f"Organization complete. Files moved: {moved}")

def main():
    raw_path = input("Enter the folder path to organize: ").strip().strip('"')
    if not raw_path:
        print("No directory entered.")
        return
    organize_directory(Path(raw_path).expanduser())

if __name__ == "__main__":
    main()
