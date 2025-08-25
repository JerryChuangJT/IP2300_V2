#!/system/bin/sh
# Create Time : 2025/07/21
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Youtube/Check_YoutubeStatus.sh "100" "5"

#-----------------------------------------------------------------------------------
# Function : 
#       1. Check the RX packets difference every 3 seconds. 
#           If the difference is less than DiffPackets_ErrorThreshold, it will record the error in the log file.

#       2. If the error occurs more than ErrorTimes_FailThreshold times, it will stop the script and log the failure.

#       3. Log [YoutubePacket_GetPackets.log]
#           Recording the RX packets and the difference between them.

#       4. Log [YoutubePacket_FailSummary.log]
#           Recording the error summary when the script fails.

#       5. Log [YoutubePacket_TestResult.log]
#           Recording the test result, including the start time, error threshold, and whether the test passed or failed.

#       6. temp [youtube_monitor_status]
#           A file to check if the script should continue running or not.

#       7. temp [youtube_play_status]
#           A file to notify whether the video is playing successfully or not.

#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : DiffPackets_ErrorThreshold - The threshold for the difference in RX packets to consider it an error.
#           ex: "100" (100 packets).

#       $2 : ErrorTimes_FailThreshold - The number of consecutive errors required to consider the test failed.  
#           ex: "5" (5 consecutive errors).

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
    local DateTimeNow=$(date "+%Y-%m-%d %H:%M:%S");
    echo "$DateTimeNow";
};

Get_CurrentTimeStamp() {
    local TimeStampNow=$(date +%s);
    echo "$TimeStampNow";
};

Count_TimeDifferent() {
    local start=$1
    local end=$2
    local diff=$(echo "$end - $start" | bc)
    printf "%.3f\n" "$diff"
};

Add_RXPacket2_Info() {
    local DateTimeNow_2=$1
    local RXPacket_2=$2
    local RXPacket_Diff=$3
    {
        echo "[$DateTimeNow_2] RXPacket_2 -> $RXPacket_2";
        echo "[$DateTimeNow_2] RXPacket_Diff -> $RXPacket_Diff";
        echo "---------------------------------------";
    } >> "$LogFile_GetRXPackets" 2>&1;
};

Update_YoutubeResult_File() {
    local result="$1";
    local CurrentTime=$(Get_CurrentDateTime);

    {
        echo "Time : $CurrentTime";
        echo "DiffPackets_ErrorThreshold : $DiffPackets_ErrorThreshold";
        echo "ErrorConsecutiveTimes_FailThreshold : $ErrorTimes_FailThreshold";
        echo "Result : $result";
    } > "$LogFile_TestResult" 2>&1;
};

#--------------------------------------------------------------
### Variables
DiffPackets_ErrorThreshold=$1;
ErrorTimes_FailThreshold=$2;

#--------------------------------------------------------------
#### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Youtube"
Create_Folder "$LogDir"

LogFile_GetRXPackets="${LogDir}/YoutubePacket_GetPackets.log";
LogFile_FailSummary="${LogDir}/YoutubePacket_FailSummary.log";
LogFile_TestResult="${LogDir}/YoutubePacket_result.log";

### Using root permission
TestStart_Time=$(Get_CurrentDateTime);
{
    echo "======================================================================";
    echo "Test Start : $TestStart_Time";
    echo "DiffPackets_ErrorThreshold : $DiffPackets_ErrorThreshold";
    echo "ErrorConsecutiveTimes_FailThreshold : $ErrorTimes_FailThreshold";
    echo "----------------------------------------------------------------------";
} >> "$LogFile_GetRXPackets" 2>&1;

{
    echo "======================================================================";
    echo "Test Start : $TestStart_Time";
    echo "DiffPackets_ErrorThreshold : $DiffPackets_ErrorThreshold";
    echo "ErrorConsecutiveTimes_FailThreshold : $ErrorTimes_FailThreshold";
    echo "----------------------------------------------------------------------";
} >> "$LogFile_FailSummary" 2>&1;

Update_YoutubeResult_File "PASS";

#--------------------------------------------------------------
### [temp] executestatus_file for checking youtube monitor should keeping running or not.
### [temp] playstatus_file for notifing youtube whether the video is playing successfully or not. 
executestatus_file="/storage/emulated/0/Documents/Youtube/monitor_run_status";
playstatus_file="/storage/emulated/0/Documents/Youtube/youtube_video_status";
echo "Start" > "$executestatus_file" 2>&1;
echo "Start" > "$playstatus_file" 2>&1;

### ========================================================================================
### ========================================================================================
### Main Code.
### Get RX Packets Command.
Network_Driver="wlan0";
command_GetRXPackets="ifconfig $Network_Driver | grep 'RX packets' | sed -n 's/.*RX packets:\([0-9]*\).*/\1/p'";
Error_StartTime=$(Get_CurrentDateTime);
ErrorTimes=0;

while true; do
    #---------------------------------------------------------
    ### Get Current TimeStamp.
    DateTimeNow_1=$(Get_CurrentDateTime); 
    RXPacket_1=$(eval "$command_GetRXPackets");
    echo "[$DateTimeNow_1] RXPacket_1 -> $RXPacket_1" >> "$LogFile_GetRXPackets" 2>&1;

    #---------------------------------------------------------
    ### Wait for 3 seconds and check current is in time range or not.
    ### Check Execute Status.
    ### If the status is not "Start", then exit the loop.
    seconds_elapsed=0;
    while (( seconds_elapsed < 3 )); do
        execute_status=$(cat "$executestatus_file" 2>&1);
        if [ "$execute_status" != "Start" ]; then
            DateTimeNow_2=$(Get_CurrentDateTime); 
            RXPacket_2=$(eval "$command_GetRXPackets");
            RXPacket_Diff=$(expr $RXPacket_2 - $RXPacket_1);
            Add_RXPacket2_Info "$DateTimeNow_2" "$RXPacket_2" "$RXPacket_Diff";
            return 0;
        fi;
        seconds_elapsed=$((seconds_elapsed + 1));
        sleep 1;
    done;

    #---------------------------------------------------------
    ### Get Packet 2 and calculate the difference.
    DateTimeNow_2=$(Get_CurrentDateTime); 
    RXPacket_2=$(eval "$command_GetRXPackets");
    RXPacket_Diff=$(expr $RXPacket_2 - $RXPacket_1);
    Add_RXPacket2_Info "$DateTimeNow_2" "$RXPacket_2" "$RXPacket_Diff";

    ### Check the difference between RXPacket_1 and RXPacket_2 whether it is greater than DiffPackets_ErrorThreshold.
    ### Recored Fail data in LogFile_FailSummary.
    if [ $RXPacket_Diff -lt $DiffPackets_ErrorThreshold ]; then
        ErrorTimes=$((ErrorTimes + 1));
        {
            echo "[$DateTimeNow_1 - $DateTimeNow_2] RXPacket_Diff -> $RXPacket_Diff";
            echo "[$DateTimeNow_1 - $DateTimeNow_2] ErrorTimes : $ErrorTimes";
            echo "----------------------------------------------------------------------";
        } >> "$LogFile_FailSummary" 2>&1;
    else
        Update_YoutubeResult_File "PASS";
        ErrorTimes=0;
        echo "Pass" > "$playstatus_file" 2>&1;
    fi;

    #---------------------------------------------------------
    ### Check ErrorTimes whether it is greater than ErrorConsecutiveTimes_FailThreshold.    
    if [ $ErrorTimes -ge $ErrorTimes_FailThreshold ]; then
        echo "ErrorTimes -> $ErrorTimes";
        ErrorTimes=0;
        Update_YoutubeResult_File "FAIL";
        echo "Fail" > "$playstatus_file" 2>&1;
    fi;
done;

