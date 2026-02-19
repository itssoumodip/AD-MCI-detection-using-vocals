import pandas as pd
import os
import sys

# Add current directory to path to allow importing from utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.pause_cha_word_by_word import get_report
except ImportError:
    # If running from root
    from backend.utils.pause_cha_word_by_word import get_report

def extract_features_from_patient(cha_file):
    """
    Extract pause and speech timing features from a single patient's .cha file
    
    Returns: Dictionary with all computed features
    """
    
    # Ensure file exists
    if not os.path.exists(cha_file):
        print(f"Error: File not found: {cha_file}")
        return None

    try:
        results = get_report(cha_file)
        # Check if we got valid results (not empty tuples)
        if not results or len(results) != 3 or not results[1]:
            print(f"Warning: No valid segments found in {cha_file}")
            return None
            
        silences, get_silence_summary, word_segments = results
    except Exception as e:
        print(f"Error processing file {cha_file}: {e}")
        return None

    if not silences:
        silences_durations = [0]
    else:
        silences_durations = [s['silence_duration_sec'] for s in silences]
    
    total_duration = [i['total_duration_sec'] for i in get_silence_summary]
    total_speech_times = [i['total_speech_sec'] for i in get_silence_summary]
    total_pause_times = [i['total_silence_sec'] for i in get_silence_summary]
    
    no_of_silences = [w['num_silences'] for w in get_silence_summary]
    
    # Calculate features matching the training data
    features = {
        # Key pause patterns (Cohen's d = 0.572)
        'pause_count': sum(no_of_silences),
        
        # Speech timing (Cohen's d = 0.513)
        'total_speech_time': round(sum(total_duration), 4), # Note: In original code this was sum(total_duration) but mapped to 'total_speech_time'. Let's verify.
        # Original: 'total_speech_time': round(sum(total_duration), 4),
        # Wait, total_duration is duration of utterance (speech + silence).
        # total_speech_time usually means pure speech.
        # But let's stick to EXACTLY what was in _main_features.py to be consistent with the model.
        
        # Pause timing (Cohen's d = 0.316)
        'total_pause_time': round(sum(total_pause_times), 4),
        
        # Speech rate components (Cohen's d = 0.310)
        'mean_word_duration': round(sum(total_speech_times) / len(word_segments), 4) if word_segments else 0,
        
        # Speech rate metric (Cohen's d = 0.304)
        'speech_rate_wpm': round((len(word_segments) / sum(total_speech_times)) * 60, 2) if sum(total_speech_times) > 0 else 0,
        
        # Pause frequency ratio (Cohen's d = 0.289)
        'pause_per_word_ratio': round(len(silences) / len(word_segments), 4) if word_segments else 0,
    }
    
    # Verify mapping from original file:
    # 'total_speech_time': round(sum(total_duration), 4),
    # total_duration comes from [i['total_duration_sec'] for i in get_silence_summary]
    # Yes, it seems the original code labeled 'total_duration' sum as 'total_speech_time'. 
    # This might be a misnomer in the original code, but we must replicate it for the model to work.
    
    return features
