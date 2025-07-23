from pydub import AudioSegment
import os

def convert_to_wav(path: str) -> str:
    output_path = path.rsplit(".", 1)[0] + ".wav"
    sound = AudioSegment.from_file(path)
    sound.export(output_path, format="wav")
    return output_path
