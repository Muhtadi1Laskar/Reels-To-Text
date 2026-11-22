from pathlib import Path
from faster_whisper import WhisperModel

from utils import generate_file_path, parse_file_name


def main():
    file_name, url = parse_file_name("Offline video/audio transcription using Whisper")
    file_path_check = generate_file_path("output-text", f"{file_name}.txt")
    
    if Path(file_path_check).exists():
        print("The transcription already exists. Moving to the next step\n")

        return None
    
    video_file_name = f"{file_name}.mp4"

    video_file_path = generate_file_path("video", video_file_name)
        

    model = "large-v3-turbo" 
    print(f"Loading model: {model}")

    model = WhisperModel(
        model,
        device="cpu",
        compute_type="int8",
        cpu_threads=8,
        num_workers=1
    )

    print(f"Transcribing: {video_file_name}")

    segments, info = model.transcribe(
        str(video_file_path),
        language="en",
        beam_size=5,
        vad_filter=True
    )

    segments = list(segments)

    if not segments:
        print("No speed detected")

    transcript = "\n".join(
        f"{segment.text.strip()}"
        for segment in segments
    )

    output_path = generate_file_path("output-text", f"{file_name}.txt")

    output_path.write_text(
        transcript,
        encoding="utf-8"
    )

    print(f"\nDetected Language: {info.language}")
    print(f"Language probability: {info.language_probability}")
    print(f"Transcript saved to: {output_path}")

    # print("\n--- TRANSCRIPT ---\n")
    # print(transcript)


if __name__ == "__main__":
    main()