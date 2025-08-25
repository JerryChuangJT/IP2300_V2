#!/system/bin/sh
# Create Time : 2025/07/22
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Youtube/StopScript_Youtube.sh
#-----------------------------------------------------------------------------------
# Function : 
#       1. Executeing KillProcess.sh to stop the youtube script and related processes.
#-----------------------------------------------------------------------------------
# Variables : 

#-----------------------------------------------------------------------------------

sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "youtube_schedule"
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "youtube"
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "youtube_monitor"

