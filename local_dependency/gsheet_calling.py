import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 以下代碼源自 https://developers.google.com/sheets/api/quickstart/python ，經過我們稍作更改
class GoogleAPIClient:
    SECRET_PATH = 'local_dependency/credentials/client_secret.json'
    CREDS_PATH = 'local_dependency/credentials/cred.json'
    
    def __init__(self, serviceName: str, version: str, scopes: list) -> None:
        self.creds = None
        # The file client_secret.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.CREDS_PATH):
            self.creds = Credentials.from_authorized_user_file(self.CREDS_PATH, scopes)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.SECRET_PATH, scopes)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.CREDS_PATH, 'w') as token:
                token.write(self.creds.to_json())

        self.googleAPIService = build(serviceName, version, credentials=self.creds)

'''
if __name__ == '__main__':
    googleSheetAPI = GoogleAPIClient(
        'sheets',
        'v4',
        ['https://www.googleapis.com/auth/spreadsheets'],
        )

    print(googleSheetAPI.googleAPIService)
'''


# ===========================以上是串接sheet API===========================
# ===========================以下是要發送的要求=============================


import pandas as pd
import numpy as np



class GoogleSheets(GoogleAPIClient):
    def __init__(self) -> None:
        # 呼叫 GoogleAPIClient.__init__()，並提供 serviceName, version, scope
        super().__init__(
            'sheets',
            'v4',
            ['https://www.googleapis.com/auth/spreadsheets'],
        )
        self.spreadsheetId='1PdPj3tWZRGp9F41OSy-vltdi_dA9RYwu50tAhZAG-SM'

    def clearWorksheet(self, range: str):
        self.googleAPIService.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheetId,
            range=range,
        ).execute()
        return 0
    
    def setWorksheet(self, range: str, df: pd.DataFrame):
        self.clearWorksheet(range)
        self.googleAPIService.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId,
            range=range,
            valueInputOption='USER_ENTERED',
            body={
                'majorDimension': 'ROWS',
                'values': df.T.reset_index().T.values.tolist()
            },
        ).execute()
        return 0

    #於底欄新增UserID及Function
    def appendWorksheet(self, values: list):
        request = self.googleAPIService.spreadsheets().values().append(
            spreadsheetId=self.spreadsheetId,
            range='工作表1',
            valueInputOption='USER_ENTERED',
            responseValueRenderOption='UNFORMATTED_VALUE',
            body={
                'majorDimension': 'COLUMNS',
                'values': values
            },
        )
        response = request.execute()
        return response
    
    #讀取所有UserID
    def getWorksheet(self):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=self.spreadsheetId,
            range='工作表1!A2:A',
        )
        response = request.execute()
        return response['values']
    
    #更新Function
    def updateWorksheet(self, ranges: int, values: list):
        request = self.googleAPIService.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId,
            range=f'工作表1!B{ranges}',
            valueInputOption='USER_ENTERED',
            responseValueRenderOption='UNFORMATTED_VALUE',
            body={
                'values': values
            },
        )
        response = request.execute()
        return response
    
    #讀取特定UserID的Current Function
    def getoneWorksheet(self, range: int):
        request = self.googleAPIService.spreadsheets().values().get(
            spreadsheetId=self.spreadsheetId,
            range=f'工作表1!B{range}',
        )
        response = request.execute()
        return response['values']
    


if __name__ == '__main__':
    myWorksheet = GoogleSheets()

    new_user = None
    user_id = 'Candy'
    results = np.array(myWorksheet.getWorksheet()).flatten()
    print(results)

    if user_id in results:
        print(f'UserID: {user_id} found')
        index = int(np.where(results == user_id)[0])
        print(f'Index is {index}')
        index = int(np.where(results == user_id)[0])+2
        print(f'Cell is {index}')
        message = [['TEST']]
        print(myWorksheet.updateWorksheet(index, message))

    else:
        print(f'UserID: {user_id} not found')
        message = 'TEST'
        data = [[user_id],[message]]
        print('creating new userID')
        print(myWorksheet.appendWorksheet(data))
