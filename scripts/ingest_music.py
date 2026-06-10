import os
import sys
import argparse
import glob
import re

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from stream_sanitizer import sanitize_ssc
from ddc_inference import generate_ddc_notes

def calculate_fitness_level(ssc_path):
    """
    Analyzes a generated chart and returns a 1-10 Fitness Level based on NPS.
    """
    try:
        with open(ssc_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Extract notes section
        notes_match = re.search(r'#NOTES:.*?\n(.*?;)', content, re.DOTALL)
        if not notes_match: return 1

        notes = notes_match.group(1)
        step_count = notes.count('1') + notes.count('2') + notes.count('4')

        # Determine duration from audio or approximate from measures
        # For v2.5.0 we approximate based on measures (16 rows per measure)
        measures = notes.count(',') + 1
        approx_seconds = measures * 2 # Assume 120bpm, 2s per measure

        nps = step_count / approx_seconds
        # Map NPS (0-10) to Fitness Level (1-10)
        level = min(10, max(1, int(nps * 1.5)))
        return level
    except Exception:
        return 3

def ingest_songs(songs_dir, difficulty=3, force=False, dry_run=False):
    """
    Automated Music Ingestion Pipeline (v2.5.0)
    """
    print(f"Ingesting songs from: {songs_dir} (Diff: {difficulty}, Force: {force}, DryRun: {dry_run})")

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

            if dry_run:
                print(f"  [DRY-RUN] Would process {audio_path}")
                continue

            print(f"  Processing {audio_path}...")
            create_skeleton_ssc(audio_path, ssc_path, difficulty)
            sanitize_ssc(ssc_path, ssc_path)

            # QA: Calculate and embed final Fitness Level
            fit_level = calculate_fitness_level(ssc_path)
            update_ssc_metadata(ssc_path, fit_level)

def update_ssc_metadata(ssc_path, fit_level):
    with open(ssc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Inject Fitness Level into Description
    new_content = content.replace("#DESCRIPTION:Automated;", f"#DESCRIPTION:Fitness Level {fit_level} (Fitness);")

    with open(ssc_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

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
#DESCRIPTION:Automated;
#DIFFICULTY:Medium;
#METER:{difficulty};
#CREDIT:FCDM-v2.5.0;
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
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    ingest_songs(args.dir, difficulty=args.difficulty, force=args.force, dry_run=args.dry_run)
