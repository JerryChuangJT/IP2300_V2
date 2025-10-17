#!/system/bin/sh
# Create Time : 2024/11/08
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Wifi/Wifi_CheckPing.sh
#-----------------------------------------------------------------------------------
# Function : 
#       1. Get IPv4 & IPv6 from Wifi Driver (wlan0) in whil loop.
#       2. [Log] Wifi_IP_result.log
#                - Record the IP result.
#                - Set Result as Fail if no IP found.
#       3. Stop the script when getip_run_status_file is not "Start".
#-----------------------------------------------------------------------------------
Get_CurrentDateTime() {
    local DateTimeNow=$(date "+%Y-%m-%d %H:%M:%S.%3N");
    echo "$DateTimeNow";
};

Create_Folder() {
    ### Get first parameter for folder path.
    folder_path="$1";

    ### Check folder is exist or not.
    if [ ! -d "$folder_path" ]; then

        ### make dir
        mkdir -p "$folder_path";
    fi
};

#--------------------------------------------------------------
#### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Wifi"
Create_Folder "$LogDir"

### Create Log Files.
LogFile_WiFiIP_Result="${LogDir}/Wifi_IP_result.log";
{
    echo "Time : $(Get_CurrentDateTime)";
    echo "IPv4 : ";
    echo "IPv6 : ";
    echo "Result : Fail" 
} > "$LogFile_WiFiIP_Result" 2>/dev/null;

#--------------------------------------------------------------
getip_run_status_file="/storage/emulated/0/Documents/Wifi/getip_run_status"
echo "Start" > "$getip_run_status_file"
### ========================================================================================
### ========================================================================================
Command_GetWlan0Ipv4="ip -4 addr show wlan0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1"
Command_GetWlan0Ipv6="ip -6 addr show wlan0 | grep 'inet6 ' | awk '{print \$2}' | cut -d/ -f1"
while true; do
    Get_Wlan0_Ipv4=$(eval "$Command_GetWlan0Ipv4")
    Get_Wlan0_Ipv6=$(eval "$Command_GetWlan0Ipv6")
    if [ -n "$Get_Wlan0_Ipv4" ] || [ -n "$Get_Wlan0_Ipv6" ]; then
        {
            echo "Time : $(Get_CurrentDateTime)";
            echo "IPv4 : $Get_Wlan0_Ipv4";
            echo "IPv6 : $Get_Wlan0_Ipv6";
            echo "Result : Pass";
        } > "$LogFile_WiFiIP_Result" 2>&1;
    else
        {
            echo "Time : $(Get_CurrentDateTime)";
            echo "IPv4 : ";
            echo "IPv6 : ";
            echo "Result : Fail";
        } > "$LogFile_WiFiIP_Result" 2>&1;
    fi
    
    ### Wait 3 seconds before next check.
    ### Check getip_run_status_file
    for i in $(seq 1 3); do
        getip_run_status=$(cat "$getip_run_status_file")
        if [ "$getip_run_status" != "Start" ]; then
            exit 0;
        fi;
        sleep 1;
    done;
done;












