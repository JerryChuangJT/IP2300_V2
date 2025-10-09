#!/system/bin/sh
# Create Time : 2024/09/04
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "$1" "$2"
#-----------------------------------------------------------------------------------
# Function : 
#       1. kill or Stop the process in IP2300.
#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : Which process needs to kill
#           a. ping_schedule -> ScriptSchedule_Ping.sh
#			b. ping_script -> Ping_Script.sh
#           c. ping -> ping xxx.xxx.xxx.xxx
#           d. ping_monitor -> Monitor_PingResponseLost.sh

#           e. wifi_connect -> Check_WifiConnectionStatus.sh
#           f. wifi_setdriver -> Set_WifiDriver.sh
#           g. wifi_getip -> Check_WiFiIP.sh

#			h. youtube -> Youtube.sh
#           i. youtube_monitor -> Check_YoutubeStatus.sh
#           j. ether_connect -> Check_EtherConnection.sh

#       $2 : Parameter for the process.
#           a. sh KillProcess.sh "ping_schedule" "Test1"
#           b. sh KillProcess.sh "ping_script" "Test1"
#           c. sh KillProcess.sh "ping" "8.8.8.8"
#           d. sh KillProcess.sh "ping_monitor" "Test1"
#-----------------------------------------------------------------------------------

###==========================================
### Variables
Kill_PrcessType=$1;
parameter2=$2;
processes="";
###==========================================
### To find related processes. ###
### Realed to Ping Scripts.
if [ "$Kill_PrcessType" = "ping_schedule" ]; then
    processes=$(ps -ef | grep "/storage/emulated/0/Documents/Ping/ScriptSchedule_Ping.sh ${parameter2}" | grep -v grep);
elif [ "$Kill_PrcessType" = "ping_script" ]; then
    processes=$(ps -ef | grep "/storage/emulated/0/Documents/Ping/Ping_Script.sh ${parameter2}" | grep -v grep);
elif [ "$Kill_PrcessType" = "ping" ]; then
	processes=$(ps -ef | grep "ping -I wlan0 ${parameter2}" | grep -v grep);
elif [ "$Kill_PrcessType" = "ping_monitor" ]; then
    echo "Stop" > /storage/emulated/0/Documents/Ping/${parameter2}_run_status;
    processes=$(ps -ef | grep "/storage/emulated/0/Documents/Ping/Monitor_PingResponseLost" | grep -v grep);

### Related to Wifi Scripts.
elif [ "$Kill_PrcessType" = "wifi_schedule" ]; then
    processes=$(ps -ef | grep "/storage/emulated/0/Documents/Wifi/ScriptSchedule_Wifi.sh" | grep -v grep);
elif [ "$Kill_PrcessType" = "wifi_connect" ]; then
    echo "Stop" > /storage/emulated/0/Documents/Wifi/wifi_run_status;
elif [ "$Kill_PrcessType" = "wifi_getip" ]; then
	echo "Stop" > /storage/emulated/0/Documents/Wifi/getip_run_status;
elif [ "$Kill_PrcessType" = "wifi_ping_script" ]; then
	processes=$(ps -ef | grep "/storage/emulated/0/Documents/Wifi/Wifi_PingScript.sh" | grep -v grep);
elif [ "$Kill_PrcessType" = "wifi_ping" ]; then
	processes=$(ps -ef | grep "ping -I wlan0 ${parameter2}" | grep -v grep);
elif [ "$Kill_PrcessType" = "wifi_check_ping" ]; then
	echo "Stop" > /storage/emulated/0/Documents/Wifi/wifi_ping_run_status;

### Related to Youtube Scripts.
elif [ "$Kill_PrcessType" = "youtube_schedule" ]; then
    processes=$(ps -ef | grep "/storage/emulated/0/Documents/Youtube/ScriptSchedule_Youtube.sh" | grep -v grep);
elif [ "$Kill_PrcessType" = "youtube" ]; then
    echo "Stop" > /storage/emulated/0/Documents/Youtube/youtube_run_status;
elif [ "$Kill_PrcessType" = "youtube_monitor" ]; then
    echo "Stop" > /storage/emulated/0/Documents/Youtube/monitor_run_status;

### Related to Check Ether Connection.
elif [ "$Kill_PrcessType" = "ether_check" ]; then
    processes=$(ps -ef | grep '/storage/emulated/0/Documents/EtherConnection/Check_EtherConnection.sh' | grep -v grep);

fi;
###==========================================
### Find all of PIDs in $processes and stop them.
echo "$processes" | while read -r line; do

    ### Get PID and kill it.
    pid=$(echo $line | awk '{print $2}') 
    su root kill -9 $pid
    echo "Killed process with PID $pid"
done