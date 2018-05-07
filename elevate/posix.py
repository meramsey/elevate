import errno
import os
import sys
try:
    from shlex import quote
except ImportError:
    from pipes import quote


def quote_shell(args):
    return " ".join(quote(arg) for arg in args)


def quote_applescript(string):
    charmap = {
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
        "\"": "\\\"",
        "\\": "\\\\",
    }
    return '"%s"' % "".join(charmap.get(char, char) for char in string)


def elevate():
    if os.getuid() != 0:
        args = [sys.executable] + sys.argv
        commands = []

        if sys.platform.startswith("darwin"):
            commands.append([
                "osascript",
                "-e",
                "do shell script %s with administrator privileges"
                % quote_applescript(quote_shell(args))])

        if sys.platform.startswith("linux") and os.environ.get("DISPLAY"):
            commands.append(["gksudo"] + args)
            commands.append(["kdesudo"] + args)

        commands.append(["sudo"] + args)

        for args in commands:
            try:
                os.execlp(args[0], *args)
            except OSError as e:
                if e.errno != errno.ENOENT or args[0] == "sudo":
                    raise
