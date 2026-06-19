import os
import sys
import argparse
import shutil
from audio_processor import analyze_audio
from stream_sanitizer import sanitize_ssc

def generate_stepchart(audio_file, temp_dir):
    """
    Generates a StepMania SSC file based on audio analysis.
    """
    bpm, beats = analyze_audio(audio_file)
    title = os.path.basename(audio_file).split('.')[0]

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

    for i in range(len(beats)):
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

    print(f"  [CoreLoop] Raw Chart generated at {out_path}")
    return out_path, title

def run_pipeline(audio_file, output_base_dir="itgmania/Songs/FCDM_Autogen"):
    print(f"--- FCDM Core Loop Execution ---")
    title = os.path.basename(audio_file).split('.')[0]
    song_dir = os.path.join(output_base_dir, title)
    os.makedirs(song_dir, exist_ok=True)

    # 1. Analyze and generate raw chart
    temp_dir = "temp_chart"
    raw_ssc_path, _ = generate_stepchart(audio_file, temp_dir)

    # 2. Sanitize stream
    final_ssc_path = os.path.join(song_dir, f"{title}.ssc")
    print(f"  [CoreLoop] Sanitizing stream...")
    sanitize_ssc(raw_ssc_path, final_ssc_path)

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
