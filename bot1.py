from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

app = Flask(__name__)

# 設定你的 Channel Access Token 和 Secret
CHANNEL_ACCESS_TOKEN = 'Z3uo8wLFrXiB5LM8y7j7ENX0l5NkYNIOZ3dMAR248Uv03GBAM99XPtlutW8I5Vgy3e5JR0IOngB0GRHZ/roqA2r4y3e5xKcoQMLKT9hn2On/BQv0R6iEhj1rfsysaMeQ6IVZ1fIsCwZCsqFVjoReqgdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'eceaa78724c62385aaa0d30ab563dd35'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

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
    # 確認事件來自群組
    if event.source.type == 'group':
        group_id = event.source.group_id  # 獲取群組 ID
        user_message = event.message.text

        # 如果使用者傳送了 "今日值班"，回應群組訊息
        if user_message == '今日值班':
            reply_text = "今天的值班人是：Alice"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
    else:
        # 回應私人訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請在群組中使用此指令。")
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
