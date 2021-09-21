import time
import json
import os
import codecs

ScriptName = "Welcomer"
Description = "To welcome who came"
Creator = "E.NeLsOn"
Version = "1.0.3"
Website = "https://github.com/enels0n/StreamLabs-Scripts/tree/main/Welcomer"

configFile = "config.json"
settings = {}
path = ""

checkTime = 0
greetingTime = 0
userList = []
welcomeQueue = []
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
      "greetingFrequency": 5,
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
  global currentTime, checkTime, settings, userList, leaversList, greetingTime

  currentTime = time.time()
  
  if(settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"]):
    if(currentTime >= checkTime):
      checkTime = currentTime + 3

      currentUserList = Parent.GetViewerList()
      for x in range(len(currentUserList)):
        if (currentUserList[x] not in userList) and (currentUserList[x] not in leaversList):
          userList.append(currentUserList[x])
          welcomeQueue.append(currentUserList[x])
        else:
          if (currentUserList[x] not in userList) and (currentUserList[x] in leaversList):
            del leaversList[currentUserList[x]]
            userList.append(currentUserList[x])
            if (currentTime>=leaversList[currentUserList[x]]+(settings["absenceTime"]*60)):
              welcomeQueue.append(currentUserList[x])
      for x in range(len(userList)):
        if (userList[x] not in currentUserList):
          if userList[x] not in leaversList:
            leaversList[userList[x]] = currentTime
          del userList[x]

    if(currentTime >= greetingTime and welcomeQueue):
      greetingTime = currentTime + settings["greetingFrequency"]
      out = settings["welcomeMessage"].replace("$user", welcomeQueue[0])
      Parent.SendStreamMessage(out)
      del welcomeQueue[0]
  return
