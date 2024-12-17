from importlib.metadata import version; 
import sys

# For more detailed info
import platform
print(platform.python_version())
print(platform.python_implementation())
print(platform.python_compiler())
print(version('statsbombpy'))