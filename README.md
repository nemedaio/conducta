# YouTube Transcript Extractor & Classifier

A Python project to extract all transcripts from a given YouTube channel and run classification scripts on them.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Provide the channel identifier to start the extraction process:
```bash
python main.py --channel "CHANNEL_ID"
```

## Project Structure
- `src/extract.py`: Handles downloading and saving transcripts from YouTube.
- `src/classify.py`: Handles classifying the extracted transcripts.
- `data/`: Storage for downloaded raw and processed data.
