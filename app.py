from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定 LINE Bot 驗證
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')  # 請替換為你的 Channel Access Token
handler = WebhookHandler('YOUR_CHANNEL_SECRET')  # 請替換為你的 Channel Secret

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    print("Request body:", body)  # 輸出訊息正文
    print("Signature:", signature)  # 輸出簽名

    try:
        handler.handle(body, signature)  # 處理訊息
    except InvalidSignatureError:
        abort(400)  # 如果簽名錯誤，返回 400 錯誤
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 當接收到訊息時，發送回應
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="收到你的訊息！")  # 使用靜態回應來測試
    )

if __name__ == "__main__":
    app.run(port=5000)
