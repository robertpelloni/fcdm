import os
import sys
import argparse
import glob

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from stream_sanitizer import sanitize_ssc
from ddc_inference import generate_ddc_notes

def ingest_songs(songs_dir, difficulty=3, force=False):
    """
    Automated Music Ingestion Pipeline (v2.1.0)
    """
    print(f"Ingesting songs from: {songs_dir} (Diff: {difficulty}, Force: {force})")

    extensions = ['*.mp3', '*.ogg', '*.wav']
    for ext in extensions:
        for audio_path in glob.glob(os.path.join(songs_dir, "**", ext), recursive=True):
            dir_name = os.path.dirname(audio_path)
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            ssc_path = os.path.join(dir_name, f"{base_name}.ssc")

            if not force and os.path.exists(ssc_path):
                with open(ssc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    if "(Fitness)" in f.read():
                        print(f"  Skipping {ssc_path} (Already Sanitized)")
                        continue

            print(f"  Processing {audio_path}...")
            create_skeleton_ssc(audio_path, ssc_path, difficulty)
            sanitize_ssc(ssc_path, ssc_path, audio_path)

def create_skeleton_ssc(audio_path, ssc_path, difficulty):
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    notes_data = generate_ddc_notes(audio_path, difficulty=difficulty)

    content = f"""#VERSION:0.81;
#TITLE:{base_name};
#ARTIST:FCDM-AI;
#MUSIC:{os.path.basename(audio_path)};
#OFFSET:0.000;
#BPMS:0.000=120.000;
#NOTES:
#STEPSTYPE:dance-single;
#DIFFICULTY:Medium;
#METER:{difficulty};
#CREDIT:FCDM-v2.1.0;
{notes_data}
;
"""
    with open(ssc_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", default="itgmania/Songs", nargs="?")
    parser.add_argument("--difficulty", type=int, default=3)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    ingest_songs(args.dir, difficulty=args.difficulty, force=args.force)
