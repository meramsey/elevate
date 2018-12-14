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


def elevate(show_console=True, graphical=True, restore_cwd=True):
    arg_prefix = "--_with-elevate-"
    if os.getuid() == 0:
        def filter_args(x, mode=True):
            comp = ["=" in x, x.startswith(arg_prefix)]
            return mode == all(comp)
        # tiny option parser to handle our special --_with-elevate-* opts
        elevate_opts = dict(map(
            lambda y: y.split("_")[1].split("="), filter(filter_args, sys.argv)
        ))
        newdir = elevate_opts.get("with-elevate-cwd", False)
        if newdir and restore_cwd:
            try:                      os.chdir(newdir)
            except FileNotFoundError: pass
            except Exception as e:    raise
        sys.argv = list(filter(lambda x: filter_args(x, mode=False), sys.argv))
        return

    args = [
        sys.executable,
        os.path.abspath(sys.argv[0]),
        arg_prefix + "cwd=" + os.getcwd() if restore_cwd else ""
    ] + sys.argv[1:]

    commands = []

    if graphical:
        if sys.platform.startswith("darwin"):
            commands.append([
                "osascript",
                "-e",
                "do shell script %s "
                "with administrator privileges "
                "without altering line endings"
                % quote_applescript(quote_shell(args))])

        if sys.platform.startswith("linux") and os.environ.get("DISPLAY"):
            commands.append(["pkexec"] + args)
            commands.append(["gksudo"] + args)
            commands.append(["kdesudo"] + args)

    commands.append(["sudo"] + args)

    print("execlp  ", args)

    for args in commands:
        try:
            os.execlp(args[0], *args)
        except OSError as e:
            if e.errno != errno.ENOENT or args[0] == "sudo":
                raise
