#!/system/bin/sh
# Create Time : 2025/07/22
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Youtube/BackupLog_Youtube.sh
#-----------------------------------------------------------------------------------
# Function : 
#       1. Create a backup folder for YouTube log files.
#       2. Move YouTube log files from the original log folder to the backup folder

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
Backup_LogDir="/storage/emulated/0/Documents/Log_Backup/Youtube"
LogDir="/storage/emulated/0/Documents/Log/Youtube"
Create_Folder "$Backup_LogDir"

Youtube_ScheduleLog="${LogDir}/Youtube_ScheduleLog.log"
Youtube_PlayUrlCommand="${LogDir}/Youtube_PlayUrlCommand.log"
YoutubePacket_GetPackets="${LogDir}/YoutubePacket_GetPackets.log"
YoutubePacket_FailSummary="${LogDir}/YoutubePacket_FailSummary.log"
Youtube_Count="${LogDir}/Youtube_Count.log"

if [ -f "$Youtube_ScheduleLog" ]; then
    mv "$Youtube_ScheduleLog" "$Backup_LogDir/Youtube_ScheduleLog.log";
fi

if [ -f "$Youtube_PlayUrlCommand" ]; then
    mv "$Youtube_PlayUrlCommand" "$Backup_LogDir/Youtube_PlayUrlCommand.log";
fi

if [ -f "$YoutubePacket_GetPackets" ]; then
    mv "$YoutubePacket_GetPackets" "$Backup_LogDir/YoutubePacket_GetPackets.log";
fi

if [ -f "$YoutubePacket_FailSummary" ]; then
    mv "$YoutubePacket_FailSummary" "$Backup_LogDir/YoutubePacket_FailSummary.log";
fi

if [ -f "$Youtube_Count" ]; then
    mv "$Youtube_Count" "$Backup_LogDir/Youtube_Count.log";
fi

