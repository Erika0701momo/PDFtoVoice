import tempfile
import pymupdf
import fitz
import cryptography
import os
import simpleaudio
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/user/serviceAccountKey/pdftoaudiobook-429604-87f458fbff39.json"

# PDFからテキスト抽出
doc = fitz.open("./マインドフルネス・セルフコンパッション.pdf")
# text_to_read = doc[0].get_text()
text_to_read = ""
for page in doc:
    text_to_read = text_to_read + page.get_text()

# clientをインスタンス化
client = texttospeech.TextToSpeechClient()

# 読み上げられるテキストをセット
synthesis_input = texttospeech.SynthesisInput(text=text_to_read)

# 声の設定
voice = texttospeech.VoiceSelectionParams(
    name="ja-JP-Neural2-D",
    language_code="ja-JP",
    ssml_gender=texttospeech.SsmlVoiceGender.MALE
)

# 生成する音声ファイルのエンコード方式
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    speaking_rate=1.3
)

# テキスト入力に対して、選択した音声パラメータと音声ファイルタイプで音声合成リクエストを実行する
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# 音声ファイルを再生
with tempfile.TemporaryDirectory() as tmp:
    with open(f"{tmp}/output.wav", "wb") as f:
        f.write(response.audio_content)
        wav_obj = simpleaudio.WaveObject.from_wave_file(f"{tmp}/output.wav")
        play_obj = wav_obj.play()
        play_obj.wait_done()