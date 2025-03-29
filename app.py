from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    print("✅ 收到 LINE webhook 測試請求")
    print("🔎 請求內容：", request.get_json())
    return "OK", 200  # ✅ 明確回傳 200 給 LINE

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

