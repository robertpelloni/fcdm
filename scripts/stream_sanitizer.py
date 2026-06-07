import re
import os
import sys

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
            # In a real implementation, we would update the #BPMS and #OFFSET tags if they are 0 or missing.
            if '#BPMS:0.000=0.000' in content or '#BPMS:;' in content:
                 content = re.sub(r'#BPMS:.*?;', f'#BPMS:0.000={audio_data["bpm"]:.3f};', content)
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

            # 1. No Hands/Quads: Limit to max 2 steps per line
            step_count = line.count('1') + line.count('2') + line.count('4') # 1=tap, 2=hold head, 4=roll head
            if step_count > 2:
                # Convert extra steps to 0 (empty)
                count = 0
                new_line = list(line)
                for i, char in enumerate(new_line):
                    if char in '124':
                        count += 1
                        if count > 2:
                            new_line[i] = '0'
                line = "".join(new_line)

            # 2. No Double-Steps / Jacks:
            # If a step is on the same column as the immediate previous step,
            # and it's a fast stream (simplified: any consecutive same-col step in this pass),
            # we should technically look at timing, but for now we just prevent consecutive same-column steps
            # if they are within the same measure or very close.
            # Simplified: if it's the same column as the last step, move it or remove it?
            # For fitness flow, we want L-R-L-R.

            new_line = list(line)
            current_step_cols = [i for i, char in enumerate(new_line) if char in '124']

            if len(current_step_cols) == 1:
                if current_step_cols[0] == last_step_col:
                    # It's a jack. For simplicity in this script, we'll try to shift it
                    # to another column that isn't the last one.
                    # Or just remove it to keep the flow. Let's try to remove for now
                    # to enforce the "alternating" rule strictly.
                    new_line[current_step_cols[0]] = '0'
                else:
                    last_step_col = current_step_cols[0]
            elif len(current_step_cols) == 2:
                # If either matches last_step_col, it's a bit messy.
                # Jumping is okay but should we allow jumping on the same col?
                pass

            sanitized_lines.append("".join(new_line))
        sanitized_measures.append("\n".join(sanitized_lines))

    # Add Fitness flag to description if not already present
    if "#DESCRIPTION:" in chart_content:
        if "(Fitness)" not in chart_content:
            chart_content = re.sub(r'#DESCRIPTION:(.*?);', r'#DESCRIPTION:\1 (Fitness);', chart_content)

    new_notes_data = "#NOTES:\n" + ",\n".join(sanitized_measures) + ";"
    return chart_content.replace(notes_match.group(0), new_notes_data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        sanitize_ssc(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 2:
        sanitize_ssc(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python3 stream_sanitizer.py <input.ssc> <output.ssc> [audio_file]")
