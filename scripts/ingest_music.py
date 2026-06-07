import os
import sys
import subprocess
import glob

# Ensure we can import from scripts/
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from stream_sanitizer import sanitize_ssc

def ingest_songs(songs_dir):
    """
    Scans a directory for audio files and ensures they have a sanitized .ssc chart.
    """
    print(f"Ingesting songs from: {songs_dir}")

    # Supported audio extensions
    extensions = ['*.mp3', '*.ogg', '*.wav']

    for ext in extensions:
        # Search recursively
        for audio_path in glob.glob(os.path.join(songs_dir, "**", ext), recursive=True):
            dir_name = os.path.dirname(audio_path)
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            ssc_path = os.path.join(dir_name, f"{base_name}.ssc")

            needs_processing = True
            if os.path.exists(ssc_path):
                with open(ssc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    if "(Fitness)" in f.read():
                        needs_processing = False

            if needs_processing:
                if not os.path.exists(ssc_path):
                    print(f"  Generating skeleton for {audio_path}...")
                    create_skeleton_ssc(audio_path, ssc_path)

                print(f"  Sanitizing {ssc_path}...")
                # Sanitizer will also handle audio analysis if missing
                sanitize_ssc(ssc_path, ssc_path, audio_path)
            else:
                print(f"  Skipping {ssc_path} (already sanitized)")

def create_skeleton_ssc(audio_path, ssc_path):
    """
    Creates a minimal .ssc file for an audio file.
    """
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
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
#METER:5;
#RADARVALUES:0,0,0,0,0;
#CREDIT:FCDM;
0000
,
0000
;
"""
    with open(ssc_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    songs_dir = "itgmania/Songs"
    if len(sys.argv) > 1:
        songs_dir = sys.argv[1]

    if not os.path.exists(songs_dir):
        print(f"Directory not found: {songs_dir}")
        sys.exit(1)

    ingest_songs(songs_dir)
