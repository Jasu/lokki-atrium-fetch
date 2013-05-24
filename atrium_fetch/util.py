import sys
import os


def dieIf(condition, msg):
    if condition:
      sys.stderr.write(msg + "\n")
      sys.stderr.write("Nothing done.\n")
      sys.exit(1)


def expandEnvironmentVariables(string):
    env = os.environ.copy()
    keys = list(env.keys())
    # Sort by length, to make sure that $ASDF_ASDF is replaced with the value 
    # of $ASDF_ASDF, not $ASDF.
    keys.sort(key=lambda x: len(x), reverse=True)

    for key in keys:
        val = env[key] 
        key = "$" + key
        string = string.replace(key, val)

    return string
        
