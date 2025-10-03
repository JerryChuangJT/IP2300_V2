#!/system/bin/sh
# Create Time : 2025/07/23
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Wifi/Delete_AllWiFiProfile.sh
#-----------------------------------------------------------------------------------
# Function : 
#       1. Search all of the WiFi profile that have connected.
#       2. Delete all Wifi profile from search result.
#       3. Record result in log. 
#		   $log_file(WifiDeleteProfile.log)
#       4. Delete log data that is over 60 days.

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
#--------------------------------------------------------------
### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Wifi"
Create_Folder "$LogDir"

### Create log file.
log_file="${LogDir}/Wifi_DeleteProfile.log";
{
    echo "StartTime: $(Get_CurrentDateTime)";
} >> $log_file 2>&1;

#--------------------------------------------------------------
current_date=$(Get_CurrentDateTime)
wifi_list=$(cmd wifi list-networks | tail -n +2) # 跳过表头
echo "[$current_date] cmd wifi list-networks" >> $log_file 2>&1;
echo -e "[$current_date] \n$wifi_list" >> $log_file 2>&1;

unique_network_ids=$(echo "$wifi_list" | awk '{print $1}' | sort -u);

echo "$unique_network_ids" | while read -r network_id; do
    echo "[$current_date] cmd wifi forget-network $network_id" >> $log_file 2>&1;
    wifi_delete=$(cmd wifi forget-network "$network_id");
    echo "[$current_date] $wifi_delete" >> $log_file 2>&1;
done
echo "----------------------------------------------------------------------" >> "$log_file" 2>&1;

