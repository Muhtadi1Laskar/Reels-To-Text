# Reel to Text

**Turn book and movie recommendations hidden in Instagram Reels into searchable, storable text.**

Reel to Text is a lightweight, locally running Python pipeline that downloads Instagram Reels, transcribes their audio, and extracts recommended books, comics, and movies using local machine learning models.

The goal is simple: instead of saving dozens of Reels just to remember a book or movie recommendation, turn their contents into structured data that can be stored, searched, and revisited later.

## Features

- **Instagram Reel downloading** — Download Reels locally for processing.
- **Speech-to-text transcription** — Transcribe audio using Faster-Whisper.
- **Named entity extraction** — Identify books, movies, comics, and other named works using GLiNER and Qwen.
- **Structured output** — Save extracted recommendations as JSON.
- **Local inference** — Run machine learning models locally instead of relying on paid cloud APIs.
- **CPU-friendly design** — Uses lightweight models and quantized inference to avoid requiring a dedicated NVIDIA GPU.

## How It Works

The project follows a three-stage pipeline:

```text
Instagram Reel URL
        |
        v
  Download Reel
        |
        v
  Extract Audio
        |
        v
  Faster-Whisper
  Speech Transcription
        |
        v
  GLiNER / Qwen
  Entity Extraction
        |
        v
  Structured JSON
```

### 1. Download

The pipeline downloads the Instagram Reel and saves it locally as an MP4 file.

### 2. Transcription — Faster-Whisper

[Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) converts the Reel's speech into text.

It uses CTranslate2 for optimized inference and supports quantized computation, making it practical to run Whisper on a CPU without a dedicated GPU.

### 3. Entity Extraction — GLiNER and Ollama

The transcribed text is processed to identify relevant named entities and recommendations.

- **[GLiNER](https://github.com/urchade/GLiNER)** — A lightweight, zero-shot named entity recognition model for identifying relevant entities in text.
- **[Ollama](https://ollama.com/)** — Runs the local Qwen model to extract explicitly mentioned work titles and produce structured JSON.

The extraction process is designed to avoid treating ordinary sentences, plot descriptions, or character names as actual book or movie titles.

### 4. Save Results

The extracted recommendations are saved as JSON files, making them easy to reuse in other applications or import into a database later.

Example:

```json
{
    "items": [
        {
            "title": "Gideon Falls",
            "creator": null,
            "recommendation": false
        },
        {
            "title": "Something Is Killing the Children",
            "creator": null,
            "recommendation": false
        }
    ]
}
```

## Requirements

- Python 3.10 or newer (Python 3.13 may require checking compatibility of individual dependencies).
- [Ollama](https://ollama.com/) installed and running.
- An internet connection for downloading Reels and obtaining models initially.
- Sufficient RAM for local model inference.

A dedicated GPU is not required. CPU inference is supported, although processing time depends on your hardware and the selected models.

## Installation

Using a virtual environment is recommended to keep project dependencies isolated.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Reel-To-Text.git
cd Reel-To-Text
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows (PowerShell)**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**

```cmd
venv\Scripts\activate.bat
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Ollama

Install Ollama from [ollama.com](https://ollama.com/).

Pull the Qwen model:

```bash
ollama pull qwen2.5:1.5b
```

Make sure Ollama is running before starting the extraction pipeline.

The required ML models are downloaded the first time they are loaded. Once downloaded and cached, model inference can run locally without repeatedly downloading them.

## Usage

The main entry point is `reels_to_text.py`.

Run the pipeline with a target filename and an Instagram Reel URL:

```bash
python reels_to_text.py "book-rec" "https://www.instagram.com/reel/REEL_ID/"
```

The pipeline executes the following steps automatically:

1. Downloads the Reel.
2. Transcribes its audio.
3. Extracts book and movie recommendations.

### Output

The downloaded video and generated text are stored separately.

```text
Reel-To-Text/
│
├── video/
│   └── book-rec.mp4
│
├── output-text/
│   └── book-rec.txt
│
└── output-results/
    └── book-rec.json
```

The JSON output contains the extracted recommendations and can be used as the input for future features such as search, categorization, or database storage.

## Design Goals

This project was built around a few practical considerations:

- **Local-first:** Keep transcription and language-model inference on the local machine.
- **Lightweight:** Prefer smaller models that can run on ordinary consumer hardware.
- **No dedicated GPU requirement:** Avoid architectures that depend on expensive GPU hardware.
- **Structured information:** Convert unstructured speech into reusable JSON data.
- **Modular pipeline:** Keep downloading, transcription, and extraction as separate stages.

## Limitations

- Transcription accuracy depends on audio quality, accents, background music, and speech clarity.
- Proper names and unfamiliar book or movie titles may be transcribed incorrectly.
- Small language models can occasionally miss recommendations or extract incorrect titles.
- Processing time depends on CPU performance and Reel duration.
- Instagram may change its access restrictions or download behavior, potentially affecting the downloading stage.
- The extraction pipeline cannot reliably identify a title that was never explicitly mentioned in the audio.

## Future Improvements

- Extract authors, directors, and creators.
- Identify whether a title is a book, comic, movie, or TV show.
- Capture the surrounding recommendation context.
- Improve extraction accuracy through transcript chunking and contextual classification.
- Store results in a searchable local database.
- Add duplicate detection across multiple Reels.

## License
