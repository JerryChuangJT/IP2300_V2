#!/system/bin/sh
# Create Time : 2025/07/17
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Wifi/StopScript_Wifi.sh "192.168.47.1"
#-----------------------------------------------------------------------------------
# Function : 
#       1. Executeing KillProcess.sh to stop the ping script and related processes.
#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : DUT IP
#           ex: "192.168.47.1"
#-----------------------------------------------------------------------------------

DUTIP=$1;

sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_schedule" 
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_connect"
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_getip"
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_ping_script" 
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_ping" "$DUTIP"
sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_check_ping" 
