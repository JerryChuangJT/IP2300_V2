#!/system/bin/sh
# Create Time : 2025/07/29
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Wifi/BackupLog_Wifi.sh

#-----------------------------------------------------------------------------------
# Function : 
#       1. Create a backup folder for Wifi log files.
#       2. Move Wifi log files from the original log folder to the backup folder

#-----------------------------------------------------------------------------------
# Variables : 

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
Backup_LogDir="/storage/emulated/0/Documents/Log_Backup/Wifi"
LogDir="/storage/emulated/0/Documents/Log/Wifi"
Create_Folder "$Backup_LogDir"


Wifi_SetDriverLog="${LogDir}/Wifi_SetDriverParameter.log"
Wffi_DeleteProfileLog="${LogDir}/Wifi_DeleteProfile.log"
Wifi_SchduleLog="${LogDir}/Wifi_ScheduleLog.log"
Wifi_ConnectCommandLog="${LogDir}/Wifi_ConnectionCommand.log"
Wifi_CountLog="${LogDir}/Wifi_Count.log"
Wifi_PingLog="${LogDir}/Wifi_Ping.log"
Wifi_PingAddTimeLog="${LogDir}/Wifi_Ping_addtime.log"
Wifi_PingFailSummaryLog="${LogDir}/Wifi_Ping_failsummary.log"
Wifi_PingRateLog="${LogDir}/Wifi_Ping_rate.log"
temp_ping_startline="/storage/emulated/0/Documents/Wifi/wifi_ping_start_line"

if [ -f "$Wifi_SetDriverLog" ]; then
    mv "$Wifi_SetDriverLog" "$Backup_LogDir/Wifi_SetDriverParameter.log";
fi

if [ -f "$Wffi_DeleteProfileLog" ]; then
    mv "$Wffi_DeleteProfileLog" "$Backup_LogDir/Wifi_DeleteProfile.log";
fi

if [ -f "$Wifi_SchduleLog" ]; then
    mv "$Wifi_SchduleLog" "$Backup_LogDir/Wifi_ScheduleLog.log";
fi

if [ -f "$Wifi_ConnectCommandLog" ]; then
    mv "$Wifi_ConnectCommandLog" "$Backup_LogDir/Wifi_ConnectCommand.log";
fi

if [ -f "$Wifi_CountLog" ]; then
    mv "$Wifi_CountLog" "$Backup_LogDir/Wifi_Count.log";
fi

if [ -f "$Wifi_PingLog" ]; then
    cat "$Wifi_PingLog" > "$Backup_LogDir/Wifi_Ping.log" && > "$Wifi_PingLog";
fi

if [ -f "$Wifi_PingAddTimeLog" ]; then
    mv "$Wifi_PingAddTimeLog" "$Backup_LogDir/Wifi_Ping_addtime.log";
fi

if [ -f "$Wifi_PingFailSummaryLog" ]; then
    mv "$Wifi_PingFailSummaryLog" "$Backup_LogDir/Wifi_Ping_failsummary.log";
fi

if [ -f "$Wifi_PingRateLog" ]; then
    mv "$Wifi_PingRateLog" "$Backup_LogDir/Wifi_Ping_rate.log";
fi

echo "0" > $temp_ping_startline;
