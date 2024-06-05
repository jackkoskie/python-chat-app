import time
from rich import print
from rich.panel import Panel
from commands import commands
from functions import addMessage, generateMessageWindow, login, nickColour, check_key
from messages import messages, user, getUser
from console import console
from firestore import db

lastUpdateTime = 0

import os

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

login()

def processMessage(message):
  if message.startswith('/'):
    if len(list(filter(lambda x: x.name == message.split(' ')[0][1:], commands))) != 1:
      addMessage(('SYSTEM', f"[red]Unknown command: {message.split(' ')[0]}[/]"), messages)
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
      messageData = list(map(lambda x: x.to_dict(), db.collection('messages').order_by('timestamp').get()))

    if messages != messageData:
      clear()
      console.print(generateMessageWindow(messageData))
      console.print(f"{nickColour(getUser())}: ", end='')
      messages = messageData.copy()
      lastUpdateTime = int(time.time())
    if check_key():
      input('test')
      break
  response = console.input()
  if processMessage(response):
    addMessage((getUser(), response), messages)
  console.print(f"{nickColour(getUser())}: ", end='')