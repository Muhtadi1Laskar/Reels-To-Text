from utils import parse_file_name
import subprocess
import sys

def main():
    target_name, url = parse_file_name(description="Pipeline to transcribe reels and extract entities.")

    try:
        print(f"--- Step 1/3: Downloading the video '{url}' ---")
        result_bideo = subprocess.run(
            [sys.executable, "-u", "download_reels.py", target_name, url],
            check=True
        )

        print(f"--- Step 2/3: Starting transcription for '{target_name}' ---")
        result_transcribe = subprocess.run(
            [sys.executable, "-u", "transcribe.py", target_name, url],
            check=True
        )

        print(f"\n--- Step 3/3: Extracting entities for '{target_name}' ---")
        result_extract = subprocess.run(
            [sys.executable, "-u", "ollma_extract_entities.py", target_name, url],
            check=True
        )

        print(f"\nPipeline completed successfully for '{target_name}'!")

    except subprocess.CalledProcessError as e:
        print(f"\nPipeline failed during execution. Exit code: {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)


if __name__ == "__main__":
    main()