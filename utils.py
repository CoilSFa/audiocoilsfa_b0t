from pydub import AudioSegment

def convert_to_wav(path: str) -> str:
    output_path = path.replace(".ogg", ".wav")
    sound = AudioSegment.from_file(path)
    sound.export(output_path, format="wav")
    return output_path
