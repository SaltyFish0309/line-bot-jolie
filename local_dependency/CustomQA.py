from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

QA_key = open('local_dependency/credentials/QA_credential.json', 'r').read()

endpoint = "https://line-bot-jolie.cognitiveservices.azure.com/"
credential = AzureKeyCredential(QA_key)
knowledge_base_project = "line-bot-jolie"
deployment = "production"

def get_answer(question: str):
    client = QuestionAnsweringClient(endpoint, credential)
    with client:
        question = question
        output = client.get_answers(
            question = question,
            project_name=knowledge_base_project,
            deployment_name=deployment
        )
    # print("連接至Azure QuestionAnswering服務")
    print("Q: {}".format(question))
    print("A: {}".format(output.answers[0].answer))
    print("Confidence Score: {}".format(output.answers[0].confidence)) # add this line 
    return output.answers[0].answer

if __name__ == '__main__':
    question = '選課須知'
    print(get_answer(question))