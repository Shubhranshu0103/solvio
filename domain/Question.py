from enum import Enum
from typing import List

from repository.module import getModule


class AnswerType(Enum):
  CONSTANT = "CONSTANT"

class Answer:
  def __init__(self, type: AnswerType, value) -> None:
    self.type = type
    self.value = value
  def evaluate(self, response):
    if self.type == AnswerType.CONSTANT:
      return self.value == response
    
    raise Exception("Answer type not supported")


class Question:
  def __init__(self, id: str, tags: List[str], statement, answer: Answer) -> None:
    if tags == []:
      raise Exception("At least 1 tag i required")
    
    if len([getModule(tag, {"type": "lesson"}) for tag in tags]) == 0:
      raise Exception("At least 1 lesson tag required")
    
    self.id = id
    self.tags = tags
    self.statement = statement
    self.answer = answer
  
  def getLessonTags(self):
    ans = [getModule(tag, {"type": "lesson"}, {"name": True, "_id": False}) for tag in self.tags]

    return [x['name'] for x in filter(lambda x: x is not None, ans)]