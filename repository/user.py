from application import db
from domain.User import User
from engine.bkt import BKT

class UserRepo:

  def loadUser(userId: str) -> User:
    return UserRepo.toDomain(UserRepo._loadUser(userId))
  
  def toDomain(dbObj) -> User:
    user = User(dbObj['userId'], dbObj['modules'], {k: BKT(v) for k, v in dbObj['progress'].items()})
    return user
  
  def toDbObject(user):
    return {
      "userId": user.userId,
      "modules": user.modules,
      "progress": {k: v.P for k, v in user.progress.moduleProgress.items()}
    }

  def _loadUser(userId: str):
    return db.users.find_one({"userId": userId})
  
  def storeUser(user: User):
    dbObj = {
      "modules": user.modules,
      "progress": {k: v.P for k, v in user.progress.moduleProgress.items()}
    }

    db.users.update_one({"userId": user.userId}, {"$set" : dbObj}, upsert = True)

