import os
import json
import yt_dlp
import glob

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

def fetch_metadata(video_ids, output_file="data/metadata.json"):
    """Fetch upload date and title for all videos."""
    os.makedirs("data", exist_ok=True)
    
    metadata = {}
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            metadata = json.load(f)

    missing_ids = [vid for vid in video_ids if vid not in metadata]
    
    if not missing_ids:
        print("Metadata already up to date.")
        return metadata

    print(f"Fetching metadata for {len(missing_ids)} videos...")
    
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for vid in missing_ids:
            try:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
                metadata[vid] = {
                    "title": info.get("title"),
                    "upload_date": info.get("upload_date"), # YYYYMMDD
                    "channel": info.get("channel"),
                    "duration": info.get("duration")
                }
                print(f"Fetched metadata for {vid}")
            except Exception as e:
                print(f"Error for {vid}: {e}")

    with open(output_file, 'w') as f:
        json.dump(metadata, f, indent=4)
    
    return metadata

if __name__ == "__main__":
    fetch_metadata(VIDEO_IDS)
