import requests
import json
from linebot import LineBotApi, WebhookHandler

def rich_menu_regis():
  #設定互動區塊 & 新增rich menu
  headers = {
      'Authorization':'Bearer hlyyv5+jqI8UTNZb5k0SS9StbdPBIt32l/O6cVEKIpZ2MmuLvi36JCX906rnbRet3gjmSdq2AMV5NLttsrdIMWVM41v0CyRKJMrdR+a0eqZtqYEqgY7JvDty1lrWWNAXwc6QEhmM4kzVh/ETzTIoXgdB04t89/1O/w1cDnyilFU=',
      'Content-Type':'application/json'
      }

  body = {
      'size': {'width': 1200, 'height': 405},    # 設定尺寸
      'selected': 'true',                        # 預設是否顯示
      'name': 'functions',                       # 選單名稱
      'chatBarText': 'functions',                # 選單在 LINE 顯示的標題
      'areas':[                                  # 選單內容
          {
            'bounds': {'x': 0, 'y': 0, 'width': 400, 'height': 405}, # 選單位置與大小
            'action': {'type': 'message', 'text': '常見問題'}                # 點擊後傳送文字
          },
          {
            'bounds': {'x': 400, 'y': 0, 'width': 400, 'height': 405},
            'action': {'type': 'message', 'text': '網站指引'}
          },
          {
            'bounds': {'x': 800, 'y': 0, 'width':400, 'height': 405},
            'action': {'type': 'uri', 'label': 'feedback', 'uri': 'https://docs.google.com/forms/d/e/1FAIpQLSd6PPj9mroWQqaarWBX3LiAtUVTTkr3qKBiow579RKnJqneng/viewform?usp=sf_link?openExternalBrowser=1'}
          }   
      ]
    }

  req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                        headers=headers,data=json.dumps(body).encode('utf-8'))

  print(req.text)
  
def rich_menu_pic():
  #設定圖片
  line_bot_api = LineBotApi('hlyyv5+jqI8UTNZb5k0SS9StbdPBIt32l/O6cVEKIpZ2MmuLvi36JCX906rnbRet3gjmSdq2AMV5NLttsrdIMWVM41v0CyRKJMrdR+a0eqZtqYEqgY7JvDty1lrWWNAXwc6QEhmM4kzVh/ETzTIoXgdB04t89/1O/w1cDnyilFU=')

  with open('X:/Others/Python/LineBot_Jolie/rich_menu_manual_deployment/rich_menu.png', 'rb') as f:
      line_bot_api.set_rich_menu_image('richmenu-160d43a09afc088545a0aa3040832d0f', 'image/jpeg', f)



def rich_menu_activate():
  #於LineBot顯示圖文選單

  headers = {
      'Authorization':'Bearer hlyyv5+jqI8UTNZb5k0SS9StbdPBIt32l/O6cVEKIpZ2MmuLvi36JCX906rnbRet3gjmSdq2AMV5NLttsrdIMWVM41v0CyRKJMrdR+a0eqZtqYEqgY7JvDty1lrWWNAXwc6QEhmM4kzVh/ETzTIoXgdB04t89/1O/w1cDnyilFU=',
      'Content-Type':'application/json'
      }
  req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/richmenu-160d43a09afc088545a0aa3040832d0f', headers=headers)

  print(req.text)


def rich_menu_list():
  #查看所有rich menu
  line_bot_api = LineBotApi('hlyyv5+jqI8UTNZb5k0SS9StbdPBIt32l/O6cVEKIpZ2MmuLvi36JCX906rnbRet3gjmSdq2AMV5NLttsrdIMWVM41v0CyRKJMrdR+a0eqZtqYEqgY7JvDty1lrWWNAXwc6QEhmM4kzVh/ETzTIoXgdB04t89/1O/w1cDnyilFU=')

  rich_menu_list = line_bot_api.get_rich_menu_list()

  for rich_menu in rich_menu_list:
    print(rich_menu.rich_menu_id)
  

def rich_menu_delete():
  #刪除rich menu
  line_bot_api = LineBotApi('hlyyv5+jqI8UTNZb5k0SS9StbdPBIt32l/O6cVEKIpZ2MmuLvi36JCX906rnbRet3gjmSdq2AMV5NLttsrdIMWVM41v0CyRKJMrdR+a0eqZtqYEqgY7JvDty1lrWWNAXwc6QEhmM4kzVh/ETzTIoXgdB04t89/1O/w1cDnyilFU=')
  line_bot_api.delete_rich_menu('richmenu-2e9788915cc6b6215cf20ab00381e119')
  


if __name__ == '__main__':
  #rich_menu_regis()
  #rich_menu_pic()
  rich_menu_activate()  
  #rich_menu_list()
  #rich_menu_delete()

