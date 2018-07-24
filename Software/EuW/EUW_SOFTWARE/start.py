import os
import time
from subprocess import Popen
import inspect
import os
import sys

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)


tmp_inp = raw_input("Simulation Mode? (0 = no, 1 = yes)")
if tmp_inp=='0':
    sim_mode=tmp_inp
else:
    sim_mode=tmp_inp
    
tmp_call = "j_EUW_JSON.py"


time.sleep(1)

Popen([sys.executable, os.path.join(get_script_dir(), tmp_call),sim_mode],creationflags=DETACHED_PROCESS).pid)

tmp_call = "s_EUW_SERIAL.py"


Popen([sys.executable, os.path.join(get_script_dir(), tmp_call),sim_mode],creationflags=DETACHED_PROCESS).pid)