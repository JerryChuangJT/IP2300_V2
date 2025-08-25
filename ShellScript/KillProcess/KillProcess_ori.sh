#!/system/bin/sh
# Create Time : 2024/09/04
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh KillProcess.sh "ping_script"
#-----------------------------------------------------------------------------------
# Function : 
#       1. kill the process in IP2300.
#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : Which process needs to kill
#			ping_script -> Ping_Script.sh
#           ping -> ping xxx.xxx.xxx.xxx
#           test_ping -> Test_PingScript.sh
#           ping_monitor -> Monitor_PingResponseLost.sh
#           wifi_connect -> Check_WifiConnectionStatus.sh
#           wifi_setdriver -> Set_WifiDriver.sh
#           wifi_getip -> Check_WiFiIP.sh
#			youtube -> Youtube.sh
#           youtube_monitor -> Check_YoutubeStatus.sh
#           ether_connect -> Check_EtherConnection.sh
#-----------------------------------------------------------------------------------

###==========================================
### Variables
Kill_PrcessType=$1;
parameter2=$2;
processes="";
###==========================================
### To find related processes. ###
### Realed to Ping Scripts.
if [ "$Kill_PrcessType" = "ping_script" ]; then
    processes=$(ps -ef | grep "/storage/emulated/0/Documents/Ping/Ping_Script.sh ${parameter2}" | grep -v grep);
elif [ "$Kill_PrcessType" = "ping" ]; then
	processes=$(ps -ef | grep "ping -I wlan0 ${parameter2}" | grep -v grep);
elif [ "$Kill_PrcessType" = "ping_monitor" ]; then
    echo "stop" > /storage/emulated/0/Documents/Ping/${parameter2}_execute_status;

### Related to Wifi Scripts.
elif [ "$Kill_PrcessType" = "wifi_connect" ]; then
    processes=$(ps -ef | grep '/storage/emulated/0/Documents/Wifi/Check_WifiConnectionStatus.sh' | grep -v grep);
elif [ "$Kill_PrcessType" = "wifi_setdriver" ]; then
	processes=$(ps -ef | grep '/storage/emulated/0/Documents/Wifi/Set_WifiDriver.sh' | grep -v grep);
elif [ "$Kill_PrcessType" = "wifi_getip" ]; then
	processes=$(ps -ef | grep '/storage/emulated/0/Documents/Wifi/Check_WiFiIP.sh' | grep -v grep);

### Related to Youtube Scripts.
elif [ "$Kill_PrcessType" = "youtube" ]; then
    processes=$(ps -ef | grep '/storage/emulated/0/Documents/Youtube/Youtube.sh' | grep -v grep);
elif [ "$Kill_PrcessType" = "youtube_monitor" ]; then
    processes=$(ps -ef | grep '/storage/emulated/0/Documents/Youtube/Check_YoutubeStatus.sh' | grep -v grep);

### Related to Check Ether Connection.
elif [ "$Kill_PrcessType" = "ether_connect" ]; then
    processes=$(ps -ef | grep '/storage/emulated/0/Documents/EtherConnection/Check_EtherConnection.sh' | grep -v grep);
fi

###==========================================
### Find all of PIDs in $processes and stop them.
echo "$processes" | while read -r line; do

    ### Get PID and kill it.
    pid=$(echo $line | awk '{print $2}')
    su root kill -9 $pid
    echo "Killed process with PID $pid"
done


ps -ef | grep "ping -I wlan 8.8.8.8" | grep -v grep