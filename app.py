import os
import json
import picsort as picsort
import esp32_control as esp32_control

from google import genai
from google.genai import types
from flask import Flask, request, jsonify, render_template

picsort.number_images()
app = Flask(__name__)

client = genai.Client()

WORDS_JSON = open("words.json", "r", encoding="utf-8")
WORDS = json.loads(WORDS_JSON.read())
# print(words)
SYSTEM_PROMPT = f"""
你現在是一個名為 "MyGO!!!!! Gemini" 的虛擬對話夥伴，你的回答方式會完全採用動畫「Bang Dream! It's my GO!!!!!」中的台詞。

你的主要任務是：
1.  **理解我的對話內容。**
2.  **根據對話內容，從以下提供的台詞中選擇一句最符合情境的台詞。**
3.  **直接回傳所選語句對應的編號，不需要回覆其他文字。**

**以下是你可以選擇的台詞:**
{WORDS}
**舉例：**
如果我的對話是 "早安"，你應該選擇「貴安」或是「早安喵姆喵姆」這句台詞回覆。

必要時可以選擇最有趣的台詞回覆，但請確保回覆的內容與對話內容有關，可能是諧音或是反諷等等。
但你也需要注意，這些台詞是來自動畫中的角色，所以有些台詞可能不適合用在所有情境中。
**舉例：**
如果我的對話是 "你為甚麼不理我"，你可以選擇「是這樣嗎」，或是「我還是會繼續下去」回覆。
**現在，開始吧！**
"""

SYSTEM_PROMPT_CONFIG = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    # 語音轉文字
    audio_file = request.files["audio"]
    audio_content = audio_file.read()
    transcript = transcribe_audio(audio_content)
    app.logger.info(f"transcript: {transcript}")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=SYSTEM_PROMPT_CONFIG,
        contents=f"回覆以下句子:{transcript}",
    )
    app.logger.info(f"{response.text=}")

    generated_text = response.text.strip()
    app.logger.info(f"generated_text: {generated_text}")
    app.logger.info(WORDS[generated_text])
    response = esp32_control.control_esp(int(generated_text))
    app.logger.info(f"send {int(generated_text)} to esp32, {response=}")
    return jsonify({"text": int(generated_text), "pic": WORDS[generated_text]})


def transcribe_audio(audio_content):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            "請將以下語音轉文字並直接輸出，如果有雜音可以忽略，如果全都是雜音或是無法分辨，請回覆「&$%$hu#did」",
            types.Part.from_bytes(
                data=audio_content,
                mime_type="audio/wav",
            ),
        ],
    )

    app.logger.info(f"{response.text=}")
    return response.text.strip()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
