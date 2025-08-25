#!/system/bin/sh
# Create Time : 2025/07/03
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Ping/ScriptSchedule_Ping.sh "Test1" "ipv4" "8.8.8.8" "1200" "60" "10" "5,00:00,1440/6,00:00,1440/0,00:00,1440"
#-----------------------------------------------------------------------------------
# Function :
#       1. Schedule the ping test based on the provided parameters.
#           The schedule will be parsed and executed based on the current day and time.
#           The ping test will be executed if the current time is within the scheduled range.
#           The ping test will be stopped if the current time is outside the scheduled range.
#           The ping test will be executed in the background.
#           The ping test will be monitored for response time and lost.
#           The ping test will be logged in the file ${LogDir}/${PingTestName}_PingScheduleLog.log.
#           The ping test will be executed every second to check the schedule.
#           The ping test will be executed in the background.
#           The ping test will be executed with the parameters:
#           - PingTestName: The ping test nick name.
#           - PingType: The ping type (ipv4 or ipv6).       
#           - Destination: The ping destination.
#           - ErrorTimeResponse_Threshold: The threshold for the response time error.
#           - ErrorConsecutiveTime_TimeResponse: The consecutive time for the response time error.
#           - ErrorConsecutiveTime_PingLost: The consecutive time for the ping lost error.
#           - Schedule: The schedule for the ping test.

#       2. Log [ScheduleLogFile] 
#           TRecording all the cmd execution and the ping test parameters.
#-----------------------------------------------------------------------------------
# Variables :
#       $1 : ping test nick name.
#           ex: "Test1".

#       $2: ipv4 / ipv6

#       $3 : ping destination
#           ex: "8.8.8.8"

#       $4 : ErrorTimeResponse_Threshold
#           The threshold for the response time error in milliseconds.
#           ex: "1200" (1.2 seconds).

#       $5 : ErrorConsecutiveTime_TimeResponse
#           The consecutive time for the response time error in seconds.
#           ex: "60" (1 minute).

#       $6 : ErrorConsecutiveTime_PingLost
#           The consecutive time for the ping lost error in seconds.
#           ex: "10" (10 seconds).

#       $7 : Schedule
#           The schedule for the ping test in the format of "weekday,starttime,runtime/weekday,starttime,runtime".
#           The weekday is a number from 0 to 6,
#           where 0 is Sunday and 6 is Saturday.
#           The starttime is in the format of "HH:MM".
#           The runtime is in minutes.
#           ex: "4,16:30,1/4,16:32,1"
#           This means the ping test will be executed on Thursday (4) at 16:30 for 1 minute,
#           and on Thursday (4) at 16:32 for 1 minute.  
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
LogDir="/storage/emulated/0/Documents/Log/Ping"
Create_Folder "$LogDir"

PingTestName=$1;
PingType=$2;
Destination="$3";

ErrorTimeResponse_Threshold=$4;
ErrorConsecutiveTime_TimeResponse=$5;
ErrorConsecutiveTime_PingLost="$6";

Schedule="$7";

### -----------------------------------------------------------------------------------
ScheduleLogFile="${LogDir}/${PingTestName}_PingScheduleLog.log";
{
    echo "================================================";
    echo "StartTime: $(Get_CurrentDateTime)";
    echo "PingTestName: $PingTestName";
    echo "PingType: $PingType";
    echo "Destination: $Destination";
    echo "Schedule: $Schedule";
    echo "------------------------------------------------";
} >> "$ScheduleLogFile" 2>&1;

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
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/Ping/Ping_Script.sh $PingTestName $PingType $Destination &"
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/Ping/Monitor_PingResponseLost.sh "$PingTestName" "$ErrorTimeResponse_Threshold" "$ErrorConsecutiveTime_TimeResponse" "$ErrorConsecutiveTime_PingLost" &"
            } >> "$ScheduleLogFile" 2>&1
            ExecuteCMD_Flag=1;

            sh /storage/emulated/0/Documents/Ping/Ping_Script.sh "$PingTestName" "$PingType" "$Destination" &
            sh /storage/emulated/0/Documents/Ping/Monitor_PingResponseLost.sh "$PingTestName" "$ErrorTimeResponse_Threshold" "$ErrorConsecutiveTime_TimeResponse" "$ErrorConsecutiveTime_PingLost" &
        fi;
    else
        if [ "$ExecuteCMD_Flag" -eq 1 ]; then
            {
                echo "[$(Get_CurrentDateTime)] Stop the scripts.";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'ping_script' '$PingTestName'";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'ping' '$Destination'";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'ping_monitor' '$PingTestName'";
                
                echo "--------------------------------------------------";
            } >> "$ScheduleLogFile" 2>&1
            ExecuteCMD_Flag=0;
        fi;
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "ping_script" "$PingTestName"
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "ping" "$Destination"
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "ping_monitor" "$PingTestName"
        {
            echo "Time : $(Get_CurrentDateTime)";
            echo "TestName : $PingTestName";
            echo "ErrorTimeResponse_Threshold : $ErrorTimeResponse_Threshold";
            echo "ErrorConsecutiveTime_TimeResponse : $ErrorConsecutiveTime_TimeResponse";
            echo "ErrorConsecutiveTime_PingLost : $ErrorConsecutiveTime_PingLost";
            echo "Result : Wait";
        } > "/storage/emulated/0/Documents/Log/${PingTestName}_ping_result.log" 2>&1;
    fi;
    sleep 1;  # Check every second
done;


