from pathlib import Path
import shutil
import argparse


def parse_file_name(description=""):
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("file_name", help="Name of the input text file")
    parser.add_argument("url", help="URL of the instagram reel")

    args = parser.parse_args()

    return [args.file_name, args.url]


def generate_file_path(folder, file_name):
    script_dir = Path(__file__).resolve().parent
    output_folder = script_dir / folder

    output_folder.mkdir(parents=True, exist_ok=True)

    output_path = output_folder / file_name

    return output_path


def flatten_video_directory():
    # Get the parent 'video' folder relative to this script
    script_dir = Path(__file__).resolve().parent
    parent_path = script_dir / "video"

    print(f"Target Parent Directory: {parent_path}")

    if not parent_path.exists():
        print("Error: The 'video' folder does not exist.")
        return

    # Find all .mp4 files that are nested inside subfolders (not sitting directly in 'video')
    nested_mp4s = [f for f in parent_path.rglob("*.mp4") if f.parent != parent_path]

    if not nested_mp4s:
        print("No nested .mp4 files found to move.")
        return

    for mp4_file in nested_mp4s:
        target_path = parent_path / mp4_file.name

        # Handle file name collisions if multiple folders have 'mp4.mp4'
        if target_path.exists():
            base = mp4_file.stem
            suffix = mp4_file.suffix
            counter = 1
            while target_path.exists():
                target_path = parent_path / f"{base}_{counter}{suffix}"
                counter += 1

        # Move the file to the main parent folder
        shutil.move(str(mp4_file), str(target_path))
        print(f"Moved: {mp4_file.name} -> Main video folder")

    # Clean up and delete any empty subfolders left behind (deepest first)
    sub_dirs = sorted(
        [d for d in parent_path.rglob("*") if d.is_dir()],
        key=lambda p: len(p.parts),
        reverse=True,
    )

    for dir_path in sub_dirs:
        try:
            if not any(dir_path.iterdir()):
                dir_path.rmdir()
                print(f"Deleted empty folder: {dir_path.name}")
        except Exception as e:
            print(f"Could not delete folder {dir_path.name}: {e}")

    print("\nDone! All files are now flattened into the main video folder.")

    print("\nFlattening complete!\n")
