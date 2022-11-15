#載入LineBot所需要的模組
from socket import create_server
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import json
import sys
import os
import numpy as np

from local_dependency import CustomQA
from local_dependency.gsheet_calling import GoogleSheets

channel_access_token = open('local_dependency/credentials/line_bot_channel_access_token.json', 'r').read()
channel_secret = open('local_dependency/credentials/line_bot_channel_secret.json', 'r').read()

app = Flask(__name__)
 
# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi(channel_access_token)
# 必須放上自己的Channel Secret
handler = WebhookHandler(channel_secret)

#line_bot_api.push_message('Uf0c92982f71d4fbaf5a3180683819e67', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
 
  
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
 
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
 
    return 'OK'

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(FollowEvent)
def handle_follow(event):
    print("New follower")
    welcome_message = json.load(x:=open('flex_message/functions.json','r',encoding= 'utf-8'))
    flex_message_functions = FlexSendMessage(
        alt_text='Jolie歡迎你!',
        contents= welcome_message
        )
    line_bot_api.reply_message(event.reply_token,flex_message_functions)
    x.close()


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    user_id = event.source.user_id
    
    #獲取User_id在gsheet上的index
    myWorksheet = GoogleSheets()
    results = np.array(myWorksheet.getWorksheet()).flatten()
    status = None

    new_user = None
    if user_id in results:
        print(f'UserID: {user_id} found')
        index = int(np.where(results == user_id)[0])+2   #type_integer
    else:
        data = [[user_id]]
        postback = myWorksheet.appendWorksheet(data)
        index = postback['updates']['updatedRange'].replace("\'工作表1\'!A", "")
        print(f'index is {index}')
        print(f'UserID: {user_id} not found')

         
    #使用者選擇功能
    if message == '網站指引':
        status = [['網站指引']]
        myWorksheet.updateWorksheet(index, status)
        flex_message_website = FlexSendMessage(
            alt_text='網站指引列表',
            contents= json.load(open('flex_message/website.json','r',encoding= 'utf-8'))
            )
        line_bot_api.reply_message(event.reply_token,flex_message_website)

    elif message == '功能表':
        status = [['功能表']]
        myWorksheet.updateWorksheet(index, status)
        
        function_message = json.load(x:=open('flex_message/functions.json','r',encoding= 'utf-8'))
        flex_message_functions = FlexSendMessage(
            alt_text='功能表',
            contents= function_message
            )
        line_bot_api.reply_message(event.reply_token,flex_message_functions)
        x.close()
    
    elif message == '畢業聯展':
        status = [['畢業聯展']]
        myWorksheet.updateWorksheet(index, status)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='感謝您來參觀畢業聯展，這是Line Bot Jolie的簡報電子檔! https://drive.google.com/file/d/1Gg8DGR7XXQMbKC7NLhmRisVM-PyrtRqo/view?usp=sharing'))
    
    elif message == '常見問題':

        #Line訊息投放
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='你想問什麼問題呢?',
                quick_reply=QuickReply(items=[
                    QuickReplyButton(action=MessageAction(label="Julie", text="Julie是誰?")),
                    QuickReplyButton(action=MessageAction(label="學期成績查詢", text="學期成績要在哪裡看?")),
                    QuickReplyButton(action=MessageAction(label="輔系繳費", text="輔系什麼時候要繳費?")),
                    QuickReplyButton(action=MessageAction(label="選課相關", text="什麼時候可以選課?")),
                    QuickReplyButton(action=MessageAction(label="英文系課表", text="英文系課表在哪裡?")),
                    QuickReplyButton(action=MessageAction(label="壓力大大Q_Q", text="好累喔，壓力好大QQ")),
                    QuickReplyButton(action=MessageAction(label="LOD", text="LOD要怎麼申請?")),
                    QuickReplyButton(action=MessageAction(label="學分最低限制", text="每學期最低要修幾學分?")),
                    QuickReplyButton(action=MessageAction(label="語言(英檢)證明", text="我要在哪裡上傳英檢證明?")),
                    QuickReplyButton(action=MessageAction(label="如何請假", text="我要怎麼請假呢?")),
                ])))
        status = [['等待常見問題']]
        myWorksheet.updateWorksheet(index, status)

    #possibly邏輯問題
    elif myWorksheet.getoneWorksheet(index)[0][0] == '等待常見問題':
        status = [['無']]
        answer = CustomQA.get_answer(message)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(answer))
        myWorksheet.updateWorksheet(index, status)

    else:        
        line_bot_api.reply_message(event.reply_token,TextSendMessage('您目前沒有選擇功能或是你問我的問題太難了，所以Jolie沒有辦法回覆你，如果你有事情想跟Jolie分享的話，歡迎去找Julie喔!'))


@handler.add(PostbackEvent)
def handle_postback(event):
    postback = event.postback.data
    
    if postback == 'building_code':
        bc_message = json.load(x:=open('flex_message/building_code.json','r',encoding= 'utf-8'))
        flex_message_bc = FlexSendMessage(
            alt_text='教室代號說明',
            contents= bc_message
            )
        line_bot_api.reply_message(event.reply_token,flex_message_bc)
        x.close()
        
  
#主程式
#import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)