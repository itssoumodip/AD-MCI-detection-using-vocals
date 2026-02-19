import pandas as pd
import os

def get_patient_word_segments(file_path):
    """
    Extract all patient (PAR) words with their individual timings from a .cha file.
    Returns a list of word segments with PAR utterance tracking.
    Also extracts silence information within each PAR line.
    """
    word_segments = []
    word_count = 0
    par_count = 0
    par_data = []  # Track data per PAR utterance

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        print(f"Total lines in file: {len(lines)}")

        i = 0
        while i < len(lines):
            line = lines[i].rstrip("\n")

            # Look for patient utterance lines
            if line.startswith("*PAR:"):
                par_count += 1
                par_content = line.replace("*PAR:", "").strip()
                # print(f"\nFound PAR utterance #{par_count} at line {i}: {par_content[:50]}")

                # Look ahead for the %wor: line (may be after %mor: and %gra: lines)
                j = i + 1
                found_wor = False
                par_words = []

                while j < len(lines) and j < i + 10:  # Look within next 10 lines
                    next_line = lines[j].rstrip("\n")

                    if next_line.startswith("%wor:"):
                        found_wor = True
                        # print(f"  Found %wor line!")
                        # Parse the word timings
                        wor_content = next_line.replace("%wor:", "").strip()

                        # Split by spaces to get words and timings
                        parts = wor_content.split()
                        # print(f"  Parts count: {len(parts)}")

                        k = 0
                        while k < len(parts):
                            word = parts[k]

                            # Check if next item is a timing (contains underscore)
                            # The timing might have tab characters, so clean it
                            if k + 1 < len(parts):
                                timing_raw = parts[k + 1]
                                # Remove tab characters and other whitespace
                                timing = timing_raw.replace("\x15", "").strip()

                                if "_" in timing:
                                    try:
                                        start_ms, end_ms = map(float, timing.split("_"))

                                        # Convert milliseconds to seconds
                                        start_sec = start_ms / 1000.0
                                        end_sec = end_ms / 1000.0
                                        duration_sec = end_sec - start_sec

                                        word_count += 1

                                        word_segment = {
                                            "word_num": word_count,
                                            "word": word,
                                            "start_ms": start_ms,
                                            "end_ms": end_ms,
                                            "start_sec": round(start_sec, 3),
                                            "end_sec": round(end_sec, 3),
                                            "duration_sec": round(duration_sec, 3),
                                            "par_num": par_count,
                                        }
                                        word_segments.append(word_segment)
                                        par_words.append(word_segment)

                                        k += 2
                                    except ValueError as e:
                                        print(f"    Error parsing timing '{timing}': {e}")
                                        k += 1
                                else:
                                    k += 1
                            else:
                                k += 1

                        # Calculate silences within this PAR line
                        if par_words:
                            par_data.append(
                                {
                                    "par_num": par_count,
                                    "par_text": par_content,
                                    "words": par_words,
                                    "total_duration": par_words[-1]["end_sec"]
                                    - par_words[0]["start_sec"],
                                }
                            )

                        break
                    elif next_line.startswith("*"):
                        # Reached next utterance without finding %wor
                        # print(f"  Reached next utterance without %wor")
                        break
                    else:
                        j += 1

                if not found_wor:
                    pass
                    # print(f"  Warning: No %wor line found for this PAR utterance")

            i += 1

        # print(f"\n\nTotal PAR utterances found: {par_count}")
        # print(f"Total words extracted: {word_count}")

    except Exception as e:
        print(f"Error reading file: {e}")
        import traceback
        traceback.print_exc()

    return word_segments, par_data


def get_word_segments_as_list(segments):
    """Return segments as a simple list for programmatic use"""
    return [(seg["word"], seg["start_sec"], seg["end_sec"]) for seg in segments]


def create_silence_map(segments, par_data):
    """
    Create a map of silence (gaps) WITHIN each PAR utterance.
    Only counts silences between words in the same PAR line, not between PAR lines.

    Returns:
        - silences: List of silence gaps within each PAR line
        - par_silence_summary: Summary of total silence per PAR utterance
    """
    if not par_data:
        return [], []

    silences = []
    par_silence_summary = []

    for par in par_data:
        par_num = par["par_num"]
        words = par["words"]
        par_total_silence = 0

        # Calculate silences between consecutive words WITHIN this PAR line
        for i in range(len(words) - 1):
            current_end = words[i]["end_sec"]
            next_start = words[i + 1]["start_sec"]

            silence_duration = next_start - current_end

            if silence_duration > 0:  # Only if there's a gap
                silences.append(
                    {
                        "par_num": par_num,
                        "par_text": par["par_text"][:50],  # First 50 chars
                        "between_word": f"{words[i]['word']} -> {words[i + 1]['word']}",
                        "silence_start": round(current_end, 3),
                        "silence_end": round(next_start, 3),
                        "silence_duration_sec": round(silence_duration, 3)
                    }
                )
                par_total_silence += silence_duration

        # Calculate PAR-level statistics
        par_total_duration = par["total_duration"]
        par_speech_duration = par_total_duration - par_total_silence

        par_silence_summary.append(
            {
                "par_num": par_num,
                "par_text": par["par_text"][:100],
                "total_duration_sec": round(par_total_duration, 3),
                "total_silence_sec": round(par_total_silence, 3),
                "total_speech_sec": round(par_speech_duration, 3),
                "silence_percentage": round(
                    (
                        (par_total_silence / par_total_duration * 100)
                        if par_total_duration > 0
                        else 0
                    ),
                    2,
                ),
                "num_words": len(words),
                "num_silences": len(words) - 1,  # n-1 gaps for n words
            }
        )

    return silences, par_silence_summary


def get_report(file_path):
    # Get all patient word segments and PAR data
    word_segments, par_data = get_patient_word_segments(file_path)

    if word_segments:
        # Create silence map (WITHIN each PAR line only)
        silences, par_silence_summary = create_silence_map(word_segments, par_data)

        if par_silence_summary:
            return silences, par_silence_summary, word_segments
        else:
            print("No PAR utterances with silence found!")
            return [], [], []
    else:
        print("No patient word segments found!")
        return [], [], []
