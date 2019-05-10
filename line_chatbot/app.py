from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
from linebot.exceptions import InvalidSignatureError, LineBotApiError

app = Flask(__name__)

TOKEN = "035x0wZZGHJFERHT4Vl5UamyrIWjQLpQQ32DiX9gp7SLB2Li9SMSmRHMTfahAeyHOmJrAuFNOmfhq7H+8Z6ppcr1+R2i0jO1jUAJEOiMGxzSa26o8pwrwfdPtyL69DsfQG3+d5mpGRhSm5GzaYfkSQdB04t89/1O/w1cDnyilFU="
SECRET = "b1a052393bab641e73936af7ccb3ef9c"

line_bot_api = LineBotApi(TOKEN, "http://localhost:8080")
handler = WebhookHandler(SECRET)

@app.route("/")
def index():
	return "Hello World!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)


if __name__ == "__main__":
	app.run(debug=True)