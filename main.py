import tempfile
import fitz
import cryptography
import os
from google.cloud import texttospeech
import faulthandler
import pygame

if __name__ == "__main__":
    faulthandler.enable()

# googleサービスアカウントの鍵を設定
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="○○"

# PDFファイルを読み込む
doc = fitz.open("./マインドフルネス呼吸.pdf")

# clientをインスタンス化
client = texttospeech.TextToSpeechClient()

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


for page in doc:
    text_to_read = page.get_text()

    # 読み上げられるテキストをセット
    synthesis_input = texttospeech.SynthesisInput(text=text_to_read)

    # テキスト入力に対して、選択した音声パラメータと音声ファイルタイプで音声合成リクエストを実行する
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 音声ファイルを再生
    with tempfile.TemporaryDirectory() as tmp:
        output_file = f"{tmp}/output.wav"
        with open(output_file, "wb") as f:
            f.write(response.audio_content)
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print("1ページ読み上げ終了")

        pygame.mixer.music.unload()  # ファイルの使用を解除する
