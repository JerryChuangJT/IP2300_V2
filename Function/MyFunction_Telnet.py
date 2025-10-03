import telnetlib
import time
import re
import traceback    

class TelNet():    
    def __init__(self, host:str, port:int=23, endtext:str=b"# ", timeout:int=2):
        self.host = host
        self.port = port
        self.endtext = endtext
        self.timeout = timeout
        self.connection_Status = False

        self.response_data = None
    
    def clean_output(self, raw_output):        
        ### 移除常見的控制字符
        cleaned = raw_output.replace('\x08', '')    # 退格鍵
        cleaned = cleaned.replace('\r', '\n')       # 回車改成換行
        
        ### 分割成行，移除空行
        lines = cleaned.split('\n')
        clean_lines = []
        
        for line in lines:
            line = line.strip()                     # 移除前後空白
            if line and line != '#':                # 忽略空行和單獨的提示符
                clean_lines.append(line)
        
        return '\n'.join(clean_lines)

    def Check_Connection(self)->str:
        try:
            self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
            self.tn.close()
            return ["PASS"]
        except:
            return ["FAIL"]
        
    '''
    Connect to the device using Telnet.
    If the connection is successful, it sets the connection_Status to True.
    '''
    def Connect_Devcie(self):
        try:
            ### 先關閉舊連接（如果存在）- 使用快速關閉方式
            if hasattr(self, 'tn') and self.tn:
                try:
                    ### 嘗試快速關閉，但不等太久
                    self.tn.sock.settimeout(0.5)  # 更短的超時
                    self.tn.close()
                except:
                    pass
                finally:
                    ### 無論如何都設為 None
                    self.tn = None
            
            self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
            self.response_data = self.tn.read_until(self.endtext, timeout=self.timeout).decode('ascii')
            self.connection_Status = True

        except Exception as e:
            self.tn = None  # 確保失敗時設置為 None
            self.connection_Status = False

    '''
    Execute a command on the device and return the response.
    If the connection is lost, it will attempt to reconnect and retry the command.
    '''
    def Execute_Command(self, command:str)->str:
        ### Retry 2 times if connection fails.
        max_retries = 2
        for attempt in range(max_retries):

            ### Check connection status, if not connected, try to connect.
            if self.connection_Status == False:
                self.Connect_Devcie()

            ### If connected, try to send command and read response.
            if self.connection_Status:
                try:
                    self.tn.write(command.encode('ascii') + b"\n")
                    raw_response = self.tn.read_until(self.endtext, timeout=self.timeout).decode('ascii')

                    ### if response ends with prompt, consider it successful.
                    if raw_response.endswith('# '):
                        clean_response = self.clean_output(raw_response)
                        return ["PASS", clean_response]
                    
                    ### If response does not end with prompt, consider it failed and retry.
                    else:
                        self.connection_Status = False

                except Exception as e:
                    self.connection_Status = False

        return ["FAIL", f"Connect device {self.host} failed after {max_retries} attempts."]

    def Disconnect_Device(self):
        if self.connection_Status and self.tn is not None:
            try:
                ### 設定短超時避免 close() 卡住
                self.tn.sock.settimeout(0.5)  # 0.5 秒超時
                self.tn.close()
            except:
                pass
            finally:
                ### 無論如何都清理狀態
                self.tn = None
                self.connection_Status = False
        else:
            ### 即使沒有連線也要清理狀態
            self.tn = None
            self.connection_Status = False

if __name__ == "__main__":
    A = TelNet("192.168.5.153", 23)
    A.Connect_Devcie()
    time.sleep(3)
    print(A.Execute_Command("ls /storage/emulated/0/Documents/Ping/"))