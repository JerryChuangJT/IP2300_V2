import telnetlib
import time

class TelNet():    
    def __init__(self, host:str, port:int=23, endtext:str=b"# ", timeout:int=3):
        self.host = host
        self.port = port
        self.endtext = endtext
        self.response_data = None
        self.timeout = timeout
        self.connection_Status = False     

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
            self.tn = telnetlib.Telnet(self.host, self.port, self.timeout)
            self.response_data = self.tn.read_until(self.endtext)
            self.connection_Status = True
        except:
            self.connection_Status = False

    '''
    Execute a command on the device and return the response.
    If the connection is lost, it will attempt to reconnect and retry the command.
    '''
    def Excecute_Command(self, command:str)->str:
        max_retries = 3
        for attempt in range(max_retries):
            ### Check connection status before executing command
            if not self.connection_Status:
                print(f"{self.host} : Attempt {attempt + 1}: Trying to reconnect...")
                self.Connect_Devcie()
                
            if self.connection_Status:
                try:
                    self.tn.write(command.encode('ascii') + b"\n")
                    self.response_data = self.tn.read_until(self.endtext, timeout=self.timeout).decode('ascii')
                    if self.response_data:
                        return ["PASS", self.response_data]
                    
                except Exception as e:
                    self.connection_Status = False  

        return ["FAIL", f"Connect device {self.host} failed after {max_retries} attempts."]

    def Disconnect_Device(self):
        if self.connection_Status:
            self.tn.close()
        self.connection_Status = False

if __name__ == "__main__":
    A = TelNet("192.168.5.153", 23)
    A.Connect_Devcie()
    time.sleep(3)
    print(A.Excecute_Command("ls /storage/emulated/0/Documents/Ping/"))