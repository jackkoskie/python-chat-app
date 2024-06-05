user = ""

def setUser(name):
  global user
  user = name

def getUser():
  return user

messages = []

room = 'general'

def getRoom():
  return room

def setRoom(r):
  global room
  room = r