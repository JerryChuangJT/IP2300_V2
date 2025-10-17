#!/system/bin/sh
# Create Time : 2025/07/25
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Wifi/Wifi_CheckPing.sh
#-----------------------------------------------------------------------------------
# Function :
#       1. Check Wifi Script to run at the specified time.
#       2. Execute Wifi Connection, Get IP, Ping Script and Check Ping Script.  
#       3. [Log] Wifi_Connection_result.log
#                - Record the connection result.
#                - Set Result as Wait.
#       4. [Log] Wifi_Ping_rate.log
#                - Record the ping rate result.
#       5. [Log] Wifi_Ping.log
#                - Record the ping result.
#       6. [Log] Wifi_Ping_addtime.log
#                - Record the ping result with add time.
#       7. [Log] Wifi_Ping_failsummary.log
#                - Record the ping error summary.
#       8. [Log] Wifi_Ping_rate.log
#                - Record the ping rate result.
#       9. [temp] wifi_ping_temp_file
#                - Temporary file for ping log analysis.
#       10. [temp] wifi_ping_run_status
#                - File for execute status.
#       11. [temp] wifi_ping_start_line
#                - File for start line of ping log analysis.
#       12. [temp] wifi_ping_rate
#                - File for ping rate result.

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

Get_CurrentTimeStamp() {
    local TimeStampNow=$(date +%s.%3N);
    echo "$TimeStampNow";
};

Init_StartLine_File() {
    local startline_file="$1"
    if [ ! -f "$startline_file" ]; then
        echo "1" > "$startline_file" 2>&1;
    fi
}

Get_StartLine() {
    local startline_file="$1"
    if [ ! -f "$startline_file" ]; then
        echo "1" > "$startline_file" 2>&1;
        echo "1";  # ← 修正：要輸出值
        return 0;
    fi
    
    local start_line=$(cat "$startline_file")
    if [ "$start_line" -eq 0 ]; then
        echo "1" > "$startline_file" 2>&1;
        echo "1";  # ← 修正：要輸出值
    else
        echo "$start_line";
    fi
}

Update_Wifi_Connection_Status() {
    local status="$1"

    ### Get the last ping rate parameters from log file.
    Wifi_SSID=$(grep "Wifi_SSID" "$LogFile_Connection_Result" | awk -F': ' '{print $2}')
    Wifi_Auth=$(grep "Wifi_Auth" "$LogFile_Connection_Result" | awk -F': ' '{print $2}')
    Wifi_Password=$(grep "Wifi_Password" "$LogFile_Connection_Result" | awk -F': ' '{print $2}')
    Wifi_BSSID=$(grep "Wifi_BSSID" "$LogFile_Connection_Result" | awk -F': ' '{print $2}')

    {
        echo "Time: $(Get_CurrentDateTime)";
        echo "Wifi_SSID: $Wifi_SSID";
        echo "Wifi_Auth: $Wifi_Auth";
        echo "Wifi_Password: $Wifi_Password";
        echo "Wifi_BSSID: $Wifi_BSSID";
        echo "Result: $status";
    } > "$LogFile_Connection_Result" 2>&1;

}

Update_PingRate_File() {
    local new_PassCount="$1";
    local new_FailCount="$2";
    local new_ResponseTotal="$3";
    local CurrentTime=$(Get_CurrentDateTime);

    ### Check the file is exist or not.
    if [ ! -f "$pingrate_file" ]; then
        PassCount=$new_PassCount;
        FailCount=$new_FailCount;
        ResponseTotal=$new_ResponseTotal;
        # if [ $(($PassCount + $FailCount)) -eq 0 ]; then
        if [ "$PassCount" -eq 0 ]; then
            ResponseAverage=0
        else
            ResponseAverage=$(echo "scale=1; $ResponseTotal / $PassCount" | bc);
        fi;
    else
        ### Get the last ping rate parameters from log file.
        StartTime=$(grep "StartTime" "$pingrate_file" | awk -F': ' '{print $2}')
        PassCount=$(grep "PassCount" "$pingrate_file" | awk -F': ' '{print $2}')
        FailCount=$(grep "FailCount" "$pingrate_file" | awk -F': ' '{print $2}')
        ResponseTotal=$(grep "ResponseTotal" "$pingrate_file" | awk -F': ' '{print $2}')

        ### Update the ping rate parameters.
        PassCount=$(($PassCount + $new_PassCount))
        FailCount=$(($FailCount + $new_FailCount))
        ResponseTotal=$(echo "scale=1; $ResponseTotal + $new_ResponseTotal" | bc)
        # if [ $(($PassCount + $FailCount)) -eq 0 ]; then
        if [ "$PassCount" -eq 0 ]; then
            ResponseAverage=0
        else
            ResponseAverage=$(echo "scale=1; $ResponseTotal / $PassCount" | bc)
        fi;
    fi;
    {   
        echo "StartTime : $StartTime"
        echo "Time : $CurrentTime";
        echo "PassCount : $PassCount";
        echo "FailCount : $FailCount";
        echo "ResponseTotal : $ResponseTotal";
        echo "ResponseAverage : $ResponseAverage";
    } > "$pingrate_file" 2>&1;
}

#-----------------------------------------------------------------------------------
### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Wifi"
Create_Folder "$LogDir"

### Log File
PingResult_File="${LogDir}/Wifi_Ping.log";
MonitorLog_File="${LogDir}/Wifi_Ping_addtime.log";
MonitorLog_FailSummary="${LogDir}/Wifi_Ping_failsummary.log";
LogFile_Connection_Result="${LogDir}/Wifi_Connection_result.log";
MonitorLog_PingRate="${LogDir}/Wifi_Ping_rate.log";

### Write Start Message in All of The Log File.
StartTime=$(Get_CurrentDateTime);
{
    echo "----------------------------------------------------------------------";
    echo "StartTime : $StartTime";
} >> "$MonitorLog_File" 2>&1;

{
    echo "======================================================================";
    echo "======================================================================";
    echo "StartTime : $StartTime" >> "$MonitorLog_FailSummary";
} >> "$MonitorLog_FailSummary" 2>&1;

#-----------------------------------------------------------------------------------
### temp_file : Temporary file for ping log analysis.
### excecutestatus_file : File for execute status.
### startline_file : File for start line of ping log analysis.
temp_file="/storage/emulated/0/Documents/Wifi/wifi_ping_temp_file";
excecutestatus_file="/storage/emulated/0/Documents/Wifi/wifi_ping_run_status";
startline_file="/storage/emulated/0/Documents/Wifi/wifi_ping_start_line";
pingrate_file="/storage/emulated/0/Documents/Wifi/wifi_ping_rate";

echo "Start" > "$excecutestatus_file" 2>&1;
Init_StartLine_File "$startline_file";
{
    echo "StartTime : $StartTime";
    echo "Time: $StartTime";
    echo "PassCount : 0";
    echo "FailCount : 0";
    echo "ResponseTotal : 0";
    echo "ResponseAverage : 0";
} > "$pingrate_file" 2>&1;
Update_Wifi_Connection_Status "Pass"

### ========================================================================================
### ========================================================================================
ping_error_count=0;

### Main Loop
while true; do

    pass_count=0;
    fail_count=0;
    response_total=0;

    ### Check Execute Status.
    execute_status=$(cat "$excecutestatus_file" 2>/dev/null);
    echo "Execute Status: $execute_status";

    if [ "$execute_status" != "Start" ]; then

        ### Write message in MonitorLog_FailSummary.
        if [ "$ping_error_count" -gt 0 ]; then
            current_time=$(Get_CurrentDateTime);
            {
                echo "[$current_time] Ping Error EndTime: $current_time";
                echo "[$current_time] Ping Error Count: $ping_error_count";
                echo "----------------------------------------------------------------------";
            } >> $MonitorLog_FailSummary 2>&1;
        fi

        ### Copy message to MonitorLog_PingRate.
        cat "$pingrate_file" >> "$MonitorLog_PingRate" 2>&1;
        echo "----------------------------------------------------------------------" >> "$MonitorLog_PingRate" 2>&1;
        rm -f "$temp_file" 2>/dev/null;
        exit 0;
    fi

    ### Get Start Line.
    ### Copy Ping Log & Analysis the Log.
    rm -f "$temp_file";
    start_line=$(Get_StartLine "$startline_file");
    tail -n +$start_line "$PingResult_File" > "$temp_file";
    while IFS= read -r line || [[ -n "$line" ]]; do

        ### Read Ping Log File.
        if echo "$line" | grep -vq -E "StartTime:|PingType:|Destination:|Executing Command:|ping: Warning:|---|rtt min|packets transmitted|PING"; then
            current_time=$(Get_CurrentDateTime);
            echo "[$current_time] $line" >> "$MonitorLog_File" 2>&1;
            
            ###--------------------------------------------------------------------------------
            ### Check if the line contains 'ttl' to determine if the ping was successful.             
            if echo "$line" | grep -q 'ttl'; then
                Update_Wifi_Connection_Status "Pass"
                if [ "$ping_error_count" -gt 0 ]; then
                    current_time=$(Get_CurrentDateTime);
                    {
                        echo "[$current_time] Ping Error EndTime: $current_time";
                        echo "[$current_time] Ping Error Count: $ping_error_count";
                        echo "----------------------------------------------------------------------";
                    } >> $MonitorLog_FailSummary 2>&1;
                fi
                ping_error_count=0;
                # time=$(echo "$line" | awk -F 'time=' '{print $2}' | awk '{print $1}');
                # time_float=$(printf "%.1f" "$time");
                pass_count=$((pass_count + 1));
            fi;

            ###--------------------------------------------------------------------------------
            ### If the line does not contain 'ttl', it indicates a ping error.
            if echo "$line" | grep -vq 'ttl'; then
                ping_error_count=$((ping_error_count + 1));
                fail_count=$((fail_count + 1));
            fi;

            ###---------------------------------------------------------------------------------
            ### Get Response Total.
            ### If "time=" is in line.
            ### response_total + response_time
            if echo "$line" | grep -q 'time='; then
                response_time=$(echo "$line" | awk -F 'time=' '{print $2}' | awk '{print $1}')
                response_total=$(echo "scale=1; $response_total + $response_time" | bc);
            fi;

            ###================================================================================
            ### Write Ping Error Summary.
            if [ "$ping_error_count" -eq 1 ]; then
                echo "[$(Get_CurrentDateTime)] Ping Error StartTime: $current_time" >> $MonitorLog_FailSummary 2>&1;
            fi;

            if [ "$ping_error_count" -eq 5 ]; then
                current_time=$(Get_CurrentDateTime);
                {
                    echo "[$current_time] Ping Error EndTime: $current_time";
                    echo "[$current_time] Ping Error Count: $ping_error_count";
                    echo "----------------------------------------------------------------------";
                } >> $MonitorLog_FailSummary 2>&1;
                Update_Wifi_Connection_Status "Fail"
                ping_error_count=0;
            fi;
        fi;
        start_line=$(($start_line + 1));
    done < "$temp_file";    
    echo "$start_line" > "$startline_file" 2>&1;
    echo "Next Start Line: $start_line";
    echo "Pass Count: $pass_count, Fail Count: $fail_count, Response Total: $response_total";
    Update_PingRate_File "$pass_count" "$fail_count" "$response_total";
    sleep 1;
done;





