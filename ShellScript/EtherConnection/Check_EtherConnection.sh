
### sh /storage/emulated/0/Documents/EtherConnection/Check_EtherConnection.sh '192.168.5.1'

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
#-----------------------------------------------------------------------------------
SERVER_IP=$1

#### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Ether";
Create_Folder "$LogDir";
log_file="${LogDir}/EtherConnection.log";

#-----------------------------------------------------------------------------------
### Record new setting parameters.
current_date=$(Get_CurrentDateTime);
echo "Test Start : $current_date" > "$log_file" 2>/dev/null;
echo "Destination: $SERVER_IP" >> "$log_file" 2>/dev/null;
echo "----------------------------------------------------------------------" >> "$log_file" 2>/dev/null;
echo "----------------------------------------------------------------------" >> "$log_file" 2>/dev/null;

while true; do
    if ! ping -c 1 -W 2 "$SERVER_IP" > /dev/null 2>&1; then
        current_date=$(Get_CurrentDateTime);
        echo "[$current_date] Network unreachable. Restarting Ethernet interface..." >> "$log_file" 2>/dev/null;

        su root ifconfig eth0 down;
        echo "[$current_date] su root ifconfig eth0 down" >> "$log_file" 2>/dev/null;

        sleep 2;

        su root ifconfig eth0 up;
        echo "[$current_date] su root ifconfig eth0 up" >> "$log_file" 2>/dev/null;

        echo "----------------------------------------------------------------------" >> "$log_file" 2>/dev/null;
    fi;
    sleep 6;
done;