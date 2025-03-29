from flask import Flask, request
import os
import openai
import requests

app = Flask(__name__)

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("Incoming data:", data)

        events = data.get("events", [])
        if not events:
            print("⚠️ 沒有 events（LINE webhook 測試用）")
            return "OK", 200  # ✅ 回傳成功狀態給 LINE

        event = events[0]

        if "message" not in event or "text" not in event["message"]:
            print("⚠️ 非文字訊息")
            return "OK", 200

        user_msg = event["message"]["text"]
        reply_token = event["replyToken"]

        # 呼叫 OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一位台灣喪禮知識專家"},
                {"role": "user", "content": user_msg}
            ]
        )
        answer = response["choices"][0]["message"]["content"]

        # 回傳給 LINE 使用者
        headers = {
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json"
        }
        reply_body = {
            "replyToken": reply_token,
            "messages": [{"type": "text", "text": answer}]
        }
        requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=reply_body)

        return "OK", 200
    except Exception as e:
        print("❌ 發生錯誤：", str(e))
        return "ERROR", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
