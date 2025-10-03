#!/system/bin/sh
# Create Time : 2025/07/17
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Ping/BackupLog_Ping.sh "Test1" 
#-----------------------------------------------------------------------------------
# Function : 
#       1. Create a backup folder for Ping log files.
#       2. Move Ping log files from the original log folder to the backup folder.
#       3. Reset temp_StartLine file to "0".
#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : ping test nick name.
#           ex: "Test1".
#-----------------------------------------------------------------------------------
Create_Folder() {
    ### Get first parameter for folder path.
    folder_path="$1";

    ### Check folder is exist or not.
    ### make dir
    if [ ! -d "$folder_path" ]; then
        mkdir -p "$folder_path";
    fi
};
#-----------------------------------------------------------------------------------
Backup_LogDir="/storage/emulated/0/Documents/Log_Backup/Ping"
LogDir="/storage/emulated/0/Documents/Log/Ping"
Create_Folder "$Backup_LogDir"

test_name=$1

Ping_ScheduleLog="${LogDir}/${test_name}_PingScheduleLog.log"
Ping_Log="${LogDir}/${test_name}_ping.log"
Ping_AddTimeLog="${LogDir}/${test_name}_ping_addtime.log"
Ping_FailSummary="${LogDir}/${test_name}_ping_failsummary.log"
Ping_RateLog="${LogDir}/${test_name}_ping_rate.log"
temp_StartLine="/storage/emulated/0/Documents/Ping/${test_name}_start_line"

if [ -f "$Ping_ScheduleLog" ]; then
    mv "$Ping_ScheduleLog" "$Backup_LogDir/${test_name}_PingScheduleLog.log";
fi

if [ -f "$Ping_Log" ]; then
    cat "$Ping_Log" > "$Backup_LogDir/${test_name}_ping.log" && > "$Ping_Log";
fi

if [ -f "$Ping_AddTimeLog" ]; then
    mv "$Ping_AddTimeLog" "$Backup_LogDir/${test_name}_ping_addtime.log";
fi  

if [ -f "$Ping_FailSummary" ]; then
    mv "$Ping_FailSummary" "$Backup_LogDir/${test_name}_ping_failsummary.log";
fi

if [ -f "$Ping_RateLog" ]; then
    mv "$Ping_RateLog" "$Backup_LogDir/${test_name}_ping_rate.log";
fi

echo "0" > $temp_StartLine;
