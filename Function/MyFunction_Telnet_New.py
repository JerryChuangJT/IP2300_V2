import telnetlib
import time
import re

class TelNet():
    """
    簡潔的 Telnet 類別，提供三個核心功能：
    1. 檢查連線 (check_connection)
    2. 執行命令 (execute_command) - 自帶重試機制
    3. 關閉連線 (disconnect)
    """
    
    def __init__(self, host: str, port: int = 23, timeout: int = 3, prompt: str = "# "):
        """
        初始化 Telnet 連線參數
        
        Args:
            host: 目標主機 IP
            port: Telnet 埠號 (預設 23)
            timeout: 命令執行超時時間 (秒)
            prompt: 命令結束提示符 (預設 "# ")
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.prompt = prompt.encode('ascii')
        self.connection = None
    """清理 Telnet 輸出，移除控制字符和空行"""
    def _clean_output(self, raw_text: str) -> str:
        if not raw_text:
            return ""
        
        cleaned = raw_text.replace('\x08', '').replace('\r', '\n')
        lines = [line.strip() for line in cleaned.split('\n') if line.strip()]
        return '\n'.join(lines)
    """
    檢查是否可以連線到目標設備

    Returns:
    bool: True 表示可以連線，False 表示無法連線
    """
    def check_connection(self) -> bool:
        try:
            test_conn = telnetlib.Telnet(self.host, self.port, timeout=self.timeout)
            test_conn.close()
            return ["PASS"]
        except Exception as e:
            print(f"Connection check failed for {self.host}:{self.port} - {e}")
            return ["FAIL"]
    
    def _connect(self) -> bool:
        """
        內部方法：建立連線
        
        Returns:
            bool: 連線是否成功
        """
        try:
            # 關閉現有連線
            if self.connection:
                try:
                    self.connection.close()
                except:
                    pass
            
            # 建立新連線
            self.connection = telnetlib.Telnet(self.host, self.port, timeout=self.timeout)
            # 等待初始提示符
            self.connection.read_until(self.prompt, timeout=self.timeout)
            return True
            
        except Exception as e:
            print(f"Connect failed for {self.host} - {e}")
            self.connection = None
            return False

    """
    執行命令，自帶重試機制

    Args:
    command: 要執行的命令
    max_retries: 最大重試次數 (預設 3 次)

    Returns:
    dict: {
        'success': bool,     # 命令是否執行成功
        'data': str,         # 回傳的數據
        'error': str         # 錯誤訊息 (如果有)
    }
    """
    def execute_command(self, command: str, max_retries: int = 3) -> dict:

        for attempt in range(max_retries):
            try:
                # 檢查連線狀態，必要時重新連線
                if not self.connection:
                    print(f"{self.host} - Attempt {attempt + 1}: Connecting...")
                    if not self._connect():
                        continue
                
                # 發送命令
                self.connection.write(command.encode('ascii') + b'\n')
                
                # 讀取回應
                raw_response = self.connection.read_until(self.prompt, timeout=self.timeout)
                response_text = raw_response.decode('ascii', errors='ignore')
                
                # 檢查是否收到完整回應
                if not response_text.endswith(self.prompt.decode('ascii')):
                    print(f"{self.host} - Attempt {attempt + 1}: Incomplete response, retrying...")
                    self.connection = None  # 標記為需要重新連線
                    continue
                
                # 清理輸出
                clean_data = self._clean_output(response_text)
                
                return {
                    'success': True,
                    'data': clean_data,
                    'error': None
                }
                
            except Exception as e:
                print(f"{self.host} - Attempt {attempt + 1}: Exception - {e}")
                self.connection = None  # 標記為需要重新連線
                time.sleep(0.5)  # 短暫等待後重試
        
        # 所有重試都失敗
        return {
            'success': False,
            'data': '',
            'error': f"Command failed after {max_retries} attempts"
        }
    
    def disconnect(self):
        """關閉 Telnet 連線"""
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            finally:
                self.connection = None
        print(f"Disconnected from {self.host}")


# 使用範例
if __name__ == "__main__":
    # 創建 Telnet 物件
    telnet = TelNet("192.168.5.153", port=23, timeout=3)
    
    # 1. 檢查連線
    if telnet.check_connection():
        print("✓ 設備可以連線")
        
        # 2. 執行命令
        result = telnet.execute_command("ls /storage/emulated/0/Documents/")
        if result['success']:
            print("✓ 命令執行成功")
            print("回傳數據:", result['data'])
        else:
            print("✗ 命令執行失敗:", result['error'])
        
        # 3. 關閉連線
        telnet.disconnect()
    else:
        print("✗ 設備無法連線")