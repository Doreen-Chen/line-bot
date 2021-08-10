# 100. [Web App專案] LINE聊天機器人 - part1
#
#    寫一個處理LINE server轉載過來的LINE訊息(對方密機器人的訊息)
#    用LINE官方釋出的SDK來寫處理程式
#
# & 101. [Web App專案] LINE聊天機器人 - part2
#    主要將客製後line bot放到雲端上
#    所以要找可以7*24服務的伺服器來執行
#      Amazon的AWS : 全球有1/3流量來到AWS
#      本專案使用 Heroku
# 

# flask 是 python 架設伺服器(=寫網站), 沒有畫面這類功能是放在雲端
# 另一個更有名套件 django, 通常做更大規模應用程式,且有網頁畫面
# Teacher : flask 的架構如果是網頁工程師會比較了解,這裡不多作說明
from flask import Flask, request, abort  # 架設伺服器

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)


# 等號左邊是程式名稱, 查看Procfile
app = Flask(__name__)


# ACCESS_TOKEN及CHANNEL_SECRET 才能與註冊的LINE機器人互動
# 'YOUR_CHANNEL_ACCESS_TOKEN' 權杖
line_bot_api = LineBotApi('Yt7WAUkveEg2M5t8Rrhq/clK2ewR3MC4LYshsfJRra3gS7lR+OGJ4FCQ024iquTvZx6sMIz/7tXLLZg1W5YPfls/JstJLCI52ZN23YV39QxzNTq8yRAoeppvbOOIO9B5u/tEKxb5dTzuUMC+vjZp0QdB04t89/1O/w1cDnyilFU=')  
# 'YOUR_CHANNEL_SECRET'
handler = WebhookHandler('20a7f0c7560bce12ffc4df04a66084f7')  


# 如果有人連結到 www.line-bot.com/callback 會執行這個function callback()
# route : 網頁路徑 ; /callback 返回觸發網頁 ; methods參數使用 POST
# 與 LINE Messaging API設定Webhook URL有關
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)  # 這裡會觸發 handle_message function
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回覆使用者傳來的訊息
    #   需要token(如前面設定)
    #   可看GitHub上 line bot的SDK, 也可回傳貼圖
    #   未程式原樣, user傳入什麼, line機器人也回傳同樣訊息 TextSendMessage(text=event.message.text)
    # original:
    #line_bot_api.reply_message(
    #    event.reply_token,
    #    TextSendMessage(text=event.message.text))  # event.message.text 使用者傳入的訊息

    user_msg = event.message.text
    s = '請留下聯絡方式,稍候由專人為您服務'

    # 回覆貼圖
    # 查詢 line-bot-sdk-python 及 sticker id
    if '貼圖' in user_msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message
        )

    else:
        if user_msg in ['hi', 'Hi', 'HI']: # 改用清單
            s = 'Hi, Welcome to join us'
        #elif user_msg == 'thank' or user_msg == 'tks':
        elif user_msg in ['thank', 'Thank', 'thanks', 'Thanks', 'tks', 'Tks']:  # 改用清單
            s = 'You are welcome'
        elif user_msg == '你是誰':
            s = '我是LINE bot'
        elif '訂位' in user_msg:
            s = '請問想預訂多少人呢'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=s)
        )


# 主程式增加if這行, 讓程式如果是被載入(import)不會一載入就執行
# 直接寫 app.run() 則import就執行本程式
if __name__ == "__main__":
    app.run()