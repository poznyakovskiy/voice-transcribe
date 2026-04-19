from vosk import Model, KaldiRecognizer
from os.path import expanduser
import wave
import json
import ffmpeg
import os
import glob

input_folder = '/data/GDrive/Audio Notes'
output_folder = expanduser('~/Documents/Transcribed Notes')

model = Model("vosk-model-ru-0.42")
recognizer = KaldiRecognizer(model, 16000)

def convert_to_wav(input_path, output_path):
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path, acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        print(f"Ошибка при конвертации {input_path}:")
        print("STDOUT:", e.stdout.decode(errors='ignore'))
        print("STDERR:", e.stderr.decode(errors='ignore'))
        raise

audio_files = glob.glob(os.path.join(os.path.expanduser(input_folder), '*.m4a'))

print("Файлы для обработки:")
for f in audio_files:
    print(f)

for audio_path in audio_files:
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    txt_path = os.path.join(output_folder, f'{base_name}.txt')

    if os.path.exists(txt_path):
        continue

    wav_path = os.path.join(output_folder, f'{base_name}.wav')

    print(f"Обрабатываю: {audio_path}")
    try:
      convert_to_wav(audio_path, wav_path)
    except ffmpeg.Error as e:
        continue

    wf = wave.open(wav_path, "rb")
    recognizer.AcceptWaveform(wf.readframes(wf.getnframes()))
    result = json.loads(recognizer.FinalResult())
    text = result.get("text", "")

    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Сохранено: {txt_path}")
    os.remove(wav_path)

print("Готово.")
