#!/system/bin/sh
# Create Time : 2025/07/24
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Wifi/Wifi_Connection.sh "4FNN-003_5G" "wpa2" "12345678" "48:f8:b3:e3:d0:69"

#-----------------------------------------------------------------------------------
# Function : 
#       1. Check Wifi Script to run at the specified time.
#       2. Execute Wifi Connection, Get IP, Ping Script and Check Ping Script.
#       3. Stop the scripts when the time is not in the schedule.
#       4. [Log] Wifi_ScheduleLog.log
#                - Record the schedule and execution status.
#       5. [Log] Wifi_Connection_result.log
#                - Record the connection result.
#                - Set Result as Wait.
#       6. [Log] Wifi_IP_result.log
#                - Record the IP result.
#                - Set Result as Wait.
#       7. [temp] wifi_run_status (Start/Stop)
#                - Record the run status of the script.
#       8. [temp] wifi_command_count
#                - Record the command count and start time.
#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : Wifi_SSID
#           ex : "4FNN-003_5G"

#       $2 : Wifi_Auth
#           ex : "wpa2"

#       $3 : Wifi_Password
#           ex : "12345678"

#       $4 : Wifi_BSSID
#           ex : "48:f8:b3:e3:d0:69"

#-----------------------------------------------------------------------------------
Get_CurrentDateTime() {
    local DateTimeNow=$(date "+%Y-%m-%d %H:%M:%S.%3N");
    echo "$DateTimeNow";
};

Get_CurrentTimeStamp() {
    local TimeStampNow=$(date +%s.%3N);
    echo "$TimeStampNow";
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

ConnectWiFi_ExecuteCommand_WriteLog() {
    local ssid="$1"
    local auth="$2"
    local password="$3"
    local bssid="$4"
    
    local count_starttime=$(grep "StartTime" "$wifi_count_file" | awk -F': ' '{print $2}')
    local connect_count=$(grep "WifiConnectCount" "$wifi_count_file" | awk -F': ' '{print $2}')
    local current_datetime=$(Get_CurrentDateTime)

    cmd wifi connect-network "$ssid" "$auth" "$password" -b "$bssid"
    
    echo "[$current_datetime] cmd wifi connect-network '$ssid' '$auth' '$password' -b '$bssid'" >> "$LogFile_CommandRecord" 2>&1
    {
        echo "StartTime : $count_starttime";
        echo "CurrentDateTime : $current_datetime";
        echo "Wifi_SSID : $Wifi_SSID";
        echo "Wifi_Auth : $Wifi_Auth";
        echo "Wifi_Password : $Wifi_Password";
        echo "Wifi_BSSID : $Wifi_BSSID";
        echo "WifiConnectCount : $((connect_count + 1))";
        echo "----------------------------------------------------------------------";
    } > "$wifi_count_file" 2>&1;
};

Restart_NetworkInterface() {
    ifconfig eth0 down;
    echo "[$(Get_CurrentDateTime)] ifconfig eth0 down" >> "$LogFile_CommandRecord" 2>&1;
    sleep 4;
    ifconfig eth0 up;
    echo "[$(Get_CurrentDateTime)] ifconfig eth0 up" >> "$LogFile_CommandRecord" 2>&1;
}

Update_Wifi_Connection_Status() {
    local status="$1"

    {
        echo "Time: $(Get_CurrentDateTime)";
        echo "Wifi_SSID: $Wifi_SSID";
        echo "Wifi_Auth: $Wifi_Auth";
        echo "Wifi_Password: $Wifi_Password";
        echo "Wifi_BSSID: $Wifi_BSSID";
        echo "Result: $status";
    } > "$LogFile_Connection_Result" 2>&1;

}
#--------------------------------------------------------------
### Variables
Wifi_SSID=$1;
Wifi_Auth=$2;
Wifi_Password=$3;
Wifi_BSSID=$4;

#--------------------------------------------------------------
#### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Wifi"
Create_Folder "$LogDir"

### Create Log Files.
LogFile_CommandRecord="${LogDir}/Wifi_ConnectionCommand.log";
LogFile_Connection_Result="${LogDir}/Wifi_Connection_result.log";
LogFile_WifiCount="${LogDir}/Wifi_Count.log";

TestStart_Time=$(Get_CurrentDateTime);
{
    echo "======================================================================";
    echo "StartTime : $TestStart_Time";
    echo "Wifi_SSID : $Wifi_SSID";
    echo "Wifi_Auth : $Wifi_Auth";
    echo "Wifi_Password : $Wifi_Password";
    echo "Wifi_BSSID : $Wifi_BSSID";
} >> "$LogFile_CommandRecord" 2>&1;

Update_Wifi_Connection_Status "Pass";

#--------------------------------------------------------------
wifi_run_status_file="/storage/emulated/0/Documents/Wifi/wifi_run_status"
wifi_count_file="/storage/emulated/0/Documents/Wifi/wifi_command_count"
current_datetime=$(Get_CurrentDateTime);

echo "Start" > "$wifi_run_status_file" 2>&1;
{
    echo "StartTime : $current_datetime";
    echo "CurrentDateTime : $current_datetime";
    echo "Wifi_SSID : $Wifi_SSID";
    echo "Wifi_Auth : $Wifi_Auth";
    echo "Wifi_Password : $Wifi_Password";
    echo "Wifi_BSSID : $Wifi_BSSID";
    echo "WifiConnectCount : 0";
    echo "----------------------------------------------------------------------";
} > "$wifi_count_file" 2>&1;

### ========================================================================================
### ========================================================================================
### Variables
### When Wifi Limmit Connection happens, it will show "PARTIAL_CONNECTIVITY" in "cmd wifi status".
command_CheckLimitConnect="cmd wifi status | grep PARTIAL_CONNECTIVITY";    
Flag_ExecuteCommand=1;

while true; do
    ### if Flag_ExecuteCommand=1 => Connect WiFi.
    ### Execute Wifi Connection Command.
    ### Flag_ExecuteCommand=0
    if [ "$Flag_ExecuteCommand" -eq 1 ]; then
        ConnectWiFi_ExecuteCommand_WriteLog "$Wifi_SSID" "$Wifi_Auth" "$Wifi_Password" "$Wifi_BSSID";
        Update_Wifi_Connection_Status "Pass";
        Flag_ExecuteCommand=0;
    fi;

    ###-------------------------------------------------------------------------
    ### Wait and check status for 30 seconds.
    for i in $(seq 1 30); do
        ### Check wifi_run_status_file != "Start"
        ### Stop the script.
        wifi_run_status=$(cat "$wifi_run_status_file" 2>&1);
        if [ "$wifi_run_status" != "Start" ]; then
            cat "$wifi_count_file" >> "$LogFile_WifiCount" 2>&1;
            echo "[$(Get_CurrentDateTime)] Test Stop" >> "$LogFile_CommandRecord" 2>&1;
            exit 0;
        fi;

        ### Check wifi_connect_status != "Pass"
        ### Flag_ExecuteCommand=1;
        wifi_connect_status=$(grep "Result" "$LogFile_Connection_Result" | awk -F': ' '{print $2}')
        if [ "$wifi_connect_status" != "Pass" ]; then
            Flag_ExecuteCommand=1;
            break;  
        fi;
        
        sleep 1;
    done;

    ###-------------------------------------------------------------------------
    ### Check whether the wifi Limmit Connection happens or not.
    ### if -z checks if the command output is empty.
    ### if -n checks if the command output is not empty.
    ### Restart Network Interface if Limmit Connection happens.
    ### Flag_ExecuteCommand=1;
    command_CheckLimitConnect_Result=$(eval "$command_CheckLimitConnect" 2>&1);
    if [ -n "$command_CheckLimitConnect_Result" ]; then
        echo "[$(Get_CurrentDateTime)] $command_CheckLimitConnect (the result is not empty means Limmited Connection happened)" 2>&1;
        echo "[$(Get_CurrentDateTime)] ==> $command_CheckLimitConnect_Result" >> "$LogFile_CommandRecord" 2>&1;
        Restart_NetworkInterface;
        Flag_ExecuteCommand=1;
    fi; 
done;