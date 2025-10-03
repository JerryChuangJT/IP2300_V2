from datetime import datetime
import os

def CreateLogPath(TestCategory):
    Dir = "./TestLog/"
    if not os.path.exists(Dir):   os.makedirs(Dir)
    else:   pass

    formatted_time = datetime.now().strftime("%Y%m%d_%H%M_")
    LogFilePath = Dir + formatted_time + "ConsoleLog_"
    for data in TestCategory.split("-"):
        LogFilePath = LogFilePath + data
    LogFilePath = LogFilePath + ".log"
    return LogFilePath

def Get_LogDir(LogPath):
    LogDir = ""
    LogPath_Split = LogPath.split("/")
    for data in LogPath_Split[:-1]:
        LogDir = LogDir + data + "/" 
    return LogDir
#----------------------------------------------------------------------------
def WriteLog(LogPath, Message, PrintMessage=False):
    FileNameTime = datetime.today().strftime("%Y%m%d")
    LogPath = LogPath + "_" + FileNameTime + ".log"
    
    # Create Dir if it is not exist
    LogDir = Get_LogDir(LogPath=LogPath)
    if not os.path.isdir(LogDir):
        os.makedirs(LogDir)
    
    # Create Log File if it is not exist
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")            # datetime format "YYYY-mm-dd HH:MM:SS"
    if os.path.exists(LogPath) != True:
        with open(LogPath, "w") as file1: 
            file1.write(f"{now} : Create file {LogPath} ....\n")    # Create log file

    # Write Message to Log FIle & Pring Message
    now = datetime.today().strftime("%Y-%m-%d %H:%M:%S")            # datetime format "YYYY-mm-dd HH:MM:SS"
    with open(LogPath, "a") as file: 
        file.write(f"{now} : {Message}\n")                            # Append the timestamp with log message.

    # Print Message
    if PrintMessage:
        print(f"{now} : {Message}\n")


