import argparse
from src.extract import process_channel_transcripts
from src.classify import load_data, classify_transcripts

def main():
    parser = argparse.ArgumentParser(description="YouTube Transcript Extraction and Classification")
    parser.add_argument("--channel", type=str, help="YouTube Channel ID or URL to extract transcripts from")
    
    args = parser.parse_args()

    if args.channel:
        print(f"Starting extraction for channel: {args.channel}")
        process_channel_transcripts(args.channel)
    else:
        print("Please provide a --channel argument to start extraction.")

if __name__ == "__main__":
    main()
