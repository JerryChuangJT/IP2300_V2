#!/system/bin/sh
# Create Time : 2025/07/03
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Youtube/ScriptSchedule_Youtube.sh "https://www.youtube.com/watch?v=m_dhMSvUCIc,https://www.youtube.com/watch?v=V1p33hqPrUk" "1" "100" "5" "5,00:00,1440/6,00:00,1440/0,00:00,1440"
#-----------------------------------------------------------------------------------
# Function :
#       1. Schedule the Youtube script to run at specific times.
#       2. Check the current time and day to determine if the script should be executed
#       3. [Log] Youtube_ScheduleLog.log
#           Record the start time, list of YouTube URLs, play interval time, and schedule.

#-----------------------------------------------------------------------------------
# Variables :
#       $1 : YouTube URL list, separated by commas.
#           ex: "https://www.youtube.com/watch?v=m_dhMSvUCIc,https://www.youtube.com/watch?v=V1p33hqPrUk"

#       $2 : Play video interval time in minutes.
#           ex: "1" (1 minute). 

#       $3 : DiffPackets_ErrorThreshold - The threshold for the difference in RX packets to consider it an error.
#           ex: "100" (100 packets).    

#       $4 : ErrorTimes_FailThreshold - The number of consecutive errors required to consider the test failed.  
#           ex: "5" (5 consecutive errors).

#       $5 : Schedule - The schedule for executing the script.
#           Format: "weekday,starttime,runtime/weekday,starttime,runtime"
#           ex: "2,10:14,1/2,10:16,1"
#           where weekday is 0 (Sunday) to 6 (Saturday), starttime is in HH:MM format, and runtime is in minutes.
#           This means the script will run on Tuesday at 10:14 AM for 1 minute and on Tuesday at 10:16 AM for 1 minute. 

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
LogDir="/storage/emulated/0/Documents/Log/Youtube"
Create_Folder "$LogDir"

list_YoutubeURL=$1;
PlayVideo_Interval_Time=$2;
DiffPackets_ErrorThreshold=$3;
ErrorTimes_FailThreshold=$4;
Schedule=$5;

### Create Log file.
CurrentDateTime=$(Get_CurrentDateTime)
ScheduleLogFile="${LogDir}/Youtube_ScheduleLog.log";
GetPackets_CurrentResult_File="${LogDir}/YoutubePacket_result.log";
{
    echo "StartTime: $CurrentDateTime";
    echo "list_YoutubeURL: $list_YoutubeURL";
    echo "PlayVideo_Interval_Time: $PlayVideo_Interval_Time";
    echo "Schedule: $Schedule";
    echo "------------------------------------------------";
} >> "$ScheduleLogFile" 2>&1;

{
    echo "Time : $CurrentDateTime";
    echo "DiffPackets_ErrorThreshold : $DiffPackets_ErrorThreshold";
    echo "ErrorConsecutiveTimes_FailThreshold : $ErrorTimes_FailThreshold";
    echo "Result : Wait";
} > "$GetPackets_CurrentResult_File" 2>&1;
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
            sleep 60;
            {   
                echo "[$(Get_CurrentDateTime)] Execute the scripts.";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/Youtube/Youtube.sh $list_YoutubeURL $PlayVideo_Interval_Time &"
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/Youtube/Check_YoutubeStatus.sh $DiffPackets_ErrorThreshold $ErrorTimes_FailThreshold &"
            } >> "$ScheduleLogFile" 2>&1
            ExecuteCMD_Flag=1;

            sh /storage/emulated/0/Documents/Youtube/Youtube.sh $list_YoutubeURL $PlayVideo_Interval_Time &
            sh /storage/emulated/0/Documents/Youtube/Check_YoutubeStatus.sh $DiffPackets_ErrorThreshold $ErrorTimes_FailThreshold &
        fi;
    else
        if [ "$ExecuteCMD_Flag" -eq 1 ]; then
            {
                echo "[$(Get_CurrentDateTime)] Stop the scripts.";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'youtube'";
                echo "[$(Get_CurrentDateTime)] sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh 'youtube_monitor'";
                echo "--------------------------------------------------";
            } >> "$ScheduleLogFile" 2>&1
            ExecuteCMD_Flag=0;
        fi;
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "youtube";
        sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "youtube_monitor"
        {
            echo "Time : $(Get_CurrentDateTime)";
            echo "DiffPackets_ErrorThreshold : $DiffPackets_ErrorThreshold";
            echo "ErrorConsecutiveTimes_FailThreshold : $ErrorTimes_FailThreshold";
            echo "Result : Wait";
        } > "$GetPackets_CurrentResult_File" 2>&1;
    fi;
    sleep 1;
done;
