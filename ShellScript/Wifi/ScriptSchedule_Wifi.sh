#!/system/bin/sh
# Create Time : 2025/07/25
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Wifi/ScriptSchedule_Wifi.sh "4FNN-003_5G" "wpa2" "12345678" "48:f8:b3:e3:d0:69" "ipv4" "192.168.47.1" "2,00:00,1440/3,00:00,1440"
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

#       $5 : PingType (ipv4 or ipv6)
#           ex: "ipv4" / "ipv6"

#       $6 : DUT IP (Destination IP for ping)
#           ex: "192.168.47.1"

#       $7 : Schedule (Format: "weekday,starttime,runtime/weekday,starttime,runtime")
#           ex: "2,16:26,2" means Tuesday at 16:26 for 2 minutes.
#                - weekday is 0 (Sunday) to 6 (Saturday)
#                - starttime is in HH:MM format
#                - runtime is in minutes    

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

Get_CurrentDay() {
    date "+%w"  # Returns the day of the week (0=Sunday, 6=Saturday)
};

Get_CurrentSeconds() {
    echo $(( $(date +%H) * 60 * 60 + $(date +%M) * 60 + $(date +%S)))  # Returns the current time in total seconds.
};

### -----------------------------------------------------------------------------------
LogDir="/storage/emulated/0/Documents/Log/Wifi"
Create_Folder "$LogDir"

Wifi_SSID=$1;
Wifi_Auth=$2;
Wifi_Password=$3;
Wifi_BSSID=$4;
PingType=$5;
DUTIP=$6;
Schedule=$7;

### Create Log Files.
CurrentDateTime=$(Get_CurrentDateTime)
ScheduleLogFile="${LogDir}/Wifi_ScheduleLog.log";
Wifi_CurrentResult_File="${LogDir}/Wifi_Connection_result.log";
GetIP_CurrentResult_File="${LogDir}/Wifi_IP_result.log";
{
    echo "StartTime: $CurrentDateTime";
    echo "Wifi_SSID: $Wifi_SSID";
    echo "Wifi_Auth: $Wifi_Auth";
    echo "Wifi_Password: $Wifi_Password";
    echo "Wifi_BSSID: $Wifi_BSSID";
    echo "Schedule: $Schedule";
    echo "------------------------------------------------";
} >> "$ScheduleLogFile" 2>&1;

{
    echo "Time: $CurrentDateTime";
    echo "Wifi_SSID: $Wifi_SSID";
    echo "Wifi_Auth: $Wifi_Auth";
    echo "Wifi_Password: $Wifi_Password";
    echo "Wifi_BSSID: $Wifi_BSSID";
    echo "Result : Wait";
} > "$Wifi_CurrentResult_File" 2>&1;

{
    echo "Time: $CurrentDateTime";
    echo "IPv4: ";
    echo "IPv6: ";
    echo "Result: $Wait";
} > "$GetIP_CurrentResult_File" 2>&1;

### -----------------------------------------------------------------------------------
### Parse schedule into an array
segments=($(echo "$Schedule" | tr '/' '\n'))
weekday=()
starttime=()
runtime=()

for segment in "${segments[@]}"; do
    while IFS=',' read -r w s r; do
        weekday+=("$w")
        starttime+=("$s")
        runtime+=("$r")
    done <<< "$segment"
done

ExecuteCMD_Flag=0;
CheckSchedule=0;

#-----------------------------------------------------------------------------------
while true; do
    ### Get Current Day and Time.
    ### Loop through the schedule.
    today_weekday=$(Get_CurrentDay)  # Get current day (0=Sunday, 6=Saturday)
    current_seconds=$(Get_CurrentSeconds)
    for i in "${!weekday[@]}"; do
        scheduled_day="${weekday[i]}"
        scheduled_time="${starttime[i]}"
        duration_minutes="${runtime[i]}"

        start_h=${scheduled_time%%:*}
        start_m=${scheduled_time#*:}
        start_minutes=$((start_h * 60 + start_m))
        start_seconds=$((start_minutes * 60))

        end_minutes=$((start_minutes + duration_minutes))
        end_seconds=$((end_minutes * 60))

        ### Handle cross-night condition
        if (( end_minutes > 1440 )); then
            next_day_weekday=$(( (scheduled_day + 1) % 7 ))
            end_minutes=$((end_minutes - 1440))
            end_seconds=$((end_minutes * 60))
        else
            next_day_weekday=-1
        fi

        ### Check if current time is within the execution range
        if [[ "$today_weekday" -eq "$scheduled_day" && "$current_seconds" -ge "$start_seconds" && "$current_seconds" -lt "$end_seconds" ]]; then
            CheckSchedule=1;
            break
        elif [[ "$today_weekday" -eq "$next_day_weekday" && "$current_seconds" -lt "$end_seconds" ]]; then
            CheckSchedule=1;
            break
        else
            CheckSchedule=0
        fi;
    done;

    ### Execute or stop the ping command based on the schedule
    if [ "$CheckSchedule" -eq 1 ]; then
        if [ "$ExecuteCMD_Flag" -eq 0 ]; then
            {   
                echo "[$(Get_CurrentDateTime)] Execute the scripts.";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/Wifi/Connect_Wifi.sh '$Wifi_SSID' '$Wifi_Auth' '$Wifi_Password' '$Wifi_BSSID' &"
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/Wifi/Get_Wifi_IP.sh &"
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/Wifi/Wifi_PingScript.sh '$PingType' '$DUTIP' &"
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/Wifi/Wifi_CheckPing.sh &"
            } >> "$ScheduleLogFile" 2>&1
            ExecuteCMD_Flag=1;

            sh /storage/emulated/0/Documents/Wifi/Wifi_Connection.sh "$Wifi_SSID" "$Wifi_Auth" "$Wifi_Password" "$Wifi_BSSID" &
            sh /storage/emulated/0/Documents/Wifi/Wifi_GetIP.sh &
            sh /storage/emulated/0/Documents/Wifi/Wifi_PingScript.sh "$PingType" "$DUTIP" &
            sh /storage/emulated/0/Documents/Wifi/Wifi_CheckPing.sh &

        fi;
    else
        if [ "$ExecuteCMD_Flag" -eq 1 ]; then
            {
                echo "[$(Get_CurrentDateTime)] Stop the scripts.";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'wifi_connect'";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'wifi_getip'";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'wifi_ping_script'";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'wifi_ping' '$DUTIP'";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'wifi_check_ping'";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/Wifi/Delete_AllWiFiProfile.sh";
                echo "--------------------------------------------------";
            } >> "$ScheduleLogFile" 2>&1
            ExecuteCMD_Flag=0;
        fi;
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_connect";
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_getip";
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_ping_script";
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_ping" "$DUTIP";
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "wifi_check_ping";
        sh /storage/emulated/0/Documents/Wifi/Delete_AllWiFiProfile.sh;
        {
            echo "Time : $(Get_CurrentDateTime)";
            echo "Wifi_SSID: $Wifi_SSID";
            echo "Wifi_Auth: $Wifi_Auth";
            echo "Wifi_Password: $Wifi_Password";
            echo "Wifi_BSSID: $Wifi_BSSID";
            echo "Result : Wait";
        } > "$Wifi_CurrentResult_File" 2>&1;
        {
            echo "Time: $(Get_CurrentDateTime)";
            echo "IPv4: ";
            echo "IPv6: ";
            echo "Result: Wait";
        } > "$GetIP_CurrentResult_File" 2>&1;
    fi;
    sleep 1;
done;




