import time
import json
import os
import codecs

ScriptName = "Welcomer"
Description = "To welcome who came"
Creator = "E.NeLsOn"
Version = "1.0.1"
Website = "http://google.com/"

configFile = "config.json"
settings = {}
path = ""

checkTime = 0
userList = []
leaversList = {}
currentTime = 0

def Init():
  global settings, path
  
  path = os.path.dirname(__file__)
  try:
    with codecs.open(os.path.join(path, configFile), encoding='utf-8-sig', mode='r') as file:
      settings = json.load(file, encoding='utf-8-sig')
  except:
    settings = {
      "liveOnly": True,
      "checkInterval": 30,
      "absenceTime": 60,
      "welcomeMessage": "Привет, @$user"
    }
  return

def Execute(data):
  pass
  
def ReloadSettings(jsonData):
  Init()
  return

def Tick():
  global currentTime, checkTime, settings, userList, leaversList

  currentTime = time.time()
  
  if(settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"]):
    if(currentTime >= checkTime):
      checkTime = currentTime + settings["checkInterval"]

      currentUserList = Parent.GetViewerList()
      for x in range(len(currentUserList)):
        if (currentUserList[x] not in userList) and not (currentUserList[x] in leaversList):
          userList.append(currentUserList[x])
          out = settings["welcomeMessage"].replace("$user", currentUserList[x])
          Parent.SendStreamMessage(out)
        else:
          if currentUserList[x] in leaversList:
            if (currentTime>=leaversList[currentUserList[x]]+(settings["absenceTime"]*60)):
              del leaversList[currentUserList[x]]
              userList.append(currentUserList[x])
              out = settings["welcomeMessage"].replace("$user", currentUserList[x])
              Parent.SendStreamMessage(out)

      for x in range(len(userList)):
        if (userList[x] not in currentUserList):
          if userList[x] not in leaversList:
            leaversList[userList[x]] = currentTime
          del userList[x]
  return
