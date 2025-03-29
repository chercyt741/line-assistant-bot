from flask import Flask, request, abort
import os
from dotenv import load_dotenv
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize LINE API with credentials from environment variables
line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))

@app.route("/", methods=["GET"])
def home():
    return "Welcome to LINE Assistant Bot!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    # Get X-Line-Signature header value
    signature = request.headers.get('X-Line-Signature')
    
    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    print("✅ 收到 LINE webhook 請求")
    print("🔎 請求內容：", json.loads(body) if body else "Empty body")
    
    try:
        # Validate the signature
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("⚠️ Invalid signature. Check your LINE_CHANNEL_SECRET.")
        abort(400)
        
    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Handle incoming text messages"""
    text = event.message.text
    print(f"📩 Received message: {text}")
    
    # Echo the received message for now (you can implement your custom logic here)
    response_message = f"You said: {text}"
    
    # Reply to the user
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_message)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4999, debug=True)
    print("✅ 伺服器已啟動")

