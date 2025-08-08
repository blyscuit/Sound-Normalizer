import os
from pydub import AudioSegment
from pydub.utils import mediainfo

# Set this to your folder containing audio files
AUDIO_FOLDER = "raw_audio"
NORMALIZED_FOLDER = "audio"
TARGET_DBFS = -30.0  # Target volume in dBFS

SUPPORTED_FORMATS = ('.mp3', '.ogg', '.wav')

def match_target_amplitude(sound, target_dBFS):
    """Normalize given sound to target dBFS."""
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def normalize_audio_file(filepath, output_folder, target_dBFS):
    filename = os.path.basename(filepath)
    file_ext = os.path.splitext(filename)[1][1:].lower()

    try:
        sound = AudioSegment.from_file(filepath, format=file_ext)
        normalized_sound = match_target_amplitude(sound, target_dBFS)
        output_path = os.path.join(output_folder, filename)
        normalized_sound.export(output_path, format=file_ext)
        print(f"Normalized: {filename}")
    except Exception as e:
        print(f"Failed to normalize {filename}: {e}")

def normalize_audio_folder(folder, target_dBFS):
    os.makedirs(NORMALIZED_FOLDER, exist_ok=True)
    for filename in os.listdir(folder):
        if filename.lower().endswith(SUPPORTED_FORMATS):
            filepath = os.path.join(folder, filename)
            normalize_audio_file(filepath, NORMALIZED_FOLDER, target_dBFS)

if __name__ == "__main__":
    normalize_audio_folder(AUDIO_FOLDER, TARGET_DBFS)
    print("Normalization complete.")
