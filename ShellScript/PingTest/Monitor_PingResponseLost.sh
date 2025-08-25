#!/system/bin/sh
# Create Time : 2025/07/17
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Ping/Monitor_PingResponseLost.sh "Test1" "1200" "60" "10"
#-----------------------------------------------------------------------------------
# Function : 
#       1. Monitor the ping response time and lost, and write the log.

#       2. Log [MonitorLog_File] 
#            Adding time stamp in ping log.

#       3. Log [MonitorLog_FailSummary] 
#            Recording all of the ping fail summary.

#       4. Log [MonitorLog_PingRate] 
#            Recording the ping rate, including pass count, fail count, response total, and response average.
#            **When excecutestatus_file != "Start", copy pingrate_file >> MonitorLog_PingRate.

#       5. Log [TestResult_File], it will record the current status of ping status.
#            Recording the current ping status. (PASS/FAIL)

#       6. temp [temp_file], it will copy ping information from XXX_ping.log for analysising ping log.
#            Copy the ping log from XXX_ping.log to temp_file for analysis.

#       7. temp [startline_file] for start line of ping log analysis.
#            It will be used to record the start line of ping log analysis, so that it can continue from the last line.

#       8. temp [excecutestatus_file] for execute status.
#            It will be used to check the execute status of this script, if it is not "start", it will stop the script.

#       9. temp [pingrate_file] for ping rate.
#            It will be used to record the ping rate, including pass count, fail count, response total, and response average.

#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : TestName
#           ex: "Test1".

#       $2 : ErrorTimeResponse_Threshold (ms)
#           ex: "1200".

#       $3 : ErrorConsecutiveTime_TimeResponse (s)
#           ex: "60".

#       $4 : ErrorConsecutiveTime_PingLost (s)
#           ex: "10".
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

Count_TimeDifferent() {
    local start=$1
    local end=$2
    local diff=$(echo "$end - $start" | bc)
    printf "%.3f\n" "$diff"
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
        echo "1";
        echo "1" > "$startline_file" 2>&1;
        return 0;
    fi
    
    local start_line=$(cat "$startline_file")
    if [ "$start_line" -eq 0 ]; then
        echo "1";
        echo "1" > "$startline_file" 2>&1;
    else
        echo "$start_line";
    fi
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
        if [ $(($PassCount + $FailCount)) -eq 0 ]; then
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
        if [ $(($PassCount + $FailCount)) -eq 0 ]; then
            ResponseAverage=0
        else
            ResponseAverage=$(echo "scale=1; $ResponseTotal / $PassCount" | bc)
        fi;
    fi;
    # echo "[$CurrentTime] StartTime : $StartTime"
    # echo "[$CurrentTime] PassCount : $PassCount"
    # echo "[$CurrentTime] FailCount : $FailCount"
    # echo "[$CurrentTime] ResponseTotal : $ResponseTotal"
    # echo "[$CurrentTime] ResponseAverage : $ResponseAverage"
    # echo "=======================================================================";
    {   
        echo "StartTime : $StartTime"
        echo "Time : $CurrentTime";
        echo "TestName : $TestName";
        echo "PassCount : $PassCount";
        echo "FailCount : $FailCount";
        echo "ResponseTotal : $ResponseTotal";
        echo "ResponseAverage : $ResponseAverage";
    } > "$pingrate_file" 2>&1;
}

Update_PingResult_File() {
    # local ping_result_file="$1";
    local result="$1";
    local CurrentTime=$(Get_CurrentDateTime);

    {
        echo "Time : $CurrentTime";
        echo "TestName : $TestName";
        echo "ErrorTimeResponse_Threshold : $ErrorTimeResponse_Threshold";
        echo "ErrorConsecutiveTime_TimeResponse : $ErrorConsecutiveTime_TimeResponse";
        echo "ErrorConsecutiveTime_PingLost : $ErrorConsecutiveTime_PingLost";
        echo "Result : $result";
    } > "$TestResult_File" 2>&1;
}

#-----------------------------------------------------------------------------------
### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Ping"
Create_Folder "$LogDir"

### Variables
TestName=${1}
ErrorTimeResponse_Threshold=$2;
ErrorConsecutiveTime_TimeResponse=$3;
ErrorConsecutiveTime_PingLost=$4;

### Log File
### PingResult_File : Ping result log.
### MonitorLog_File : Save the monitor log.
### MonitorLog_FailSummary : Save the fail summary log.
### TestResult_File : Save the test result log.
PingResult_File="${LogDir}/${1}_ping.log";
MonitorLog_File="${LogDir}/${1}_ping_addtime.log";
MonitorLog_FailSummary="${LogDir}/${1}_ping_failsummary.log";
MonitorLog_PingRate="${LogDir}/${1}_ping_rate.log";
TestResult_File="${LogDir}/${1}_ping_result.log";

### Write Start Message in All of The Log File.
StartTime=$(Get_CurrentDateTime);
{
    echo "----------------------------------------------------------------------";
    echo "StartTime : $StartTime";
    echo "TestName : $TestName";
    echo "ErrorTimeResponse_Threshold : $ErrorTimeResponse_Threshold";
    echo "ErrorConsecutiveTime_TimeResponse : $ErrorConsecutiveTime_TimeResponse";
    echo "ErrorConsecutiveTime_PingLost : $ErrorConsecutiveTime_PingLost";
} >> "$MonitorLog_File" 2>&1;

{
    echo "======================================================================";
    echo "======================================================================";
    echo "StartTime : $StartTime" >> "$MonitorLog_FailSummary";
    echo "TestName : $TestName" >> "$MonitorLog_FailSummary";
    echo "ErrorTimeResponse_Threshold : $ErrorTimeResponse_Threshold";
    echo "ErrorConsecutiveTime_TimeResponse : $ErrorConsecutiveTime_TimeResponse";
    echo "ErrorConsecutiveTime_PingLost : $ErrorConsecutiveTime_PingLost";
} >> "$MonitorLog_FailSummary" 2>&1;

Update_PingResult_File "FAIL"


#-----------------------------------------------------------------------------------
### temp_file : Temporary file for ping log analysis.
### excecutestatus_file : File for execute status.
### startline_file : File for start line of ping log analysis.
temp_file="/storage/emulated/0/Documents/Ping/${1}_temp_file";
excecutestatus_file="/storage/emulated/0/Documents/Ping/${1}_run_status";
startline_file="/storage/emulated/0/Documents/Ping/${1}_start_line";
pingrate_file="/storage/emulated/0/Documents/Ping/${1}_pingrate";

{
    echo "StartTime : $StartTime";
    echo "Time: $StartTime";
    echo "TestName : $TestName";
    echo "PassCount : 0";
    echo "FailCount : 0";
    echo "ResponseTotal : 0";
    echo "ResponseAverage : 0";
} > "$pingrate_file" 2>&1;

### "Start" >> excecutestatus_file
### Only write initial value when the file does not exist.
echo "Start" > "$excecutestatus_file" 2>&1;
Init_StartLine_File "$startline_file";

### ========================================================================================
### ========================================================================================
### Flag for Record Error Happened.
Error_PingResponse=0;
Error_PingLost=0;

WriteLog_PingRespone=0;
WriteLog_PingLost=0;

### Main Loop
while true; do
    ### Check Execute Status.
    execute_status=$(cat "$excecutestatus_file" 2>/dev/null);
    if [ "$execute_status" != "Start" ]; then
        CurrentTime=$(Get_CurrentDateTime);
        CurrentTimeStamp=$(Get_CurrentTimeStamp);
        
        ### Write End Message in All of The Log File.
        if [ "$WriteLog_PingRespone" -eq 1 ]; then
            TimeDifferent=$(Count_TimeDifferent "$Error_PingResponse_STS" "$CurrentTimeStamp");
            {
                echo "[$CurrentTime] PingResponse-EndTime : $CurrentTime";
                echo "[$CurrentTime] PingResponse-ErrorDuration : $TimeDifferent";
                echo "----------------------------------------------------------------------";
            } >> "$MonitorLog_FailSummary" 2>&1;
        fi;

        if [ "$WriteLog_PingLost" -eq 1 ]; then
            TimeDifferent=$(Count_TimeDifferent "$Error_PingLost_STS" "$CurrentTimeStamp");
            {
                echo "[$CurrentTime] PingLost-EndTime : $CurrentTime";
                echo "[$CurrentTime] PingLost-ErrorDuration : $TimeDifferent";
                echo "----------------------------------------------------------------------";
            } >> "$MonitorLog_FailSummary" 2>&1;
        fi;

        echo "[$CurrentTime] Test Stop" >> "$MonitorLog_File" 2>&1;
        echo "[$CurrentTime] Test Stop" >> "$MonitorLog_FailSummary" 2>&1;

        ### Write the final ping rate to the log file.
        if [ -f "$pingrate_file" ]; then
            cat "$pingrate_file" >> "$MonitorLog_PingRate" 2>&1;
            echo "----------------------------------------------------------------------" >> "$MonitorLog_PingRate" 2>&1;
        fi;
        return 0;
    fi;

    ### Get Start Line.
    ### Copy Ping Log & Analysis the Log.
    start_line=$(Get_StartLine "$startline_file");
    pass_count=0;
    fail_count=0;
    response_total=0;
    tail -n +$start_line "$PingResult_File" > "$temp_file";
    while IFS= read -r line || [[ -n "$line" ]]; do
        ###====================================================================================================================
        ###====================================================================================================================
        ### Read Ping Log File.
        if echo "$line" | grep -vq -E "StartTime:|PingTestName:|PingType:|Destination:|Executing Command:|ping: Warning:|---|rtt min|packets transmitted|PING"; then
            Error_PingResponse_ST=$(Get_CurrentDateTime);
            echo "[$Error_PingResponse_ST] $line" >> "$MonitorLog_File" 2>&1;

            ###--------------------------------------------------------------------------------
            ### Get Ping Response Time.
            ### If "ttl" is in line.
            ### pass_count + 1
            ### Error_PingResponse=0
            if echo "$line" | grep -q 'ttl'; then
                time=$(echo "$line" | awk -F 'time=' '{print $2}' | awk '{print $1}');
                time_float=$(printf "%.1f" "$time");
                
                ### If 
                if (( $(echo "$time_float > $ErrorTimeResponse_Threshold" | bc -l) )); then
                    Error_PingResponse=1;
                else
                    Error_PingResponse=0;
                    Update_PingResult_File "PASS";
                fi
                pass_count=$(($pass_count + 1));
                Error_PingLost=0;
            fi;

            ###--------------------------------------------------------------------------------
            ### Ping Lost.
            ### If "ttl" is not in line.
            ### fail_count + 1
            ### Error_PingLost=1
            if echo "$line" | grep -vq 'ttl'; then
                fail_count=$(($fail_count + 1));
                Error_PingLost=1;
            fi; 

            ###---------------------------------------------------------------------------------
            ### Get Response Total.
            ### If "time=" is in line.
            ### response_total + response_time
            if echo "$line" | grep -q 'time='; then
                response_time=$(echo "$line" | awk -F 'time=' '{print $2}' | awk '{print $1}')
                response_total=$(echo "scale=1; $response_total + $response_time" | bc);
            fi;
        fi;
        start_line=$(($start_line + 1));
    done < "$temp_file";
    rm -f "$temp_file";
    echo "$start_line" > "$startline_file" 2>&1;
    Update_PingRate_File "$pass_count" "$fail_count" "$response_total";

    ###====================================================================================================================
    ###====================================================================================================================
    ### Analyze Ping Reponse Error.
    ### If Ping Response Error, Write Log.
    ### If WriteLog_PingRespone is 0, it means the first time to write the log.
    ### If WriteLog_PingRespone is 1, it means the log is already written, so we need to check the time difference.
    if [ "$Error_PingResponse" -eq 1 ]; then
        if [ "$WriteLog_PingRespone" -eq 0 ]; then
            Error_PingResponse_ST=$(Get_CurrentDateTime);
            Error_PingResponse_STS=$(Get_CurrentTimeStamp);
            {
                echo "[$Error_PingResponse_ST] ErrorType : Ping Response" >> "$MonitorLog_FailSummary";
                echo "[$Error_PingResponse_ST] PingResponse-StartTime : $Error_PingResponse_ST";
            } >> "$MonitorLog_FailSummary" 2>&1;
            WriteLog_PingRespone=1;
        else
            ### Get Current Time & Time Stamp.
            CurrentTime=$(Get_CurrentDateTime);
            CurrentTimeStamp=$(Get_CurrentTimeStamp);
            
            ### Calculate Time Different.
            TimeDifferent=$(Count_TimeDifferent "$Error_PingResponse_STS" "$CurrentTimeStamp");
            
            if (( $(echo "$TimeDifferent > $ErrorConsecutiveTime_TimeResponse" | bc -l) )); then
                {
                    echo "[$CurrentTime] PingResponse-EndTime : $CurrentTime" >> "$MonitorLog_FailSummary";
                    echo "[$CurrentTime] PingResponse-ErrorDuration : $TimeDifferent" >> "$MonitorLog_FailSummary";
                    echo "----------------------------------------------------------------------";
                } >> "$MonitorLog_FailSummary" 2>&1;
                Update_PingResult_File "FAIL";
                Error_PingResponse=0;
                WriteLog_PingRespone=0;
            fi;
        fi;
    else
        if [ "$WriteLog_PingRespone" -eq 1 ]; then
            ### Get Current Time & Time Stamp.
            CurrentTime=$(Get_CurrentDateTime);
            CurrentTimeStamp=$(Get_CurrentTimeStamp);
            
            ### Calculate Time Different.
            TimeDifferent=$(Count_TimeDifferent "$Error_PingResponse_STS" "$CurrentTimeStamp");
            {
                echo "[$CurrentTime] PingResponse-EndTime : $CurrentTime" >> "$MonitorLog_FailSummary";
                echo "[$CurrentTime] PingResponse-ErrorDuration : $TimeDifferent" >> "$MonitorLog_FailSummary";
                echo "----------------------------------------------------------------------";
            } >> "$MonitorLog_FailSummary" 2>&1;
        fi;
        Error_PingResponse=0;
        WriteLog_PingRespone=0;
    fi;

    ###----------------------------------------------------------------------------------------------------------------
    ### Analyze Ping Lost Error.
    ### If Ping Lost Error, Write Log.
    ### If WriteLog_PingLost is 0, it means the first time to write the log.
    ### If WriteLog_PingLost is 1, it means the log is already written, so we need to check the time difference. 
    if [ "$Error_PingLost" -eq 1 ]; then
        if [ "$WriteLog_PingLost" -eq 0 ]; then
            WriteLog_PingLost=1;
            Error_PingLost_ST=$(Get_CurrentDateTime);
            Error_PingLost_STS=$(Get_CurrentTimeStamp);
            {
                echo "[$Error_PingLost_ST] ErrorType : Ping Lost" >> "$MonitorLog_FailSummary";
                echo "[$Error_PingLost_ST] PingLost-StartTime : $Error_PingLost_ST";
            } >> "$MonitorLog_FailSummary" 2>&1;
        else
            ### Get Current Time & Time Stamp.
            CurrentTime=$(Get_CurrentDateTime);
            CurrentTimeStamp=$(Get_CurrentTimeStamp);
            
            ### Calculate Time Different.
            TimeDifferent=$(Count_TimeDifferent "$Error_PingLost_STS" "$CurrentTimeStamp");
            
            if (( $(echo "$TimeDifferent > $ErrorConsecutiveTime_PingLost" | bc -l) )); then
                {
                    echo "[$CurrentTime] PingLost-EndTime : $CurrentTime" >> "$MonitorLog_FailSummary";
                    echo "[$CurrentTime] PingLost-ErrorDuration : $TimeDifferent" >> "$MonitorLog_FailSummary";
                    echo "----------------------------------------------------------------------";
                } >> "$MonitorLog_FailSummary" 2>&1;
                Update_PingResult_File "FAIL";
                WriteLog_PingLost=0;
                Error_PingLost=0;
            fi;
        fi;
    else
        if [ "$WriteLog_PingLost" -eq 1 ]; then
            ### Get Current Time & Time Stamp.
            CurrentTime=$(Get_CurrentDateTime);
            CurrentTimeStamp=$(Get_CurrentTimeStamp);
            
            ### Calculate Time Different.
            TimeDifferent=$(Count_TimeDifferent "$Error_PingLost_STS" "$CurrentTimeStamp");
            {
                echo "PingLost-EndTime : $CurrentTime";
                echo "PingLost-ErrorDuration : $TimeDifferent";
                echo "----------------------------------------------------------------------";
            } >> "$MonitorLog_FailSummary" 2>&1;
        fi;
        Error_PingLost=0;
        WriteLog_PingLost=0;
    fi;

    ### ------------------------------------------------------------------------------
    sleep 1;
done;