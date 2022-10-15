import requests
import json

def get_answer(message_text):
    
    url = "https://jolie.azurewebsites.net/qnamaker/knowledgebases/81af20c3-487c-44c3-81b0-26ef882c97f4/generateAnswer"

    # 發送request到QnAMaker Endpoint要答案
    response = requests.post(
                   url,
                   json.dumps({'question': message_text}),
                   headers={
                       'Content-Type': 'application/json',
                       'Authorization': 'EndpointKey 2ec50282-714b-4d18-9b45-d2cfe3b3ab85'
                   }
               )

    data = response.json()

    try: 
        #我們使用免費service可能會超過限制（一秒可以發的request數）
        if "error" in data:
            return data["error"]["message"]
        #沒找到適合答案的話，回傳無搜尋結果
        elif data['answers'][0]['answer'] == "No good match found in KB.":
            answer = "無搜尋結果"
            return answer
        #這裡我們預設取第一個答案
        answer = data['answers'][0]['answer']

        return answer

    except Exception:

        return "Error occurs when finding answer"

if __name__ == "__main__":
    #測試
    question = '柬埔寨'
    answer = get_answer(question)
    print(answer)