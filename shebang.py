#!/bin/bash
import platform
import sys
import shutil
"exec" "pyenv" "exec" "python" "$0" "$@"
# the rest of your Python script can be written below

print("hello")
print("Python version")
print(sys.version)
print("Version info.")
print (sys.version_info)

print(platform.python_version())
print("which python = ")
print(shutil.which("python"))
