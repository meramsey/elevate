#! /usr/bin/env python

import os, sys
from elevate import elevate


def is_root():
    if sys.platform.startswith("win"):
        from ctypes import windll
        return bool(windll.shell32.IsUserAnAdmin())
    else:
        return os.getuid() == 0


print("before: ", os.getcwd())
print("before: ", is_root())

elevate()

print("after:  ", os.getcwd())
print("after:  ", is_root())
print(sys.argv)
print(open(sys.argv[1], "r").readline())

# should print: False True True and a line
