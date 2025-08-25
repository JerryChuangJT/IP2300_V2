#!/system/bin/sh
# Create Time : 2025/07/25
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Wifi/Wifi_PingScript.sh "ipv4" "8.8.8.8" 
#-----------------------------------------------------------------------------------
# Function : 
#       1. Execute ping command with specified type (IPv4 or IPv6) and destination.
#       2. [Log] Wifi_Ping.log
#                - Record the ping results.
#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : PingType 
#           ex: "ipv4" or "ipv6"

#       $2 : Destination IP or hostname
#           ex: "192.168.47.1"

#-----------------------------------------------------------------------------------
Create_Folder() {
    ### Get first parameter for folder path.
    folder_path="$1";

    ### Check folder is exist or not.
    if [ ! -d "$folder_path" ]; then
        ### make dir
        mkdir -p "$folder_path";
    fi
};
    
Get_CurrentDateTime() {
    local DateTimeNow=$(date "+%Y-%m-%d %H:%M:%S.%3N");
    echo "$DateTimeNow";
};

### -----------------------------------------------------------------------------------
#### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Wifi"
Create_Folder "$LogDir"

PingType=$1;
Destination=$2;

PINGLOG_FILE="${LogDir}/Wifi_Ping.log";
{   
    echo "------------------------------------------------";
    echo "StartTime: $(Get_CurrentDateTime)";
    echo "PingType: $PingType";
    echo "Destination: $Destination";
} >> "$PINGLOG_FILE" 2>&1;

### -----------------------------------------------------------------------------------
if [ "$PingType" == "ipv4" ]; then
    PING_CMD="ping -I wlan0 ${Destination}";
elif [ "$PingType" == "ipv6" ]; then  
    PING_CMD="ping6 -I wlan0 ${Destination}";
fi;
echo "Executing Command: $PING_CMD" >> "$PINGLOG_FILE" 2>&1;


### ========================================================================================
### ========================================================================================
while true; do
    ### Execute ping with timeout for remaining time until midnight
    $PING_CMD >> "$PINGLOG_FILE" 2>&1;
    sleep 1  # Check every second
done




