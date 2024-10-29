from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from linebot import LineBotApi
from linebot.models import TextSendMessage
import json
from datetime import datetime

# 初始化 Flask 應用
app = Flask(__name__)

# LINE Bot 配置
CHANNEL_ACCESS_TOKEN = 'Z3uo8wLFrXiB5LM8y7j7ENX0l5NkYNIOZ3dMAR248Uv03GBAM99XPtlutW8I5Vgy3e5JR0IOngB0GRHZ/roqA2r4y3e5xKcoQMLKT9hn2On/BQv0R6iEhj1rfsysaMeQ6IVZ1fIsCwZCsqFVjoReqgdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

# 讀取排班表的函數
def get_this_week_shift():
    today = datetime.now().strftime('%Y-%m-%d')
    with open('schedule.json', 'r') as f:
        schedule = json.load(f)
    for record in schedule:
        if record['date'] == today:
            return f"本週的值班人是：{record['duty']}"
    return "本週沒有排班紀錄。"

# 傳送本週值班通知的函數
def send_weekly_shift_notification():
    try:
        shift_info = get_this_week_shift()
        # 傳送訊息到某個聊天室 (群組或使用者 ID)
        line_bot_api.push_message(
            'U14ecf9c86126bb5ddfd66abfae0c3c4c',  # 更改為目標使用者或群組的 ID
            TextSendMessage(text=shift_info)
        )
        print("本週值班通知已發送。")
    except Exception as e:
        print(f"Error sending message: {e}")

# APScheduler 設定
scheduler = BackgroundScheduler()
# 設定每週一上午10點執行
scheduler.add_job(send_weekly_shift_notification, 'interval', minutes=1)
scheduler.start()

# Flask 根路由測試
@app.route("/")
def home():
    return "Flask server is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
