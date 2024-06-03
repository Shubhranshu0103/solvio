from types import SimpleNamespace
from typing import Dict, List
from application import app, db
from flask import jsonify, Response, request
from bson.json_util import dumps
from domain.Question import Question
from domain.User import User
from repository.module import getModule, getModuleTree
from repository.question import QuestionRepo
from repository.user import UserRepo
import jsonpickle

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/modules')
def getModules():
    y = [m for m in db.modules.find({}, {"_id":False})]
    name = "Properties of Integers"
    # m = getModule(name, projection={"_id": False})
    moduleTree = getModuleTree(name)
    return jsonify(moduleTree)
@app.get('/lessons')
def getArticles():
    mname = "Properties of Integers"
    username = "shubhranshu"
    threshold = 0.7
    user:User = UserRepo.loadUser(username)
    progress: Dict[str, float] = UserRepo.toDbObject(user)['progress']
    modules = [m for m in getModuleTree(mname) if m['type'] == 'lesson']
    lessonsRequireLearning = [m for m  in modules if progress[m['name']] < threshold]
    return jsonify(lessonsRequireLearning)

@app.post('/progress/reset')
def resetProgress():
    mname = "Properties of Integers"
    username = "shubhranshu"
    user:User = UserRepo.loadUser(username)
    user.resetProgress(mname)
    UserRepo.storeUser(user)

    return f"Progress reset for user {username}'s module {mname}"


@app.route('/debug/progress/<userId>')
def getUserProgress(userId):
    user:User = UserRepo.loadUser(userId)
    return jsonify(UserRepo.toDbObject(user))

@app.post('/user/<userId>')
def createUser(userId):
    UserRepo.storeUser(User(userId))
    return f'User {userId} created', 200

@app.route('/module/start/', methods=["POST"])
def startModule():
    data = getData(['userId', 'moduleName'], request.get_json())
    user: User = UserRepo.loadUser(data.userId)
    user.initializeModule(data.moduleName)
    user.modules.append(data.moduleName)
    UserRepo.storeUser(user)
    return f"Module {data.moduleName} started for user {data.userId}"

@app.put('/mastery')
def updateMastery():
    fields = ['userId', 'qId', 'response']
    data = getData(fields, request.get_json())
    user: User = UserRepo.loadUser(data.userId)
    question = QuestionRepo.getQuestionById(data.qId)
    correct = question.answer.evaluate(data.response)
    [user.progress.updateProgress(lessonTag, correct) for lessonTag in question.getLessonTags()]
    UserRepo.storeUser(user)

    return f"Mastery Updated for user {data.userId}"

@app.get('/questions')
def getQuestions():
    fields = ['moduleName', 'lessons']
    data = getData(fields, request.get_json())
    
    questions: List[Question] = [QuestionRepo.toDbObject(q) for q in QuestionRepo.loadQuestions(data.moduleName)]
    res = []
    if data.lessons != []:
        for lesson in data.lessons:
            res += [q for q in questions if lesson in q['tags']]
    else:
        res = questions

    return jsonify(res)

def getData(fields, reqBody):
    if not reqBody or any([key not in reqBody for key in fields]):
        return jsonify({'error': "Bad Request", 'message': f"one of the fields in {fields} not provided"})
    data = SimpleNamespace()
    [setattr(data, key, reqBody[key]) for key in fields]
    return data
