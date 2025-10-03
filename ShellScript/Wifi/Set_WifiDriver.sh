#!/system/bin/sh
# Create Time : 2025/07/23
# Author : Jerry Chunag
#-----------------------------------------------------------------------------------
# Run command : 
#       sh /storage/emulated/0/Documents/Wifi/Set_WiFiDriver.sh "5G" "11a" "36" "20"

#-----------------------------------------------------------------------------------
# Function : 
#       1. Set Wifi Driver Parameters. Band, Standart and Bandwidth.
#       2. Record result in log. 
#		   $log_file(Wifi_SetDriverParameter.log)
#       3. Need 10 seconds to set driver parameters.
#-----------------------------------------------------------------------------------
# Variables : 
#       $1 : Band Parameter. 
#           ex: "Defaule" / "5G" / "2G".

#       $2 : Standard Parameter.
#           ex: "Auto" / "11a" / "11b" / "11g" / "11n" / "11ac" / "11ax"

#       $3 : Cannel Parameter.
#           ex: "Auto" / "7" / "36" 

#       $4 : Bandwidth Parameter.
#           ex: "Auto" / "20" / "40" / "80"

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

#-----------------------------------------------------------------------------------
SetDriver_11a() {
    ### Variables.
    Log_Path=$1
    Band=$2
    Channel=$3
    BandWidth=$4

    ### Set Driver Paramter.
    ### BandWidth : 20, 40, 80
    current_date=$(Get_CurrentDateTime);
    if [ "$Band" == "5G" ]; then

        ### Set Bandwidth if Bandwidth is not "Auto".
        if [ "$BandWidth" == "Auto" ]; then
            wl 5g_rate -r 54;
            echo "[$current_date] 5g_rate -r 54" >> "$Log_Path" 2>&1;
        else
            wl 5g_rate -r 54 -b $BandWidth;
            echo "[$current_date] 5g_rate -r 54 -b $BandWidth" >> "$Log_Path" 2>&1;
        fi;
    fi;
};

SetDriver_11b() {
    ### Variables.
    Log_Path=$1
    Band=$2
    Channel=$3
    BandWidth=$4

    ### Set Driver Parameter.
    ### BandWidth : 20
    current_date=$(Get_CurrentDateTime);
    if [ "$Band" == "2G" ]; then

        ### Set Bandwidth if Bandwidth is not "Auto".
        if [ "$BandWidth" == "Auto" ]; then
            wl 2g_rate -r 11;
            echo "[$current_date] wl 2g_rate -r 11" >> "$Log_Path" 2>&1;
        else
            wl 2g_rate -r 11 -b $BandWidth;
            echo "[$current_date] 2g_rate -r 11 -b $BandWidth" >> "$Log_Path" 2>&1;
        fi;
    fi;
};

SetDriver_11g() {
    ### Variables.
    Log_Path=$1
    Band=$2
    Channel=$3
    BandWidth=$4

    ### Set Driver Parameter.
    ### BandWidth : 20 
    current_date=$(Get_CurrentDateTime);
    if [ "$Band" == "2G" ]; then

        ### Set Bandwidth if Bandwidth is not "Auto".
        if [ "$BandWidth" == "Auto" ]; then
            wl 2g_rate -r 54;
            echo "[$current_date] wl 2g_rate -r 54" >> "$Log_Path" 2>&1;
        else
            wl 2g_rate -r 54 -b $BandWidth;
            echo "[$current_date] 2g_rate -r 54 -b $BandWidth" >> "$Log_Path" 2>&1;
        fi;
    fi;
};

SetDriver_11n() {
    ### Variables.
    Log_Path=$1
    Band=$2
    Channel=$3
    BandWidth=$4

    ### Set Driver Parameter.
    ### BandWidth : 20
    current_date=$(Get_CurrentDateTime);
    if [ "$Band" == "2G" ]; then

        ### Set Bandwidth if Bandwidth is not "Auto".
        if [ "$BandWidth" == "Auto" ]; then
            wl 2g_rate -h 7;
            echo "[$current_date] 2g_rate -h 7" >> "$Log_Path" 2>&1;
        else
            wl 2g_rate -h 7 -b $BandWidth;
            echo "[$current_date] 2g_rate -h 7 -b $BandWidth" >> "$Log_Path" 2>&1;
        fi;
    fi;

    ### BandWidth : 20, 40, 80
    if [ "$Band" == "5G" ]; then

            ### Set Bandwidth if Bandwidth is not "Auto".
        if [ "$BandWidth" == "Auto" ]; then
            wl 5g_rate -h 7;
            echo "[$current_date] 2g_rate -h 7" >> "$Log_Path" 2>&1;
        else
            wl 5g_rate -h 7 -b $BandWidth;
            echo "[$current_date] 2g_rate -h 7 -b $BandWidth" >> "$Log_Path" 2>&1;
        fi;
    fi;
};

SetDriver_11ac() {
    ### Variables.
    Log_Path=$1
    Band=$2
    Channel=$3
    BandWidth=$4

    ### Set Driver Parameter.
    ### BandWidth : 20, 40, 80
    current_date=$(Get_CurrentDateTime);
    if [ "$Band" == "5G" ]; then

        ### Set Bandwidth if Bandwidth is not "Auto".
        if [ "$BandWidth" == "Auto" ]; then
            wl 5g_rate -v 9 -s 1 --ldpc;
            echo "[$current_date] 5g_rate -v 9 -s 1 --ldpc" >> "$Log_Path" 2>&1;
        else
            wl 5g_rate -v 9 -s 1 --ldpc -b $BandWidth;
            echo "[$current_date] 5g_rate -v 9 -s 1 --ldpc -b $BandWidth" >> "$Log_Path" 2>&1;
        fi;
    fi;
};

SetDriver_11ax() {
    ### Variables.
    Log_Path=$1
    Band=$2
    Channel=$3
    BandWidth=$4

    ### Set Driver Parameter.
    ### BandWidth : 20
    current_date=$(Get_CurrentDateTime);
    if [ "$Band" == "2G" ]; then

        ### Set Bandwidth if Bandwidth is not "Auto".
        if [ "$BandWidth" == "Auto" ]; then
            wl 2g_rate -e 8 -s 1;
            echo "[$current_date] 2g_rate -e 8 -s 1" >> "$Log_Path" 2>&1;
        else
            wl 2g_rate -e 8 -s 1 -b $BandWidth;
            echo "[$current_date] 2g_rate -e 8 -s 1 -b $BandWidth" >> "$Log_Path" 2>&1;
        fi;
    fi;

    ### BandWidth : 20, 40, 80
    if [ "$Band" == "5G" ]; then

        ### Set Bandwidth if Bandwidth is not "Auto".
        if [ "$BandWidth" == "Auto" ]; then
            wl 5g_rate -e 9 -s 1;
            echo "[$current_date] 5g_rate -e 9 -s 1" >> "$Log_Path" 2>&1;
        else
            wl 5g_rate -e 9 -s 1 -b $BandWidth;
            echo "[$current_date] 5g_rate -e 9 -s 1 -b $BandWidth" >> "$Log_Path" 2>&1;
        fi;
    fi;
};

###-----------------------------------------------------------------------------------
#### Make Log Folder
LogDir="/storage/emulated/0/Documents/Log/Wifi";
Create_Folder "$LogDir";

###-----------------------------------------------------------------------------------
### Variables.
Parameter_Band=$1;
Parameter_Standard=$2;
Parameter_Channel=$3
Parameter_Bandwidth=$4;

### Create Log File.
log_file="${LogDir}/Wifi_SetDriverParameter.log";
current_date=$(Get_CurrentDateTime)
{
    echo "StartTime : $current_date";
    echo "Parameter_Band : $Parameter_Band";
    echo "Parameter_Standard : $Parameter_Standard";
    echo "Parameter_Channel : $Parameter_Channel";
    echo "Parameter_Bandwidth : $Parameter_Bandwidth";
} >> "$log_file" 2>&1;

###===================================================================================
### Check Channel or Bnadwidth need to set to "Auto" or not.
current_date=$(Get_CurrentDateTime)
if [ "$Parameter_Band" = "Default" ] || [ "$Parameter_Channel" = "Auto" ] || [ "$Parameter_Standard" = "Auto" ] || [ "$Parameter_Bandwidth" = "Auto" ]; then
    svc wifi disable;
    echo "[$current_date] svc wifi disable" >> "$log_file" 2>&1;
    sleep 1;

    svc wifi enable
    echo "[$current_date] svc wifi enable" >> "$log_file" 2>&1;
    sleep 1;

fi;

### Before setting parameter of wifi driver, remember to turn off "RF Function" first.
### Turn Off RF function.
wl down;
echo "[$current_date] wl down" >> "$log_file" 2>&1;
sleep 2;

### -----------------------------------------------
### Set Band.
current_date=$(Get_CurrentDateTime)

if [ "$Parameter_Band" == "2G" ]; then
    wl band b;
    echo "[$current_date] wl band b (a => 5G, b => 2G)" >> "$log_file" 2>&1;
    sleep 2;
fi;

if [ "$Parameter_Band" == "5G" ]; then
    wl band a;
    echo "[$current_date] wl band a (a => 5G, b => 2G)" >> "$log_file" 2>&1;
    sleep 2;
fi;

### -----------------------------------------------
### Set Channel
if [ "$Parameter_Channel" != "Auto" ]; then
    wl channel $Parameter_Channel;
    echo "[$current_date] wl channel $Parameter_Channel" >> "$log_file" 2>&1;
    sleep 1;
fi;

### -----------------------------------------------
### Set Standard.
if [ "$Parameter_Standard" == "11a" ]; then
    SetDriver_11a $log_file $Parameter_Band $Parameter_Channel $Parameter_Bandwidth;
fi;

if [ "$Parameter_Standard" == "11b" ]; then
    SetDriver_11b $log_file $Parameter_Band $Parameter_Channel $Parameter_Bandwidth;
fi;

if [ "$Parameter_Standard" == "11g" ]; then
    SetDriver_11g $log_file $Parameter_Band $Parameter_Channel $Parameter_Bandwidth;
fi;

if [ "$Parameter_Standard" == "11n" ]; then
    SetDriver_11n $log_file $Parameter_Band $Parameter_Channel $Parameter_Bandwidth;
fi;

if [ "$Parameter_Standard" == "11ac" ]; then
    SetDriver_11ac $log_file $Parameter_Band $Parameter_Channel $Parameter_Bandwidth;
fi;

if [ "$Parameter_Standard" == "11ax" ]; then
    SetDriver_11ax $log_file $Parameter_Band $Parameter_Channel $Parameter_Bandwidth;
fi;

sleep 1;

### -----------------------------------------------
### Turn On RF function.
current_date=$(Get_CurrentDateTime)
wl up;
echo "[$current_date] wl up" >> "$log_file" 2>&1;
sleep 2;
echo "--------------------------------------------------------------" >> "$log_file" 2>&1;

