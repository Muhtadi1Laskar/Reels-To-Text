import yt_dlp
from urllib.parse import urlparse
from pathlib import Path
import argparse

from utils import generate_file_path, parse_file_name, flatten_video_directory


def download_reel(url, output_folder, file_name="sample"):
    ydl_opts = {
        "outtmpl": str(output_folder / file_name),
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
    }
    

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



def main():
    file_name, url = parse_file_name()
    output_folder_path = Path("video")

    download_folder_path = generate_file_path("video", output_folder_path)

    print("\n\n" + str(download_folder_path) + "\n\n")

    download_reel(url, download_folder_path, file_name)

    print("\n ---- Organizing the files ---- ")

    flatten_video_directory()

main()
