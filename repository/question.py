from application import db
from domain.Question import Answer, AnswerType, Question
from repository.module import getModule

class QuestionRepo:
  def loadQuestions(tag):
    dbRes = [res for res in db.questions.find({"tags" : {"$in" : [tag]}})]
    return [QuestionRepo.toDomain(q) for q in dbRes]

  def toDomain(dbObj) -> Question:
    answerType = dbObj['answer']['type'].upper()
    try:
      answerType = AnswerType[answerType]
    except KeyError:
      raise Exception(f"Invalid Answertype {answerType}")

    question = Question(dbObj['qId'], dbObj['tags'], dbObj['statement'], Answer(answerType, dbObj['answer']['value']))
    return question
  
  def toDbObject(question: Question):
    return {
      "id" : question.id,
      "tags" : question.tags,
      "statement" : question.statement
    }
  
  # def getQuestion(tag):
  #   tag = getModule(tag, {"type": "lesson"})
  #   if not tag:
  #     raise Exception(f"Need lesson tag but got {tag}")

  
  def getQuestionById(qId) -> Question:
    return QuestionRepo.toDomain(db.questions.find_one({"qId": qId}))