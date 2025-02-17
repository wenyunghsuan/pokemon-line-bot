from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = Flask(__name__)

# 設定 LINE Bot 驗證
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# 載入模型和tokenizer（使用較小的模型以符合免費資源限制）
model_name = "facebook/opt-125m"  # 這是一個較小的模型
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    print("Request body:", body)
    print("Signature:", signature)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="收到你的訊息！")  # 使用靜態回應來測試
    )


if __name__ == "__main__":
    app.run(port=5000)
