#!/system/bin/sh
# Create Time : 2025/07/17
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Ping/StopScript_Ping.sh "Test1" "8.8.8.8"
#-----------------------------------------------------------------------------------
# Function : 
#       1. Executeing KillProcess.sh to stop the ping script and related processes.
#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : ping test nick name.
#           ex: "Test1".

#       $2 : ping destination
#           ex: "8.8.8.8"
#-----------------------------------------------------------------------------------

test_name=$1
destination=$2

sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "ping_schedule" "$test_name"
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "ping_script" "$test_name"
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "ping" "$destination"
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "ping_monitor" "$test_name"
