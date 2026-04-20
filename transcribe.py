from vosk import KaldiRecognizer
import wave
import json
import ffmpeg
import os

def _convert_to_wav(input_path, output_path):
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path, acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        print(f"Conversion error for {input_path}:")
        print("STDOUT:", e.stdout.decode(errors='ignore'))
        print("STDERR:", e.stderr.decode(errors='ignore'))
        raise


def transcribe_file(audio_path, output_folder, model, overwrite=False):
    """Transcribe a single audio file and save the result as a .txt in output_folder.

    Skips processing if the .txt already exists unless overwrite is True.
    Returns the transcribed text string.
    """
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    txt_path = os.path.join(output_folder, f'{base_name}.txt')

    if os.path.exists(txt_path) and not overwrite:
        with open(txt_path, encoding='utf-8') as f:
            return f.read()

    os.makedirs(output_folder, exist_ok=True)
    wav_path = os.path.join(output_folder, f'{base_name}.wav')

    _convert_to_wav(audio_path, wav_path)

    try:
        recognizer = KaldiRecognizer(model, 16000)
        wf = wave.open(wav_path, "rb")
        recognizer.AcceptWaveform(wf.readframes(wf.getnframes()))
        wf.close()
        text = json.loads(recognizer.FinalResult()).get("text", "")
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

    return text
