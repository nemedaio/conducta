import os
import argparse
import glob
import time
from youtube_transcript_api import YouTubeTranscriptApi

VIDEO_IDS = [
    'HB0tzzEyqAM', '84J6RomVy54', 'qYJqSr7A5kc', 'ca4Bmu-XV2s', 'rSKBY-l_O2M', 
    'nVEFgICNztk', '3wXCNg6GmMk', 'ae6XDGByV5c', 'nj6TNdf18xM', 'Z1mkMgRS2os', 
    'MR6GYCuxRJQ', 'JT3X7RsLLTw', 'zSs8kqyIBK8', 'CV1B6CDClRU', 'O7PcRPci5UE', 
    'alK4Mnh5DjI', 'q6LZmp-zXG0', 'M7afAW5CihI', 'CPBtm9b_ZJ8', 'bXxU1iKQn5M', 
    'O1q47Q2KnoQ', '92VjHF3Dj4s', 'KljgLblLsA8', 'GDeR21s3OLE', 'oe92W8s3qLY', 
    'VJqhEViuk7c', 'm0KftBK0tfg', '-s85_A8-3s8', 'rbIyJvJ7PWs', 'VBo069U1jKU', 
    'o6Gk_EfCB1g', 'E5H9qw2OWUE', 'gCXi77GQUb4', 'ZLOEbvWwwKE', 'QuPZYZztxNA', 
    'i8ksBggpJR0', '4ijsFI0wYWQ', 'JMg24UiMq2g', '7_UFLPSRqjQ', 'nTIAaZ5P4e8', 
    'IR2rjECjwzQ', 'wfNE_04jA2U', 'jPyDyi9_uTk', 'Dvsfci4_0UY', 'Z3tcqLxGmas', 
    'LyVQHev2H4M', '-105UXcvVwA', 'vW4xM0H93gM', 'ujnZS5zGQ4E', 'q6G4vDxDpCQ', 
    '9u7x4Ify4Ys', 'K9nBs9ID6tU', 'fYQC8mLDxbg', 'eEll0ywICQU', 'Q0pvpfI78g4', 
    'PRtA5CdYdN4', 'RtnsJCYnIho', 'Ok8mk0uyfSw', 'fyGgo-q8RuY', 'eso9hXBTaDA', 
    'BGHZpQfhpcA', '7AlLpZnVJpk', 'ynfb_H79YDo', '6cBXeddaJbM', 'bejscUSJecU', 
    'E521YaR4OL0', 'yB2e23xHdoI', '7Aosu8T278E', 'HglaNVyfOGA', 't-ekRv43XGE', 
    'hBOlS00S5zU', 'BMt7arnEa1M', 'UO0fV2ZNh1g', 'FPb6mgBzMFU', 'MGfOpiwbJ1c', 
    'HY4whjpikZA', 't5LwBUyHdOE', 'EyhNQ5Fg8G4', 'WmcC9y2G7ig', 'hYH0DqiXk6w', 
    'UgIcwTfuAcY', 'vD2jWjGWdR0', 'cxU1jiTk8A0', 'o5D9Xid_fE0', 'cXlm0NdiIGk', 
    'eSEnT1b-0XM', '-M8SUHRILig', 'Dwg_XcaO400', 'NR6DHfhj7Sw', 'PC8h_ciuW2s', 
    '7EPVMllxyJA', 'GLu95BlbKCk', 'Z-nx_3y8_ks', 'Q5oFdPYzY64', 'T3n4Eh0AZAM', 
    'vPzNOC5Yfpk', 'UsmYXw9Bniw', 'cDIUQUNG04M', 'yxGXPqb5WqI', 'Sr8H14oLA9A', 
    'ssm2cw16EiI', 'z4i-fo5w6CU', 'McSYjLtO7f0', 'e7_v9WRrohU', '2daPKbClqYc', 
    'TkNI3BLAvYI', 'R_5W1Sm6WaA', '3UTLo_81Xbo', 'uKwiq0W-IIk', '6GAMN0GYT7w', 
    '3aNvKkxPtvk', 'Jq1TpO_MIcU', 'AV_85dV4-S8', 'SKreUbUe4uc', '0uFMgTpbSGs', 
    'G7mJxEyOVNc', 'ZCWj_MuH-ds', '1dMbmDZxZNA', 'Z8e7DRBFNk0', 'T9zTQDzee94', 
    'HlwvmhugMfY', 'pEfEpR6f2LE', 'fUbGv-UFSf4', '0850zU08LZc', 'efR-AH5OlC4', 
    'oHu8fEF1aTU', 'fD63FEMX82s', 'hsFrC9IY6Es', 'W8f7qcilhUU', 'CJpNmTTGY9o', 
    'KCqjW1NyhRQ', 'beC24CFysaw', 'wOaIohPADLU', 'ItA4nr-KhIw', 'C3epNuZ0GeE', 
    'z12Cv6P12sU', '0dpYoX1wT9o', 'Q5CibVhIPg8', 'D06HPB6zDN8', 'qhTwBHNoaoU', 
    '5EOnCNci60s', 'I1mgcwOFeG0', '_4VbxOGWzto', 'zyVlcGx8en8', 'xBzCefH3ZJc', 
    'B3BSBvl31Gc', '7GPXSngrd9s', 'jfEziQendAE', '4Xg4mi-pBfE', 'vaL5HSO7bp4', 
    'M7wy-hnWFq4', 'qddooE1IwdQ', 'uhJGXiyDBgk', 'HkMh-ur8y_s', 'GsIJQm3FGMU', 
    'YCZPzF9FphI', 'pBUIGI2TSIA', 'krB4vAPaG0M', 'jgCW3fN4wnI', '0KsmReqOVMM', 
    'WWheJzxx-qk', 'CCit6v2MQXE', 'X2N7TeciZRE', 'G0SkWx82gwc', 'qrrI98xrL3Y', 
    'v5BdGSB9PEo', '5M1ZwvLI7JU', 'KZHoJ1lD_GQ', 'yTvYgsjxiEA', 'lzXiqumJY0M', 
    '_iR-gbTVcvw', 'yGFbO_Jb4Uk'
]

def extract_transcript(video_id, languages=['es', 'es-MX', 'es-419']):
    """Extract transcript for a specific video ID."""
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=languages)
        return transcript
    except Exception as e:
        print(f"Error fetching {video_id}: {e}")
        return None

def process_video_list(video_ids, output_dir="obsidian_vault/transcripts"):
    """Fetch transcripts for a list of video IDs and save to output directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Identify existing files to skip
    existing_files = glob.glob(os.path.join(output_dir, "*.md"))
    existing_ids = set([os.path.basename(f).replace(".md", "") for f in existing_files])
    
    missing_ids = [vid for vid in video_ids if vid not in existing_ids]
    
    if not missing_ids:
        print("All transcripts already downloaded!")
        return

    print(f"Starting extraction for {len(missing_ids)} missing videos...")
    
    for i, video_id in enumerate(missing_ids):
        # Progress indication
        print(f"[{i+1}/{len(missing_ids)}] Fetching {video_id}...")
        
        transcript = extract_transcript(video_id)
        if transcript:
            md_content = f"# Transcript for Video ID: {video_id}\n\n"
            for snippet in transcript:
                time_val = snippet.start
                text = snippet.text
                md_content += f"[{time_val:.2f}s] {text}\n\n"
            
            file_path = os.path.join(output_dir, f"{video_id}.md")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"Successfully saved {video_id}")
        
        # Take a larger break to avoid blocking
        time.sleep(5) 

if __name__ == "__main__":
    process_video_list(VIDEO_IDS)
