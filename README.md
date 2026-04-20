# Transcribe - Russian Audio Transcription Tool

A Python-based audio transcription tool that converts Russian language audio files to text using the Vosk speech recognition engine and optional recasing/punctuation correction.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- FFmpeg (for audio format conversion)

#### Installing FFmpeg

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**On macOS (with Homebrew):**
```bash
brew install ffmpeg
```

**On Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use:
```bash
choco install ffmpeg
```

### Step 1: Install Python Dependencies

1. Navigate to the project directory:
```bash
cd /data/Dev/transcribe
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install required Python packages:
```bash
pip install -r requirements.txt
```

### Step 2: Download and Install Models

This project uses Vosk for Russian language processing:

#### Vosk Russian Speech Recognition Model

The Vosk model (`vosk-model-ru-0.42`) is included in this repository. If you need to manually download or update it:

1. Download from the Vosk model repository:
   - Link: [Vosk Models - Russian](https://alphacephei.com/vosk/models)
   - Download: `vosk-model-ru-0.42.zip`

2. Extract to the project directory:
```bash
unzip vosk-model-ru-0.42.zip
```

The model directory structure should look like:
```
vosk-model-ru-0.42/
├── am/              # Acoustic model
├── conf/            # Configuration files
├── graph/           # Language model and pronunciation
├── ivector/         # iVector extractor
└── rnnlm/          # Neural network language model
```

### Step 3: Verify Installation

Verify that all models are properly installed by checking:

```bash
ls -la vosk-model-ru-0.42/
```

## Usage

### Basic Transcription

```python
from vosk import Model
from transcribe import transcribe_file

# Initialize the model
model = Model("vosk-model-ru-0.42")

# Transcribe an audio file
result = transcribe_file(
    audio_path="path/to/audio.mp3",
    output_folder="output",
    model=model,
    overwrite=False
)

print(result)
```

### Supported Audio Formats

The tool supports any audio format that FFmpeg can handle:
- MP3
- WAV
- FLAC
- OGG
- M4A
- And many others

## Project Structure

```
transcribe/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── transcribe.py                      # Main transcription script
├── transcribe.ipynb                   # Jupyter notebook for interactive use
├── vosk-model-ru-0.42/               # Russian speech recognition model
└── vosk-recasepunc-ru-0.22/          # Russian recasing and punctuation model
```

## Dependencies

Key dependencies:
- **vosk** (0.3.45): Speech recognition engine
- **ffmpeg-python**: Audio format conversion
- **wave**: Audio file processing
- **srt**: Subtitle file handling

See `requirements.txt` for complete list of dependencies.

## Troubleshooting

### "ModuleNotFoundError: No module named 'vosk'"

Ensure you've activated the virtual environment and installed requirements:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### "ffmpeg not found"

Ensure FFmpeg is installed and accessible in your PATH:
```bash
ffmpeg -version
```

### Model not found errors

Verify that the model directories exist in the project root:
```bash
ls vosk-model-ru-0.42/
```

If missing, re-download and extract them as described in Step 2.

## Notes

- The speech recognition model is specifically trained for Russian language (ru-RU)
- Audio files are converted to 16kHz mono WAV format for optimal recognition
- Large audio files may take several minutes to process
- The tool saves transcription results as `.txt` files in the specified output folder
