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
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    try:
        # 準備輸入
        inputs = tokenizer(user_message, return_tensors="pt", max_length=50, truncation=True)
        
        # 生成回應
        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_length=100,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                temperature=0.7
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # 發送回應
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )
    except Exception as e:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，我現在無法正確處理您的請求。")
        )

if __name__ == "__main__":
    app.run(port=5000)
