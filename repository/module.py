from typing import List
from application import db

def getModule(moduleName: str, filter={}, projection={}):
  return db.modules.find_one({"name": moduleName, **filter},projection)

def getModuleTree(moduleName):
  tree = []
  def _getTree(mName, acc):
    module = getModule(mName, projection={"_id":False})
    acc.append(module)

    if 'submodules' in module:
      [_getTree(sm, acc) for sm in module['submodules']]
  
  _getTree(moduleName, tree)

  return tree


  

