import os
import time
from google.cloud.firestore_v1.base_query import FieldFilter
from commands import commands
from functions import addMessage, generateMessageWindow, login, nickColour, check_key, showCommandResult
from messages import getRoom, messages,  getUser
from console import console
from firestore import db
from rich.panel import Panel

lastUpdateTime = 0


def clear(): return os.system('cls' if os.name == 'nt' else 'clear')


clear()
signup = login()
# login()

if signup == True:
    clear()
    console.print(Panel("""This is a simple chat app that allows you to chat to your friends from the terminal!

After reading this message, you will be dropped into the \"general\" room. This room is a place where everyone can chat. Should you wish to have a more private conversation. You and a friend may join another room together by using the [b blue]/room \[room name][/] command. This will move you to the room of that name. Please note anyone may join any room if they know the name.

There are a few other commands that can be used to help you navigate around [i red]Costell-O-Gram[/]. All of these commands can be found through the [b blue]/help[/] command.

Happy chatting!""", title="Welcome to [i red]Costell-O-Gram[/]!"))
    input('Press ENTER to continue...')


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
