from rich.panel import Panel
from console import console
from rich import print
from messages import setUser
from firestore import db
from argon2 import PasswordHasher
import os
from messages import getUser, getRoom
from time import time
import select
import sys

screenSize = 20


def clear(): return os.system('cls' if os.name == 'nt' else 'clear')


ph = PasswordHasher()

colours = ['grey37', 'red', 'green', 'yellow',
           'blue', 'magenta', 'cyan', 'dark_magenta']


def nickColour(nickname):
    if nickname == 'SYSTEM':
        return 'SYSTEM'

    value = 0
    for char in nickname:
        value += ord(char)

    return f'[{colours[value % len(colours)]}]{nickname}[/]'


def generateMessageWindow(messages):
    data = []

    for message in messages[-screenSize:]:
        if message['author'] == 'SYSTEM':
            data.append(f'[italic]{message["text"]}[/]')
        else:
            data.append(f"{nickColour(message['author'])}: {message['text']}")

    if len(messages) < screenSize:
        for _ in range(screenSize - len(messages)):
            data.append("")

    return Panel('\n'.join(data), title=f"[italic red]My Chat App[/] - {getRoom()}")


def clear_line(n=1):
    LINE_UP = '\033[1A'
    LINE_CLEAR = '\x1b[2K'
    for _ in range(n):
        print(LINE_UP, end=LINE_CLEAR)


def login():
    print(
        Panel(
            """This is a chatroom style chat app allowing you to stay connected with your friends.

  Please enter a nickname to sign in / sign up.""",
            title="Welcome to [italic red]My Chat App[/]!"))

    nickname = input('Nickname: ').lower()

    if db.collection('users').document(nickname).get().exists:
        incorrect = False
        while True:
            clear()
            print(
                Panel(f"""Welcome back, {nickColour(nickname)}!

      Please enter your password...""",
                      title=f"Welcome back, {nickColour(nickname)}!"))

            if incorrect:
                print("[red]Incorrect password.[/] Please try again")
            else:
                print()
            password = console.input("Password: ")

            try:
                ph.verify(
                    db.collection('users').document(nickname).get().to_dict()
                    ['password'], password)

                # salt = os.urandom(32)
                # hashedPassword = hashlib

                setUser(nickname)
                print("Log in successful!")
                input("Press ENTER to continue...")
                break
            except:
                incorrect = True
                continue
    else:
        incorrect = False
        while True:
            clear()
            print(
                Panel(f"""Welcome, {nickColour(nickname)}!

      Please chose a password...""",
                      title=f"Welcome, {nickColour(nickname)}!"))
            if incorrect:
                print("[red]Passwords do not match.[/] Please try again")
            else:
                print()
            password = console.input("Password: ")
            password2 = console.input("Confirm password: ")

            if password == password2:
                db.collection('users').document(nickname).create(
                    {"password": ph.hash(password)})
                setUser(nickname)
                print("Sign up successful!")
                input("Press ENTER to continue...")
                break
            else:
                incorrect = True
                continue


def addMessage(message, room, messages):
    for line in message[1].splitlines():
        if message[0] == getUser():
            db.collection('messages').add(document_data={
                "author": getUser(), "text": line, "timestamp": int(time()), 'room': room})
        messages.append({'author': nickColour(message[0]), 'text': line})
    clear()
    console.print(generateMessageWindow(messages))


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
  screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()


def check_key():
    return sys.stdin in select.select([sys.stdin], [], [], 0)[0]


def showCommandResult(message):
    console.print('\n', message)
    input('Press ENTER to continue...')
    clear()
    console.print(generateMessageWindow(list(map(
        lambda x: x.to_dict(), db.collection('messages').order_by('timestamp').get()))))

# import os

# # Windows
# if os.name == 'nt':
#     import msvcrt

# # Posix (Linux, OS X)
# else:
#     import sys
#     import termios
#     import atexit
#     from select import select


# class KBHit:

#     def __init__(self):
#         '''Creates a KBHit object that you can call to do various keyboard things.
#         '''

#         if os.name == 'nt':
#             pass

#         else:

#             # Save the terminal settings
#             self.fd = sys.stdin.fileno()
#             self.new_term = termios.tcgetattr(self.fd)
#             self.old_term = termios.tcgetattr(self.fd)

#             # New terminal setting unbuffered
#             self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
#             termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

#             # Support normal-terminal reset at exit
#             atexit.register(self.set_normal_term)


#     def set_normal_term(self):
#         ''' Resets to normal terminal.  On Windows this is a no-op.
#         '''

#         if os.name == 'nt':
#             pass

#         else:
#             termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


#     def getch(self):
#         ''' Returns a keyboard character after kbhit() has been called.
#             Should not be called in the same program as getarrow().
#         '''

#         s = ''

#         if os.name == 'nt':
#             return msvcrt.getch().decode('utf-8')

#         else:
#             return sys.stdin.read(1)


#     def getarrow(self):
#         ''' Returns an arrow-key code after kbhit() has been called. Codes are
#         0 : up
#         1 : right
#         2 : down
#         3 : left
#         Should not be called in the same program as getch().
#         '''

#         if os.name == 'nt':
#             msvcrt.getch() # skip 0xE0
#             c = msvcrt.getch()
#             vals = [72, 77, 80, 75]

#         else:
#             c = sys.stdin.read(3)[2]
#             vals = [65, 67, 66, 68]

#         return vals.index(ord(c.decode('utf-8')))


#     def kbhit(self):
#         ''' Returns True if keyboard character was hit, False otherwise.
#         '''
#         if os.name == 'nt':
#             return msvcrt.kbhit()

#         else:
#             dr,dw,de = select([sys.stdin], [], [], 0)
#             return dr != []
