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
from audio_processor import analyze_audio

def calculate_fitness_level(notes_block):
    """
    Analyzes a notes block and returns a 1-10 Fitness Level based on NPS.
    """
    try:
        step_count = notes_block.count('1') + notes_block.count('2') + notes_block.count('4')
        measures = notes_block.count(',') + 1
        approx_seconds = measures * 2
        nps = step_count / approx_seconds
        level = min(10, max(1, int(nps * 1.5)))
        return level
    except Exception:
        return 3

def process_single_song(audio_path, difficulty, force, dry_run):
    """Worker function for multiprocessing bulk ingestion (v3.8.1)."""
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
        # 1. High-fidelity Audio Analysis
        audio_info = analyze_audio(audio_path)
        bpm_str = ",".join([f"{t}={b}" for t, b in audio_info['bpms']])

        # 2. Generate multi-mode charts
        notes_single = generate_ddc_notes(audio_path, difficulty=difficulty, mode='dance-single')
        notes_double = generate_ddc_notes(audio_path, difficulty=difficulty, mode='dance-double')

        fit_single = calculate_fitness_level(notes_single)
        fit_double = calculate_fitness_level(notes_double)

        content = f"""#VERSION:0.81;
#TITLE:{base_name};
#ARTIST:FCDM-AI;
#MUSIC:{os.path.basename(audio_path)};
#OFFSET:{audio_info['offset']};
#BPMS:{bpm_str};

//---------------dance-single -
#NOTES:
#STEPSTYPE:dance-single;
#DESCRIPTION:Fitness Level {fit_single} (Fitness);
#DIFFICULTY:Medium;
#METER:{difficulty};
#CREDIT:FCDM-v3.8.1;
{notes_single}
;

//---------------dance-double -
#NOTES:
#STEPSTYPE:dance-double;
#DESCRIPTION:Fitness Level {fit_double} (Fitness);
#DIFFICULTY:Medium;
#METER:{difficulty};
#CREDIT:FCDM-v3.8.1;
{notes_double}
;
"""
        with open(ssc_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # 3. Sanitize resulting charts
        sanitize_ssc(ssc_path, ssc_path)

        return f"SUCCESS: {base_name} (S:{fit_single}, D:{fit_double})"
    except Exception as e:
        return f"ERROR: {base_name} ({e})"

def ingest_songs(songs_dir, difficulty=3, force=False, dry_run=False, cores=None):
    if cores is None:
        cores = max(1, multiprocessing.cpu_count() - 1)

    print(f"Ingesting songs (Single+Double) from: {songs_dir} (Cores: {cores})")
    audio_files = []
    for ext in ['*.mp3', '*.ogg', '*.wav']:
        audio_files.extend(glob.glob(os.path.join(songs_dir, "**", ext), recursive=True))

    if not audio_files: return

    worker_func = partial(process_single_song, difficulty=difficulty, force=force, dry_run=dry_run)
    with multiprocessing.Pool(processes=cores) as pool:
        for result in pool.imap_unordered(worker_func, audio_files):
            print(f"  [Worker] {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", default="itgmania/Songs", nargs="?")
    parser.add_argument("--difficulty", type=int, default=3)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cores", type=int, default=None)
    args = parser.parse_args()
    ingest_songs(args.dir, difficulty=args.difficulty, force=args.force, dry_run=args.dry_run, cores=args.cores)
