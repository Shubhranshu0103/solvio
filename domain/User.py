from enum import Enum
from typing import Dict, List
from engine.bkt import BKT
from repository.module import getModule

class ModuleType(Enum):
    MODULE = "MODULE"
    LESSON = "LESSON"

class Module:
  initialMastery = 0.6
  def __init__(self, name, type: ModuleType= ModuleType.MODULE, superModules: List[str] =[], subModules: List[str] = []) -> None:
    self.name = name
    self.type = type
    self.superModules = superModules
    self.subModules = subModules
    self.mastery = Module.initialMastery
  
  def updateMastery(self, updatedMastery):
    self.mastery = updatedMastery

class User:
  def __init__(self, userId, modules:List[str] = [], progress:Dict[str, BKT] = {}) -> None:
    self.progress = Progress()
    self.progress.moduleProgress = progress
    self.userId = userId
    self.modules = modules
    [self.initializeModule(module) for module in self.modules]

  def resetProgress(self, moduleName):
    self.progress = Progress()
    [self.initializeModule(module) for module in self.modules]
  
  def initializeModule(self, moduleName):
    self.progress.initializeModule(moduleName)


class Progress:
  def __init__(self) -> None:
    self.moduleProgress: Dict[str, BKT]= {} 
    self.modules: Dict[str, Module] = {} 

  def updateProgress(self, moduleName: str, correct: bool ):
    if moduleName not in self.modules:
      raise Exception(f"Module {moduleName} not started yet")

    module = self.modules[moduleName]
    currentMastery = self.moduleProgress[moduleName]
    currentMastery.update(correct)

    if module.type == ModuleType.MODULE:
      raise Exception("Can only update Lesson progress directly") 

    [self.updateParentMastery(parent, moduleName, currentMastery.P) for parent in module.superModules]

    module.mastery = currentMastery.P
    return None

  def initializeModule(self, moduleName: str):
    module = getModule(moduleName)
    if module['type'] != 'lesson':
      self.setModuleTree(module['name'], module['type'], module['submodules'])
      for subModule in module['submodules']:
        self.initializeModule(subModule)
    else:
      if moduleName in self.modules:
        self.modules[moduleName].type = module['type']
      else:
        self.modules[moduleName] = Module(module['name'], module['type'])
        self.moduleProgress[moduleName] = BKT(Module.initialMastery)
      # [self.initializeModule(subModule) for subModule in module['submodules']]
      
    

  def setModuleTree(self, moduleName, moduleType, subModulesName):
    if moduleName in self.modules:
      m = self.modules[moduleName]
      if m.subModules:
        [m.subModules.append(s) for s in  subModulesName]
      else:
        m.subModules = list(subModulesName)
      self.modules[moduleName].type = moduleType
    else:
      self.modules[moduleName] = Module(moduleName, moduleType, subModules=subModulesName)
    
    if moduleName not in self.moduleProgress:
      self.moduleProgress[moduleName] = BKT(Module.initialMastery)
    
    [self.setModuleParent(moduleName, subModuleName) for subModuleName in subModulesName]

  def setModuleParent(self, parent, module):
    if module in self.modules:
      self.modules[module].superModules.append(parent)
    else:
      self.modules[module] = Module(module, superModules=[parent])
    
    if module not in self.moduleProgress:
      self.moduleProgress[module] = BKT(Module.initialMastery)

  def updateParentMastery(self, module: str, subModule: str, newMastery):
    currentModule = self.modules[module]
    childModule = self.modules[subModule]

    noOfSubModules = len(currentModule.subModules)

    newCurrentMastery = (currentModule.mastery*(noOfSubModules) - childModule.mastery + newMastery)/noOfSubModules
    [self.updateParentMastery(parent, module, newCurrentMastery) for parent in currentModule.superModules]

    currentModule.mastery = newCurrentMastery
    self.moduleProgress[module].P =  newCurrentMastery
    return None
    




