import os

import subprocess
import traceback

### Function for Get Current Time.
def Create_Folder(folder_path:str=None):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

### Function for Renaming File.
def Rename_file(old_file_path, new_file_path):
    if not os.path.exists(old_file_path):
        return
    if os.path.exists(new_file_path):
        os.remove(new_file_path)
    os.rename(old_file_path, new_file_path)
### ======================================================================================================
### Private Function for Communicating with Device. ###
### Function for running command via subprocess
### ADB command need Subprocess to execute it.
def Run_Subprocess(command:str)->str:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        return ["PASS", result.stdout + result.stderr]

    except subprocess.CalledProcessError as e:
        return ["FAIL", str(e)]
    
    except Exception as e:
        return ["FAIL", traceback.format_exc()]
    
