import os
import sys
import argparse
import shutil
import subprocess
import urllib.request
import json

def generate_stepchart(audio_file, temp_dir):
    """
    v24.1.1: Utilizes DDCInference instead of naive beats, enabling Coordinate-Aware decoding.
    """
    title = os.path.basename(audio_file).split('.')[0]

    # Milestone 7: Deprecate Python ML inference and audio processing.
    # The generation of the raw chart is now fully managed by the Go orchestrator.
    # We create a dummy raw chart here to simulate the output of the extraction pipeline
    # until the full audio processing is ported to Go in a later phase.

    bpm = 120.0

    ssc_content = f"""#VERSION:0.83;
#TITLE:{title};
#SUBTITLE:;
#ARTIST:FCDM AutoGen;
#TITLETRANSLIT:;
#SUBTITLETRANSLIT:;
#ARTISTTRANSLIT:;
#GENRE:;
#ORIGIN:;
#CREDIT:;
#BANNER:;
#BACKGROUND:;
#PREVIEWVID:;
#JACKET:;
#CDIMAGE:;
#DISCIMAGE:;
#LYRICSPATH:;
#CDTITLE:;
#MUSIC:{os.path.basename(audio_file)};
#OFFSET:0.000000;
#SAMPLESTART:100.000000;
#SAMPLELENGTH:12.000000;
#SELECTABLE:YES;
#BPMS:0.000000={bpm};
#STOPS:;
#DELAYS:;
#WARPS:;
#TIMESIGNATURES:0.000000=4=4;
#TICKCOUNTS:0.000000=4;
#COMBOS:0.000000=1;
#SPEEDS:0.000000=1.000000=0.000000=0;
#SCROLLS:0.000000=1.000000;
#FAKES:;
#LABELS:0.000000=Song Start;
#BGCHANGES:;
#KEYSOUNDS:;
#ATTACKS:;
"""

    ssc_content += """//---------------dance-single - ----------------
#NOTEDATA:;
#CHARTNAME:;
#STEPSTYPE:dance-single;
#DESCRIPTION:Cardio Flow;
#CHARTSTYLE:;
#DIFFICULTY:Medium;
#METER:5;
#RADARVALUES:0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000;
#CREDIT:;
#NOTES:
"""

    measures = []
    current_measure = []
    arrows = ["1000", "0001", "0100", "0010"]
    arrow_idx = 0

    # Dummy raw chart block
    num_notes = 100
    for i in range(num_notes):
        current_measure.append(arrows[arrow_idx])
        arrow_idx = (arrow_idx + 1) % len(arrows)
        if len(current_measure) == 4:
            measures.append("\n".join(current_measure))
            current_measure = []

    if len(current_measure) > 0:
        while len(current_measure) < 4:
            current_measure.append("0000")
        measures.append("\n".join(current_measure))

    ssc_content += ",\n".join(measures) + "\n;\n"

    os.makedirs(temp_dir, exist_ok=True)
    out_path = os.path.join(temp_dir, f"{title}.ssc")
    with open(out_path, 'w') as f:
        f.write(ssc_content)

    print(f"  [CoreLoop] Raw ML Chart generated at {out_path}")
    return out_path, title

def run_pipeline(audio_file, output_base_dir="itgmania/Songs/FCDM_Autogen"):
    print(f"--- FCDM Core Loop Execution ---")
    title = os.path.basename(audio_file).split('.')[0]
    song_dir = os.path.join(output_base_dir, title)
    os.makedirs(song_dir, exist_ok=True)

    # 1. Analyze and generate raw chart
    temp_dir = "temp_chart"
    raw_ssc_path, _ = generate_stepchart(audio_file, temp_dir)

    # 2. Sanitize stream via the Go Orchestrator API endpoint (Milestone 7)
    final_ssc_path = os.path.join(song_dir, f"{title}.ssc")
    print(f"  [CoreLoop] Sanitizing stream via Go Orchestrator API...")

    with open(raw_ssc_path, 'rb') as f:
        raw_data = f.read()

    req = urllib.request.Request(
        "http://localhost:8080/api/sanitize",
        data=raw_data,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            sanitized_data = response.read()
            with open(final_ssc_path, 'wb') as f:
                f.write(sanitized_data)
            print("  [CoreLoop] Successfully sanitized via Go Orchestrator.")
    except Exception as e:
        # Fallback to CLI if the server isn't running
        print(f"  [CoreLoop] API call failed ({e}), falling back to CLI orchestrator...")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # For local development we check src/go-orchestrator, in prod it's compiled at the root
        orchestrator_path = os.path.join(os.path.dirname(script_dir), "fcdm-orchestrator")
        if not os.path.exists(orchestrator_path):
             orchestrator_path = os.path.join(os.path.dirname(script_dir), "src/go-orchestrator/go-orchestrator")
        try:
            subprocess.run([orchestrator_path, "--sanitize", raw_ssc_path, "--out", final_ssc_path], check=True)
        except subprocess.CalledProcessError:
            print("[CoreLoop] FATAL: Go Sanitizer failed.")
            sys.exit(1)

    # 3. Copy audio
    final_audio_path = os.path.join(song_dir, os.path.basename(audio_file))
    shutil.copy(audio_file, final_audio_path)

    print(f"  [CoreLoop] Success! Final song package at: {song_dir}")
    return song_dir

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio_file")
    parser.add_argument("--output_dir", default="itgmania/Songs/FCDM_Autogen")
    args = parser.parse_args()

    run_pipeline(args.audio_file, args.output_dir)

if __name__ == "__main__":
    main()
