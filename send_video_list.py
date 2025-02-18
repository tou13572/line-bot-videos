from linebot import LineBotApi
from linebot.models import FlexSendMessage
import json

# 設定你的 LINE Bot Token
LINE_CHANNEL_ACCESS_TOKEN = "HtFwVbDkr8bVCozbLviv0mF+JvQ+6aNGk61PNegLbAeJoIp8CWjXm7uOTPHAESIwW+h24qrWyR9YaCpDfmOeQ2JYm9gRWHg4EMGul7tntY5wqeE8vZPpysR+Ah98UnMTj/rge1hGoEyqPvSF8ydZOwdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# 影片清單（台南兩天一夜）
video_list = [
    {"title": "台南旅遊 - Day 1", "image": "C:\Users\cynth\OneDrive\桌面\linebot\photo\tainanday2.jpg", "url": "https://drive.google.com/drive/folders/1S5j0rMYHqjAwUVswIYu6338OIDhcyRfP?usp=drive_link"},
    {"title": "台南旅遊 - Day 2", "image": "C:\Users\cynth\OneDrive\桌面\linebot\photo\tainanday1.jpg", "url": "https://drive.google.com/drive/folders/1VgHmYa7ItKtIVMMg82no-nf62fpX-RFL?usp=drive_link"}
]

# 建立 Flex Message
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

# 發送 Flex Message
flex_message = {"type": "carousel", "contents": flex_contents}
line_bot_api.push_message("你的使用者 LINE ID", FlexSendMessage(alt_text="請選擇旅遊影片", contents=flex_message))
