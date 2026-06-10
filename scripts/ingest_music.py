import os
import sys
import argparse
import glob
import re
import multiprocessing
from functools import partial

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

        # Determine duration from measures (16 rows per measure)
        measures = notes.count(',') + 1
        approx_seconds = measures * 2 # Assume 120bpm, 2s per measure

        nps = step_count / approx_seconds
        level = min(10, max(1, int(nps * 1.5)))
        return level
    except Exception:
        return 3

def process_single_song(audio_path, difficulty, force, dry_run):
    """Worker function for multiprocessing."""
    dir_name = os.path.dirname(audio_path)
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    ssc_path = os.path.join(dir_name, f"{base_name}.ssc")

    if not force and os.path.exists(ssc_path):
        try:
            with open(ssc_path, 'r', encoding='utf-8', errors='ignore') as f:
                if "(Fitness)" in f.read():
                    return f"SKIP: {base_name}"
        except Exception: pass

    if dry_run:
        return f"DRY-RUN: {base_name}"

    try:
        # 1. Generate skeleton with ML notes
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
#CREDIT:FCDM-v3.4.0;
{notes_data}
;
"""
        with open(ssc_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # 2. Sanitize
        sanitize_ssc(ssc_path, ssc_path)

        # 3. QA: Calculate and embed final Fitness Level
        fit_level = calculate_fitness_level(ssc_path)

        with open(ssc_path, 'r', encoding='utf-8') as f:
            ssc_content = f.read()
        new_content = ssc_content.replace("#DESCRIPTION:Automated;", f"#DESCRIPTION:Fitness Level {fit_level} (Fitness);")
        with open(ssc_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return f"SUCCESS: {base_name} (Level {fit_level})"
    except Exception as e:
        return f"ERROR: {base_name} ({e})"

def ingest_songs(songs_dir, difficulty=3, force=False, dry_run=False, cores=None):
    """
    Industrial Music Ingestion Pipeline (v3.4.0)
    Supports multiprocessing for bulk ingestion.
    """
    if cores is None:
        cores = max(1, multiprocessing.cpu_count() - 1)

    print(f"Ingesting songs from: {songs_dir} (Diff: {difficulty}, Cores: {cores})")

    audio_files = []
    extensions = ['*.mp3', '*.ogg', '*.wav']
    for ext in extensions:
        audio_files.extend(glob.glob(os.path.join(songs_dir, "**", ext), recursive=True))

    if not audio_files:
        print("No audio files found.")
        return

    print(f"Found {len(audio_files)} files. Starting pool...")

    worker_func = partial(process_single_song, difficulty=difficulty, force=force, dry_run=dry_run)

    with multiprocessing.Pool(processes=cores) as pool:
        # Using imap_unordered for better performance in long lists
        for result in pool.imap_unordered(worker_func, audio_files):
            print(f"  [{multiprocessing.current_process().name}] {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", default="itgmania/Songs", nargs="?")
    parser.add_argument("--difficulty", type=int, default=3)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cores", type=int, default=None)
    args = parser.parse_args()

    ingest_songs(args.dir, difficulty=args.difficulty, force=args.force, dry_run=args.dry_run, cores=args.cores)
