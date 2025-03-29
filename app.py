from flask import Flask, request
import os
import requests
import openai

app = Flask(__name__)
openai.api_key = os.environ.get("OPENAI_API_KEY")
LINE_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Incoming data:", data)  # Debugging line to inspect the payload

    # Check if 'events' exists and is not empty
    if not data or "events" not in data or len(data["events"]) == 0:
        return "No events found or invalid payload", 400

    # Safely access the first event
    try:
        user_msg = data["events"][0]["message"]["text"]
        reply_token = data["events"][0]["replyToken"]
    except (IndexError, KeyError) as e:
        print(f"Error accessing event data: {e}")
        return "Invalid event structure", 400

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是喪禮知識專家"},
            {"role": "user", "content": user_msg}
        ]
    )
    answer = response.choices[0].message.content

    # Reply to LINE
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": answer}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
