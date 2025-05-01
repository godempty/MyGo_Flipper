import json
import picsort as picsort

from google import genai
from google.genai import types
from flask import Flask, request, jsonify, render_template
from pydantic import BaseModel
from dotenv import load_dotenv
import os

class GeminiResponse(BaseModel):
    transcribe: str
    response: str

load_dotenv()
picsort.number_images()
app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

WORDS_JSON = open("words.json", "r", encoding="utf-8")
WORDS = json.loads(WORDS_JSON.read())
# print(words)
SYSTEM_PROMPT = f"""
你現在是一個名為 "MyGO!!!!! Gemini" 的虛擬對話夥伴，你的回答方式會完全採用動畫「Bang Dream! It's my GO!!!!!」中的台詞。

你的主要任務是：
1.  **讀取音檔，並理解我的對話內容。**
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

PROMPT = """
回覆音訊內容中的句子，如果有雜音可以忽略，如果全都是雜音或是無法分辨，請辨識為「&$%$hu#did」，你必須用 json 格式回應，範例如下：
input : "早安"
output : {
    "transcribe": "早安",
    "response": "31"
}
"""

SYSTEM_PROMPT_CONFIG = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    response_mime_type="application/json",
    response_schema=GeminiResponse,
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_content = audio_file.read()

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=SYSTEM_PROMPT_CONFIG,
        contents=[
            PROMPT,
            types.Part.from_bytes(
                data=audio_content,
                mime_type="audio/wav",
            ),
        ],
    )

    structured_response: GeminiResponse = response.parsed
    app.logger.info(f"{structured_response=}")

    transcribe = structured_response.transcribe
    generated_text = structured_response.response

    app.logger.info(f"{transcribe=}")
    app.logger.info(f"{generated_text=}")
    app.logger.info(WORDS[generated_text])
    return jsonify({"text": int(generated_text), "pic": WORDS[generated_text]})



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
