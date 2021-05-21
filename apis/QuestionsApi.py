import random

from starlette import status

import model
from utils.jsonReturnUtils import returnQuestion, returnAnswer


class QuestionApi:
    def __init__(self, client):
        self.client = client

    def loadQuestion(self):
        questions_db = self.client.questions['questions']
        number = questions_db.count_documents({})
        questions = questions_db.find()
        return returnQuestion(question=questions[random.randint(0, number)], statusCode=status.HTTP_200_OK)

    def addQuestion(self, question: model.Question):
        questions_db = self.client.questions['questions']
        questions_db.insert_one(question)
        return question

    def postAnswer(self, answer: model.Answer):
        answer_db = self.client.questions['answers']
        new = answer_db.insert_one(answer)
        return returnAnswer(statusCode=status.HTTP_200_OK, answer=new)
