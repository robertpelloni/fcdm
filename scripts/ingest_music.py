import os
import sys
import subprocess
import glob
import argparse

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from stream_sanitizer import sanitize_ssc
from ddc_inference import generate_ddc_notes

def ingest_songs(songs_dir, difficulty=3, force=False):
    """
    Scans a directory for audio files and ensures they have a sanitized .ssc chart.
    """
    print(f"Ingesting songs from: {songs_dir} (Difficulty: {difficulty}, Force: {force})")

    extensions = ['*.mp3', '*.ogg', '*.wav']

    for ext in extensions:
        for audio_path in glob.glob(os.path.join(songs_dir, "**", ext), recursive=True):
            dir_name = os.path.dirname(audio_path)
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            ssc_path = os.path.join(dir_name, f"{base_name}.ssc")

            needs_processing = True
            if not force and os.path.exists(ssc_path):
                with open(ssc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    if "(Fitness)" in f.read():
                        needs_processing = False

            if needs_processing:
                print(f"  Processing {audio_path}...")
                create_skeleton_ssc(audio_path, ssc_path, difficulty)
                # Sanitizer will also handle audio analysis if missing
                sanitize_ssc(ssc_path, ssc_path, audio_path)
            else:
                print(f"  Skipping {ssc_path} (already sanitized)")

def create_skeleton_ssc(audio_path, ssc_path, difficulty):
    """
    Creates a minimal .ssc file for an audio file with Deep Learning ML-generated notes.
    """
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    notes_data = generate_ddc_notes(audio_path, difficulty=difficulty)

    content = f"""#VERSION:0.81;
#TITLE:{base_name};
#ARTIST:Unknown;
#MUSIC:{os.path.basename(audio_path)};
#OFFSET:0.000;
#BPMS:0.000=0.000;
#SAMPLESTART:0.000;
#SAMPLELENGTH:15.000;

//---------------dance-single -
#NOTES:
#STEPSTYPE:dance-single;
#CHARTNAME:;
#DESCRIPTION:Automated;
#CHARTSTYLE:;
#DIFFICULTY:Medium;
#METER:{difficulty};
#RADARVALUES:0,0,0,0,0;
#CREDIT:FCDM;
{notes_data}
;
"""
    with open(ssc_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FCDM Music Ingestion Pipeline")
    parser.add_argument("dir", nargs="?", default="itgmania/Songs", help="Songs directory")
    parser.add_argument("--difficulty", type=int, default=3, help="ML Generation difficulty (1-5)")
    parser.add_argument("--force", action="store_true", help="Force re-processing of already sanitized songs")
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        print(f"Directory not found: {args.dir}")
        sys.exit(1)

    ingest_songs(args.dir, difficulty=args.difficulty, force=args.force)
