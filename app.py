from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("✅ LINE Webhook 收到資料：", data)
        return "OK", 200
    except Exception as e:
        print("❌ 錯誤：", str(e))
        return "ERROR", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
