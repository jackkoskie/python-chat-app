import time
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from rich import print
from rich.panel import Panel
from commands import commands
from functions import addMessage, generateMessageWindow, login, nickColour, check_key, showCommandResult
from messages import getRoom, messages, user, getUser
from console import console
from firestore import db
from firebase_admin import firestore

lastUpdateTime = 0

import os

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

login()

def processMessage(message):
  if message.startswith('/'):
    if len(list(filter(lambda x: x.name == message.split(' ')[0][1:], commands))) != 1:
      showCommandResult(f"[red]Unknown command: {message.split(' ')[0]}[/]")
      return False
    else:
      list(filter(lambda x: x.name == message.split(' ')[0][1:], commands))[0].run(message.split(' ')[1:])
      return False
  else:
    return True

messageData = []


while True:
  while True:
    if int(time.time()) - lastUpdateTime >= 1:
      messageData = list(map(lambda x: x.to_dict(), db.collection('messages').where(filter=FieldFilter('room', '==', getRoom())).get()))

    if messages != messageData:
      clear()
      console.print(generateMessageWindow(messageData))
      console.print(f"{nickColour(getUser())}: ", end='')
      messages = messageData.copy()
      lastUpdateTime = int(time.time())
    if check_key():
      break
  response = console.input()
  if processMessage(response):
    addMessage((getUser(), response), getRoom(), messages)
  console.print(f"{nickColour(getUser())}: ", end='')