from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import os
import json

# 從環境變數讀取 LINE API Token
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Webhook 接收請求
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# 處理使用者輸入
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    if user_text == "台南影片":
        video_list = [
            {"title": "台南旅遊 Day 1", "image": "https://drive.google.com/file/d/1NZ2ruevawMld37mRoY_8eetSRky0jgE_/view?usp=drive_link", "url": "https://drive.google.com/drive/folders/1S5j0rMYHqjAwUVswIYu6338OIDhcyRfP?usp=drive_link"},
            {"title": "台南旅遊 Day 2", "image": "https://drive.google.com/file/d/1Lhq4RjHQx4PJUF5q-3wySyuUhWCJPIvc/view?usp=drive_link", "url": "https://drive.google.com/drive/folders/1VgHmYa7ItKtIVMMg82no-nf62fpX-RFL?usp=drive_link"}
        ]

        flex_contents = []
        for video in video_list:
            flex_contents.append({
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": video["image"],
                    "size": "full",
                    "aspectRatio": "16:9",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": video["title"], "weight": "bold", "size": "lg"}
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "color": "#1DB446",
                            "action": {"type": "uri", "label": "觀看影片", "uri": video["url"]}
                        }
                    ]
                }
            })

        flex_message = {"type": "carousel", "contents": flex_contents}
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="請選擇旅遊影片", contents=flex_message))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入『台南影片』來觀看影片"))

# 啟動伺服器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

