import re
import os
import sys
import numpy as np

# Add the scripts directory to path to import audio_processor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from audio_processor import analyze_audio
except ImportError:
    analyze_audio = None

def sanitize_ssc(input_path, output_path, audio_path=None):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If audio_path is provided and we lack BPM/Offset, we inject the analyzed results.
    needs_timing = ('#BPMS:0.000=0.000' in content or '#BPMS:;' in content or
                    '#OFFSET:0.000' in content or '#OFFSET:;' in content)

    if audio_path and analyze_audio and needs_timing:
        try:
            audio_data = analyze_audio(audio_path)
            print(f"Audio analysis successful: BPM={audio_data['bpm']}")

            # Map Multi-BPM segments to SM #BPMS tag
            bpm_str = ",".join([f"{beat:.3f}={bpm:.3f}" for beat, bpm in audio_data["bpms"]])
            content = re.sub(r'#BPMS:.*?;', f'#BPMS:{bpm_str};', content)

            if '#OFFSET:0.000' in content or '#OFFSET:;' in content:
                 offset = audio_data['downbeats'][0] if audio_data['downbeats'] else 0.0
                 content = re.sub(r'#OFFSET:.*?;', f'#OFFSET:{-offset:.3f};', content)
        except Exception as e:
            print(f"Audio analysis failed: {e}")

    # Split into charts
    charts = re.split(r'//---------------', content)
    header = charts[0]
    processed_charts = []

    for chart in charts[1:]:
        processed_charts.append(process_chart(chart))

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(header)
        for chart in processed_charts:
            f.write('//---------------' + chart)

def process_chart(chart_content):
    # Extract notes section
    notes_match = re.search(r'#NOTES:\n(.*?);', chart_content, re.DOTALL)
    if not notes_match:
        return chart_content

    notes_data = notes_match.group(1)
    measures = notes_data.split(',')
    sanitized_measures = []
    last_step_col = -1

    for measure in measures:
        lines = measure.strip().split('\n')
        sanitized_lines = []
        for line in lines:
            line = line.strip()
            if not line: continue
            step_count = line.count('1') + line.count('2') + line.count('4')
            if step_count > 2:
                count, new_line = 0, list(line)
                for i, char in enumerate(new_line):
                    if char in '124':
                        count += 1
                        if count > 2: new_line[i] = '0'
                line = "".join(new_line)
            new_line = list(line)
            current_step_cols = [i for i, char in enumerate(new_line) if char in '124']
            if len(current_step_cols) == 1:
                if current_step_cols[0] == last_step_col: new_line[current_step_cols[0]] = '0'
                else: last_step_col = current_step_cols[0]
            sanitized_lines.append("".join(new_line))
        sanitized_measures.append("\n".join(sanitized_lines))

    if "#DESCRIPTION:" in chart_content and "(Fitness)" not in chart_content:
        chart_content = re.sub(r'#DESCRIPTION:(.*?);', r'#DESCRIPTION:\1 (Fitness);', chart_content)

    new_notes_data = "#NOTES:\n" + ",\n".join(sanitized_measures) + ";"
    return chart_content.replace(notes_match.group(0), new_notes_data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3: sanitize_ssc(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 2: sanitize_ssc(sys.argv[1], sys.argv[2])
    else: print("Usage: python3 stream_sanitizer.py <input.ssc> <output.ssc> [audio_file]")
