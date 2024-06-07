from functions import showCommandResult
from messages import getRoom, setRoom


class Command:
    def __init__(self, name, description, function, args="",) -> None:
        self.name = name
        self.description = description
        self.args = args
        self.function = function

    def run(self, args):
        self.function(args)

    def help(self):
        args = f"[i]{self.args}[/]" if self.args != "" else ""

        return f"""[b blue]/{self.name}[/] {args}

        {self.description}"""


def runHelp(args):
    if (len(args) > 0):
        command = list(filter(lambda x: x.name == args[0], commands))[0]

        return showCommandResult(command.help())
    else:
        data = ['\n[b u]List of Commands[/]',
                '[i]Run [b blue]/help \[command name][/] to get more information about a command.[/]\n']

        for command in commands:
            data.append(f'[b blue]/{command.name}[/] - {command.description}')

        data.append('\n')
        # return addMessage(('SYSTEM', '\n'.join(data)), messages)
        return showCommandResult('\n'.join(data))


def runExit(args):
    showCommandResult('Goodbye :)')
    return exit()


def runRoom(args):
    if len(args) == 0:
        return showCommandResult(f'[b blue]Current room: {getRoom()}[/]')

    setRoom(args[0])
    return showCommandResult(f'[b blue]Room set to: {getRoom()}[/]')


commands = [
    Command('help', 'Shows this help page.', runHelp),
    Command('exit', 'Exits the program.', runExit),
    Command('room', 'Display the current room or set join a new room.',
            runRoom, '[room name]')
]
