from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import *
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from models import Input
from main2 import recommend
import json

app = Flask(__name__)

TOKEN = ""
SECRET = ""
LIMIT_FUNDS_NUM = 3
LIMIT_FUNDS_RATIO = 0.3

line_bot_api = LineBotApi(TOKEN)
handler = WebhookHandler(SECRET)


@app.route("/")
def index():
    return ""

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
    All_state = json.load(open("db.txt"))
    user_input = event.message.text
    user_id = event.source.user_id

    if user_id not in All_state:
        All_state[user_id] = 0
    user_state = All_state[user_id]
    # print(All_state)

    if user_state == 0 and (user_input == "E" or user_input == "e"):
        text = "請依照下列格式輸入你的基金組合喔\U0010005E:\n\n" + \
            "[基金1統編]:[基金1比重],[基金2統編]:[基金2比重]...\n\n" + \
            "範例:\n" + \
            "26396604B:0.4,26286281F:0.6"
        message = TextMessage(text=text)
        line_bot_api.reply_message(event.reply_token,message)
        All_state[user_id] = 1

    elif user_state == 0:
        text = "" + \
            "嗨\U0010005E\U0010005E\U0010005E!\n" + \
            "這是一個評估/推薦基金組合的聊天機器人\U0010005E。\n\n" + \
            "如果想要評估目前的基金組合，請輸入\"E\"。"
        message = TextMessage(text=text)
        line_bot_api.reply_message(event.reply_token,message)

    elif user_state == 1 and (user_input == "Q" or user_input == "q"):
        text = "" + \
            "嗨\U0010005E\U0010005E\U0010005E!\n" + \
            "這是一個評估/推薦基金組合的聊天機器人\U0010005E。\n\n" + \
            "如果想要評估目前的基金組合，請輸入\"E\"。"
        message = TextMessage(text=text)
        line_bot_api.reply_message(event.reply_token,message)
        All_state[user_id] = 0

    elif user_state == 1:
        try:
            user_input_splited = user_input.split(",")
            selectFunds = []
            selectFund_weights = []
            for item in user_input_splited:
                temp_fund, temp_weight = item.split(":",1)
                selectFunds.append(temp_fund)
                selectFund_weights.append(float(temp_weight))
            # print(selectFunds,selectFund_weights)

            All_selectFunds = json.load(open("selectFunds.txt"))
            All_selectFunds_weights = json.load(open("selectFund_weights.txt"))
            # print(All_selectFunds,All_selectFunds_weights)
            All_selectFunds[user_id] = selectFunds
            All_selectFunds_weights[user_id] = selectFund_weights
            json.dump(All_selectFunds,open("selectFunds.txt","w"))
            json.dump(All_selectFunds_weights,open("selectFund_weights.txt","w"))
            # print(All_selectFunds,All_selectFunds_weights)

            # evaluate
            extra_ratio = 0
            recommend_num = 0

            user_input = Input(extra_ratio,selectFunds,selectFund_weights,recommend_num)
            origin, result = recommend(user_input,line_bot_api,user_id)
                
            # Check
            check_ration = 0
            for item in selectFund_weights:
                if item < 0:
                    check_ration = -1
                    break
                check_ration += item
            if check_ration != 1:
               message = TextSendMessage(text="基金比重錯誤!請重新輸入!")
               line_bot_api.reply_message(event.reply_token,[message1,message2])
            elif origin == None:
                message = TextSendMessage(text="基金統編錯誤!請重新輸入!")
                line_bot_api.reply_message(event.reply_token,[message1,message2])
            else:
                message = TextMessage(text="評估結果:")
                message1 = TextSendMessage(text=origin.output_portfolio())
                confirm_template_message = TemplateSendMessage(
                    alt_text='Confirm template',
                    template=ConfirmTemplate(
                        text='需要推薦基金組合嗎?',
                        actions=[MessageAction(label='是',text='Y'),MessageAction(label='否',text='N')]
                    )
                )
                    
                line_bot_api.push_message(user_id,message)
                line_bot_api.push_message(user_id,message1)
                line_bot_api.reply_message(event.reply_token,confirm_template_message)
                All_state[user_id] = 2

        except:
            text = "格式錯誤或是基金不存在\U0010005E!請再輸入一次，如果要停止評估，請輸入\"Q\"。" 
            message = TextMessage(text=text)
            line_bot_api.reply_message(event.reply_token,message)

    elif user_state == 2 and user_input == "N":
        text = "" + \
            "嗨\U0010005E\U0010005E\U0010005E!\n" + \
            "這是一個評估/推薦基金組合的聊天機器人\U0010005E。\n\n" + \
            "如果想要評估目前的基金組合，請輸入\"E\"。"
        message = TextMessage(text=text)
        line_bot_api.reply_message(event.reply_token,message)
        All_state[user_id] = 0

    elif user_state == 2:
        text = "" + \
            "請依照下列格式輸入資料:\n\n" + \
            "[轉換金額比例],[最多推薦的基金數量]\n\n" + \
            "範例:\n" + \
            "0.3,2\n\n" + \
            "**注意**\n" + \
            "轉換比例不能大於" + str(LIMIT_FUNDS_RATIO) + "\n" + \
            "推薦基金數量不能大於" +  str(LIMIT_FUNDS_NUM) 
        message = TextMessage(text=text)
        line_bot_api.reply_message(event.reply_token,message)
        All_state[user_id] = 3

    elif user_state == 3 and (user_input == "Q" or user_input == "q"):
        text = "" + \
            "嗨\U0010005E\U0010005E\U0010005E!\n" + \
            "這是一個評估/推薦基金組合的聊天機器人\U0010005E。\n\n" + \
            "如果想要評估目前的基金組合，請輸入\"E\"。"
        message = TextMessage(text=text)
        line_bot_api.reply_message(event.reply_token,message)
        All_state[user_id] = 0

    elif user_state == 3:
        try:
            temp1, temp2 = user_input.split(",",1)
            extra_ratio = float(temp1)
            recommend_num = int(temp2)

            #check 
            if extra_ratio > float(LIMIT_FUNDS_RATIO):
                message = TextSendMessage(text="轉換金額比例大於限制!請重新輸入!")
                line_bot_api.reply_message(event.reply_token,message)
            elif recommend_num > int(LIMIT_FUNDS_NUM):
                message = TextSendMessage(text="推薦基金數量大於限制!請重新輸入!")
                line_bot_api.reply_message(event.reply_token,message)
            else:
                All_selectFunds = json.load(open("selectFunds.txt"))
                All_selectFunds_weights = json.load(open("selectFund_weights.txt"))
                selectFunds = All_selectFunds[user_id]
                selectFund_weights = All_selectFunds_weights[user_id]

                # print(extra_ratio,recommend_num,selectFunds,selectFund_weights)

                #Optimize
                user_input = Input(extra_ratio,selectFunds,selectFund_weights,recommend_num)
                origin, result = recommend(user_input,line_bot_api,user_id)

                message = TextMessage(text="下列是基金組合的新舊對照\U0010005E:")
                message1 = TextSendMessage(text="舊:\n" + origin.output_portfolio())
                message2 = TextSendMessage(text="新:\n" + result.output_portfolio())
                message_last = TextMessage(text="如果還想要評估基金組合，請輸入\"E\"。")

                line_bot_api.push_message(user_id,message)
                line_bot_api.push_message(user_id,[message1,message2])                
                line_bot_api.reply_message(event.reply_token,message_last)
                All_state[user_id] = 0

        except:
            text = "格式錯誤\U0010005E!請再輸入一次，如果要停止推薦，請輸入\"Q\"。" 
            message = TextMessage(text=text)
            line_bot_api.reply_message(event.reply_token,message)


    else:
        message = TextMessage(text="\U0010005E\U0010005E\U0010005E")
        line_bot_api.reply_message(event.reply_token,message)
        All_state[user_id] = 0


    # print(All_state)
    json.dump(All_state,open("db.txt","w"))


if __name__ == "__main__":
    app.run()