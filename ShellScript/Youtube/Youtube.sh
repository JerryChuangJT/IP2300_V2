#!/system/bin/sh
# Create Time : 2025/07/21
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Youtube/Youtube.sh "https://www.youtube.com/watch?v=m_dhMSvUCIc,https://www.youtube.com/watch?v=V1p33hqPrUk" "1"

#-----------------------------------------------------------------------------------
# Function :
#       1. Execute YouTube URLs in a shuffled order.
#           The URLs will be played in the background.
#           The URLs will be executed every Interval_Time minutes.
#           The URLs will be logged in the file ${LogDir}/Youtube_PlayUrlCommand.log.

#       2. Log [Youtube_PlayUrlCommand.log]
#           Recording all the cmd execution and the YouTube URLs.

#       3. Log [Youtube_Count.log]
#           Recording the start time, current time, YouTube URL list, and the count of executed URLs.

#       4. temp [youtube_execute_status]
#           This file is used to check if the script is running.
#           If the content is not "Start", the script will stop executing URLs.

#       5. temp [youtube_play_status]
#           This file is used to check if the script is ready to play the next URL. 

#       6. temp [youtube_execute_url_count]
#           This file is used to record the count of executed URLs.

#-----------------------------------------------------------------------------------
# Variables :
#       $1 : YouTube URL list, separated by commas.
#           ex: "https://www.youtube.com/watch?v=m_dhMSvUCIc,https://www.youtube.com/watch?v=V1p33hqPrUk"
#       $2 : Interval time in minutes.
#           ex: "1" (1 minute).

#-----------------------------------------------------------------------------------
Get_CurrentDateTime() {
    local DateTimeNow=$(date "+%Y-%m-%d %H:%M:%S.%3N");
    echo "$DateTimeNow";
};

Get_CurrentTimeStamp() {
    local TimeStampNow=$(date +%s);
    echo "$TimeStampNow";
};

Count_TimeDifferent() {
    local start=$1;
    local end=$2;
    local diff=$(echo "$end - $start" | bc);
    printf "%.3f\n" "$diff";
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

### 打亂 youtube_urls 順序的函數
shuffle_array() {
    local i tmp size rand

    # 取得陣列大小
    size=${#youtube_urls[@]}
    i=$((size-1))
    
    # Fisher-Yates 洗牌算法
    while [ $i -gt 0 ]; do
        # 產生 0 到 i 的隨機數
        rand=$((RANDOM % (i+1)))
        
        # 交換元素
        tmp=${youtube_urls[i]}
        youtube_urls[i]=${youtube_urls[rand]}
        youtube_urls[rand]=$tmp

        # 遞減 i
        i=$((i-1))
    done
}

Execute_Commmand() {
    local command="$1";
    eval "$command" 2>&1;
    echo "[$(Get_CurrentDateTime)] $command" >> "$LogFile_YoutubeCommand" 2>&1;
}

Add_ExecuteURL_Count() {
    local start_time=$(grep "StartTime" "$url_count_file" | awk -F': ' '{print $2}')
    local current_time=$(Get_CurrentDateTime)
    local current_count=$(grep "YoutubeURLCount" "$url_count_file" | awk -F': ' '{print $2}')
    
    current_count=$((current_count + 1))
    {
        echo "StartTime : $start_time";
        echo "Time: $current_time";
        echo "list_YoutubeURL=$list_YoutubeURL";
        echo "Youtube Sequence : ${youtube_urls[@]}";
        echo "YoutubeURLCount: $current_count";
        echo "----------------------------------------------------------------------"
    } > "$url_count_file" 2>&1;

}

#--------------------------------------------------------------
### Get parameters.
### $1 : Youtube URL list, separated by commas.
### $2 : Interval time in minutes.
### Example: sh Youtube.sh "https://www.youtube.com/watch?v=m_dhMSv
list_YoutubeURL="$1";
Interval_Time="$2";

### 使用 read 和 IFS 分割
OLD_OFS=$IFS
IFS=','
youtube_urls=($list_YoutubeURL)
IFs=$OLD_OFS
shuffle_array 

#--------------------------------------------------------------
### Make Log Directory.
LogDir="/storage/emulated/0/Documents/Log/Youtube";
Create_Folder "$LogDir";

### Create log file.
LogFile_YoutubeCommand="$LogDir/Youtube_PlayUrlCommand.log";
LogFile_YoutubeCount="$LogDir/Youtube_Count.log";

StartTime=$(Get_CurrentDateTime);
{
    echo "=======================================================================";
    echo "StartTime : $StartTime";
    echo "YoutubeURLList : $list_YoutubeURL";
    echo "Youtube Sequence : ${youtube_urls[@]}";
    echo "IntervalTime : $Interval_Time min";
} >> "$LogFile_YoutubeCommand" 2>&1;

#--------------------------------------------------------------
### Create execute status file.
### This file is used to check if the script is running.
executestatus_file="/storage/emulated/0/Documents/Youtube/youtube_run_status";
playstatus_file="/storage/emulated/0/Documents/Youtube/youtube_video_status";
url_count_file="/storage/emulated/0/Documents/Youtube/youtube_execute_url_count";

echo "Start" > "$executestatus_file" 2>&1;
echo "Pass" > "$playstatus_file" 2>&1;
{
    echo "StartTime : $StartTime";
    echo "Time: $StartTime";
    echo "list_YoutubeURL=$list_YoutubeURL";
    echo "Youtube Sequence : ${youtube_urls[@]}";
    echo "YoutubeURLCount: 0";
    echo "----------------------------------------------------------------------"
} > "$url_count_file" 2>&1;

### ========================================================================================
### ========================================================================================
### Interval_Time_Seconds for checking the time interval.
### TimeStamp_StartVideo is used to record the start time of the video playback.
Interval_Time_Seconds=$((Interval_Time * 60));
TimeStamp_StartVideo=$(Get_CurrentTimeStamp);
Flag_executeURL=1;
url_int=0;
while true; do
    # echo "${youtube_urls[0]}"
    # echo "${youtube_urls[1]}"
    ###------------------------------------------------------------------------------------------------
    ### Check Play Status.
    ### If play_status is not "Pass" => Flag_executeURL=1
    play_status=$(cat "$playstatus_file" 2>&1);
    if [ "$play_status" != "Pass" ]; then
        Flag_executeURL=1;
        echo "Pass" > "$playstatus_file" 2>&1;
    fi;

    ###------------------------------------------------------------------------------------------------
    ### Check Execute Status.
    ### Flag_executeURL=1, means there is something wrong when playing the video.
    ### Execute the youtube URL again.
    if [ $Flag_executeURL -eq 1 ]; then
        Flag_executeURL=0;
        url="${youtube_urls[$url_int]}";
        command_PlayYoutubeURL="am start -n com.google.android.youtube.tv/com.google.android.apps.youtube.tv.activity.ShellActivity -a android.intent.action.VIEW -d $url"
        Execute_Commmand $command_PlayYoutubeURL;
        Add_ExecuteURL_Count;
    fi;

    ###------------------------------------------------------------------------------------------------
    ### If Time Interval > Interval_Time_Seconds.
    ### Flag_executeURL=1
    ### TimeStamp_StartVideo=$(Get_CurrentTimeStamp);
    ### Check if the URL index is within bounds.
    TimeStamp_Current=$(Get_CurrentTimeStamp);
    time_diff=$((TimeStamp_Current - TimeStamp_StartVideo));
    if [ $time_diff -ge $Interval_Time_Seconds ]; then
        Flag_executeURL=1;
        TimeStamp_StartVideo=$(Get_CurrentTimeStamp);

        ### Check url_int is within bounds.
        ### To make sure url_int does not exceed the length of youtube_urls.
        url_int=$((url_int + 1));
        if [ $url_int -ge ${#youtube_urls[@]} ]; then
            url_int=0;  
        fi;
    fi;

    #---------------------------------------------------------
    ### Wait for 10 seconds and check current is in time range or not.
    ### Check Execute Status.
    ### Stop Youtube App.
    for i in $(seq 1 30); do
        execute_status=$(cat "$executestatus_file" 2>/dev/null);
        if [ "$execute_status" != "Start" ]; then
            if [ -f "$url_count_file" ]; then
                cat "$url_count_file" >> "$LogFile_YoutubeCount" 2>&1;
            fi;
            command_StopYoutube="am force-stop com.google.android.youtube.tv";
            Execute_Commmand "$command_StopYoutube";
            return 0;
        fi;
        sleep 1;
    done;
done;
