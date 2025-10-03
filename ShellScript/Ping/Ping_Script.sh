#!/system/bin/sh
# Create Time : 2025/07/17
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Ping/Ping_Script.sh "Test1" "ipv4" "8.8.8.8" 
#-----------------------------------------------------------------------------------
# Function : 
#       1. Create and save ping result log. 
#           The log will be saved in the file $PINGLOG_FILE (${1}_ping.log).
#           The log will include the ping test nick name, ping type, destination, and schedule.
#           The log will be saved in the folder /storage/emulated/0/Documents/Log.

#       2. Create files : Save ping log in the file. 
#           $PINGLOG_FILE (${1}_ping.log)
#           The log will be saved in the folder /storage/emulated/0/Documents/Log.
#           The log will include the ping test nick name, ping type, destination, and schedule.
#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : ping test nick name. 
#           ex: "Test1".
#       
#       $2: ipv4 / ipv6
#           
#       $3 : ping destination
#           ex: "8.8.8.8"
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
    date "+%Y-%m-%d %H:%M:%S.%3N"
};

### -----------------------------------------------------------------------------------
#### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Ping"
Create_Folder "$LogDir"

PingTestName=$1;
PingType=$2;
Destination=$3;

PINGLOG_FILE="${LogDir}/${PingTestName}_ping.log";
{   
    echo "------------------------------------------------";
    echo "StartTime: $(Get_CurrentDateTime)";
    echo "PingTestName: $PingTestName";
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