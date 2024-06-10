import os
import time
from google.cloud.firestore_v1.base_query import FieldFilter
from commands import commands
from functions import addMessage, generateMessageWindow, login, nickColour, check_key, showCommandResult
from messages import getRoom, messages,  getUser
from console import console
from firestore import db

lastUpdateTime = 0


def clear(): return os.system('cls' if os.name == 'nt' else 'clear')


login()


def processMessage(message):
    if message.startswith('/'):
        if len(list(filter(lambda x: x.name == message.split(' ')[0][1:], commands))) != 1:
            unknownCommand = message.split(' ')[0]
            showCommandResult(f"[red]Unknown command:{unknownCommand}[/]")
            return False
        else:
            list(filter(lambda x: x.name == message.split(' ')[0][1:], commands))[
                0].run(message.split(' ')[1:])
            return False
    else:
        return True


messageData = []
startup = True

while True:
    while True:
        if int(time.time()) - lastUpdateTime >= 1:
            messageData = list(map(lambda x: x.to_dict(), db.collection(
                'messages').where(filter=FieldFilter('room', '==', getRoom())).order_by('timestamp').get()))

        if messages != messageData or startup:
            clear()
            console.print(generateMessageWindow(messageData))
            console.print(f"{nickColour(getUser())}: ", end='')
            messages = messageData.copy()
            lastUpdateTime = int(time.time())
            startup = False
        if check_key():
            break
    response = console.input()
    if processMessage(response):
        addMessage((getUser(), response), getRoom(), messages)
    console.print(f"{nickColour(getUser())}: ", end='')
