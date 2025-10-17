

======================================================================================================================
======================================================================================================================
1. Wifi_Connection.sh
    /Doucment/
        |--/Wifi/
            |-- (read) wifi_run_status      (write 'start' at first, and run until when it become 'stop')
            |-- (write) wifi_command_count  (write the count:0 at the first time, and increase 1 after each connection command.)
        |--/Log/Wifi/
            |-- (write) Wifi_ConnectionCommand.log  (every connection command will be recorded here, with time stamp.)
            |-- (*write*) Wifi_Connection_result.log  (only write after execute connection command, with time stamp.)
            |-- (write) Wifi_Count.log              (when wifi_run_status == 'stop', copy wifi_command_count to here.)    
    -----------------------------------------------------------------------------------------------------------------
    command_CheckLimitConnect="cmd wifi status | grep PARTIAL_CONNECTIVITY";
    Flag_ExecuteCommand=1;
    while true; do
        ### Check whether the wifi connection needs to be exectued.
        1. if $Flag_ExecuteCommand == 1:   
                execute wifi connection command => cmd wifi connect-network '$ssid' '$auth' '$password' -b '$bssid'
                [Wifi_ConnectionCommand.log] += "[$(Get_CurrentDateTime)] cmd wifi connect-network '$ssid' '$auth' '$password' -b '$bssid'\n"
                [wifi_command_count] += 1
                $Flag_ExecuteCommand = 0;
            fi;
        ### wait for 30 seconds
        2. for i in $(seq 1 30); do
                if [wifi_run_status] == "stop":
                    copy [wifi_command_count] ---> [Wifi_Count.log]
                    [Wifi_ConnectionCommand.log] += "[$(Get_CurrentDateTime)] Test Stop\n"
                    exit 0;
                fi;

                if [wifi_connect_status] != "Pass":
                    $Flag_ExecuteCommand = 1;
                    break;  
                fi;

                sleep 1;
            done;
        ### Check limited connection
        3. if $command_CheckLimitConnect is not empty, means limited connection happened:
                [Wifi_ConnectionCommand.log] += "[$(Get_CurrentDateTime)] command_CheckLimitConnect_Result.\n"
                Restart_NetworkInterface
                $Flag_ExecuteCommand = 1;
            fi;
    done;

======================================================================================================================
======================================================================================================================
2. Wifi_GetIP.sh
    /Document/
        |--/Wifi/
            |-- (read) getip_run_status     (write 'start' at first, and run until when it become 'stop')
        |--/Log/Wifi/
            |-- (write) Wifi_IP_result.log  (ipv4 & ipv6 & result will be recorded here, with time stamp.)
    -----------------------------------------------------------------------------------------------------------------
    Command_GetWlan0Ipv4="ip -4 addr show wlan0 | grep 'inet ' | awk '{print \$2}' | cut -d/ -f1"
    Command_GetWlan0Ipv6="ip -6 addr show wlan0 | grep 'inet6 ' | awk '{print \$2}' | cut -d/ -f1"
    while true; do
        ### get wifi ipv4 & ipv6
        ipv4=$(eval $Command_GetWlan0Ipv4);
        if ipv4 is not None || ipv6 is not None:
            [Wifi_IP_result,log] += ipv4 + ipv6 + "pass";
        else:
            [Wifi_IP_result,log] += "None" + "None" + "fail";
        fi;

        ### wait for 3 seconds
        for i in $(seq 1 3); do
            if [getip_run_status] == "stop":
                exit 0;
            fi;
            sleep 1;
    done;

======================================================================================================================
======================================================================================================================
3. Wifi_PingScript.sh
    /Document/
        |--/Log/Wifi/
            |-- (write) Wifi_Ping.log  (ping result will be recorded here, without time stamp.)
    -----------------------------------------------------------------------------------------------------------------
    PING_CMD="ping -I wlan0 ${Destination}";
    PING_CMD="ping6 -I wlan0 ${Destination}";
    ### If ping lost, the command will return non-zero value, so it needs while loop.
    while true; do
        $PING_CMD >> [Wifi_Ping.log]
        sleep 1  # Check every second
    done;

======================================================================================================================
======================================================================================================================
4. Wifi_CheckPing.sh
    /Document/
        |--/Wifi/
            |-- (write & read) wifi_ping_temp_file  (copy ping result from Wifi_Ping.log)
            |-- (write & read) Wifi_ping_start_line (record the start line number of this check)
            |-- (read) wifi_ping_run_status         (write 'start' at first, and run until when it become 'stop')
            |-- (write) Wifi_ping_rate              (record the ping rate % of this check)
        |--/Log/Wifi/
            |-- (read) Wifi_Ping.log                (ping result will be read from here)
            |-- (write) Wifi_Ping_addtime.log       (record the ping result with time stamp)
            |-- (write) Wifi_Ping_failsummary.log   (record the ping fail summary with time stamp)
            |-- (write) Wifi_Connection_result.log  (if ping rate < 80%, write "ping fail" here with time stamp)
            |-- (write) Wifi_Ping_rate.log          (record the ping rate % of this check with time stamp)
        
    -----------------------------------------------------------------------------------------------------------------
    ping_error_count = 0;
    while true; do
        pass_count=0;
        fail_count=0;
        response_total=0;

        ping_error_count=0;

        ### Check whether the ping check needs to be exectued. 
        if [wifi_ping_run_status] != "start":
            exit 0;
        fi;
        
        ### Read ping result from Wifi_Ping.log
        while (read ping result) => $line; do
            ### pass count
            if 'ttl' in $line:
                $pass_count += 1;
                $ping_error_count = 0;
                "Pass" > [Wifi_Connection_result.log];
            fi;

            ### fail count
            if 'ttl' not in $line:
                $fail_count += 1;
                $ping_error_count += 1;
            fi;

            ### reponse time count
            if 'time=' in $line:
                $response_total += response_time;
            fi;

            ### 
            if $ping_error_count == 5:
                "Fail" > [Wifi_Connection_result.log];
            fi;
        done;

        ### update pinrate file
        Update_PingRate_File $pass_count, $fail_count, $response_total;
    done;

















