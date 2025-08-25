#================================================================================================
#================================================================================================
[ADB Execute Command] 
1. [Setting]
    Make sure three files is in the same floders before executing ADB_ExecuteCommand.tcl
    > ADBTelnet_ExecuteCommand.tcl
    > ADBTelnet_ExecuteCommand.json
 
2. [Variables_Explanation] Variables in ADB_ExecuteCommand.json.
    "list_DeviceIP" : List all devices on which you want to execute commands.
    "list_Command" : List all commands you want to executes.

3. [Local_Cmd_Command] 
    tclsh ADBTelnet_ExecuteCommand.tcl

#================================================================================================
#================================================================================================
[Ping Test Related Doocuments]
1. [adb] Push Files into IP2300.
    adb -s 192.168.0.5 push ping_script.sh storage/emulated/0/Documents/Ping
    adb -s 192.168.0.5 push Monitor_PingLostCount.sh storage/emulated/0/Documents/Ping
    adb -s 192.168.0.5 push Monitor_PingResponseLost.sh storage/emulated/0/Documents/Ping

2. [Telnet] Execute script with command line in IP2300.
    sh /storage/emulated/0/Documents/Ping/ping_script.sh "Test1" "8.8.8.8" &
    sh /storage/emulated/0/Documents/Ping/Monitor_PingLostCount.sh "Test1" "10" & 
    sh /storage/emulated/0/Documents/Ping/Monitor_PingResponseLost.sh "Test1" "1200" "60" "10" &

3. [adb] Pull Down Log File from IP2300. (ping test Result)
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/Test1_ping.log
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/Test1_ping_result.log
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/Test1_ping_addtime.log
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/Test1_ping_failsummary.log

4. [Variables_Explanation]
    sh ping_script.sh "AAA" "BBB"
        AAA : Name
        BBB : Destination Address,
        ex: sh ping_script.sh "Test1" "8.8.8."

    sh Monitor_PingLostCount.sh "AAA" "BBB"
        AAA : Name
        BBB : How Many continuous pings must be lost to be considered a Failure,
        ex: sh Monitor_PingLostCount.sh "Test1" "10"

    sh Monitor_PingResponseLost.sh "AAA" "BBB" "CCC" "DDD"
        AAA : Name
        BBB(ms) : How many response times exceeds to be considered a Response Error.
        CCC(s) : How Many times of Response Error to be considered a FAIL. 
        DDD : How many consecutive times of PingLost to be considered a FAIL.
        ex: sh Monitor_PingResponseLost.sh "Test1" "1200" "60" "10"

#================================================================================================
#================================================================================================
[Wi-Fi Reconnecting Related Document]
### Enviroment In Controller PC for Making IP2300 Connecting and Disconnecting Wifi Repeatly.
1. [Setting] 
    Make sure three files is in the same floders before executing ADB_WiFiCommand.tcl.
    > ADB_WiFiConnect.tcl
    > ADB_WiFiConnect.json
    > MyFunction.tcl

2. [Variables_Explanation] Variables in ADB_WiFiConnect.json.
    "list_DeviceIP" : List all the IP let you are going to test for connecting and disconnect Wi-Fi.
    "WiFi_SSID" : Wi-Fi SSID
    "WiFi_Auth" : Wi-Fi Authentication
    "WiFi_Password" : Wi-Fi Password
    "WiFi_BSSID" : Wi-Fi BSSID
    "TimeStamp"(min) : How many times for waiting to reconnect Wi-Fi again. 

3. [Local_Cmd_Command] 
    tclsh ADB_WiFiCommand.tcl

#----------------------------------------------------------------
### Connect Wifi and Check Connecting Status.
1. [adb] Push Files into IP2300.
    adb -s 192.168.0.5 push Check_WifiConnectionStatus.sh storage/emulated/0/Documents/Wifi
    adb -s 192.168.0.5 push Delete_AllWiFiPrlfile.sh storage/emulated/0/Documents/Wifi
    adb -s 192.168.0.5 push Set_WifiDriver.sh storage/emulated/0/Documents/Wifi

2. [Telnet] Execute script with command line in IP2300.
    sh /storage/emulated/0/Documents/Wifi/Check_WifiConnectionStatus.sh "1111_Verizon_5G" "wpa2" "12345678" "88:5a:85:fb:0f:4d" &
    sh /storage/emulated/0/Documents/Wifi/Delete_AllWiFiPrlfile.sh
    sh /storage/emulated/0/Documents/Wifi/Set_WifiDriver.sh "5G" "11a" "36" "20"
    sh /storage/emulated/0/Documents/Wifi/Check_WiFiIP.sh 

3. [adb] Pull Down Log File from IP2300. (ping test Result)
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/WifiConnection.log
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/WifiDeleteProfile.log
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/Wifi_SetDriverParameter.log   
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/WiFi_IP.log 
       
4. [Variables_Explanation]
    sh Check_WifiConnectionStatus.sh "AAA" "BBB" "CCC" "DDD"
        AAA : Wifi_SSID
        BBB : Wifi_Auth
        CCC : Wifi_Password
        DDD : Wifi_BSSID
        ex: sh ping_script.sh "1111_Verizon_5G" "wpa2" "12345678" "88:5a:85:fb:0f:4d"
    
    sh Delete_AllWiFiPrlfile.sh
    
    sh Set_Driver.sh "AAA" "BBB" "CCC" "DDD"
        AAA : Band Parameter
        BBB : Standard Parameter
        CCC : Cannel Parameter
        DDD : Bandwidth Parameter
        ex : sh Set_Driver.sh "5G" "11a" "36" "20"

    sh Check_WiFiIP.sh
        
#================================================================================================
#================================================================================================
[Plays Videos on Youtube Related Document] 
### Enviroment In Controller PC for Playing Youtube Video on IP2300 by ADB Comnmand.
### --- This Python File is Not Use in GUI. ---
1. [Setting]
    Make sure three files is in the same floders before executing Youtube.tcl
    > Youtube.tcl
    > MyFunction.tcl
    > Youtube.json
 
2. [Variables_Explanation] Variables in Youtube.json.
    "devices" : List all of the devices IP in lost type.
    "url" : List all of the url to play in devices.
    "interval_time" (min) : Sleep time between every videos.
    "Comment" : Script is not using this parameter, you can make notes here.

3. [Local_Cmd_Command] 
    tclsh Youtube.tcl

#----------------------------------------------------------------
### Check Youtube Playing Status by Counting TXPackets.
1. [adb] Push Files into IP2300.
	adb -s 192.168.0.5 push Youtube.sh storage/emulated/0/Documents/Youtube/
    	adb -s 192.168.0.5 push Check_YoutubeStatus.sh storage/emulated/0/Documents/Youtube/

2. [Telnet] Execute script with command line in IP2300.
	sh /storage/emulated/0/Documents/Youtube/Youtube.sh "https://www.youtube.com/watch?v=m_dhMSvUCIc,https://www.youtube.com/watch?v=V1p33hqPrUk" "0.1" "2,15:00,5/2,18:00,5/2,23:50,15" "30" &
    	sh /storage/emulated/0/Documents/Youtube/Check_YoutubeStatus.sh "100" "5" &

3. [adb] Pull Down Log File from IP2300. (ping test Result)
	adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/Youtube_PlayURL.log
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/YoutubePacket_GetPackets.log
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/YoutubePacket_FailSummary.log
    adb -s 192.168.0.5 pull /storage/emulated/0/Documents/Log/YoutubePacket_TestResult.log


4. [Variables_Explanation]
	sh Youtube.sh "AAA" "BBB"
		AAA: Youtube URL list. This value can contain mutiple urls. Remember to add "," between urls.
		BBB(min): The interval time between each video.
       		CCC : Weekday,StartTime.RunTime/Weekday,StartTime.RunTime/....
		DDD(sec) : When the time comes, how long should I wait before playing the video so that the wifi can be connected?

    	sh Check_YoutubeSatus.sh "AAA" "BBB"
        	AAA : How much differenct between receiving packets within 3 seconds will be judged as Error.
        	BBB : How many consecutive times of Error happens will be judged as Test Fail.
        	ex: sh Check_YoutubeSatus.sh "100" "5"

#================================================================================================
#================================================================================================
[Kill_Process]
1. [adb] Push File into IP2300.
    adb -s 192.168.0.5 push Check_YoutubeSatus.sh storage/emulated/0/Documents/KillProcess/

2. [Telnet] Execute script with command line in IP2300.
    sh /storage/emulated/0/Documents/KillProcess/KillProcess.sh "youtube"

3. [Variables_Explanation]
    sh KillProcess.sh "1"
        $1 : Which process needs to kill
            ping -> Ping_Script.sh
            test_ping -> Test_PingScript.sh
            ping_monitor -> Monitor_PingResponseLost.sh
            wifi_connect -> Check_WifiConnectionStatus.sh
            wifi_setdriver -> Set_WifiDriver.sh
            wifi_getip -> Check_WiFiIP.sh
            youtube -> Youtube.sh
            youtube_monitor -> Check_YoutubeStatus.sh