import serial
import time
import sys

class GRBLServoSender:
    def __init__(self, port, baudrate=115200):
        """
        GRBL-Servoとの通信を初期化
        
        Args:
            port (str): シリアルポート名 (例: 'COM3' または '/dev/ttyUSB0')
            baudrate (int): ボーレート（デフォルト: 115200）
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        
    def connect(self):
        """Arduinoとの接続を確立"""
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"ポート {self.port} に接続しました")
            time.sleep(2)  # Arduinoの起動を待つ
            
            # 接続確認
            self.wake_up()
            return True
            
        except serial.SerialException as e:
            print(f"接続エラー: {e}")
            return False
    
    def wake_up(self):
        """GRBLを起動状態にする"""
        self.serial_conn.write(b"\r\n\r\n")
        time.sleep(2)
        self.serial_conn.flushInput()
        print("GRBL起動完了")
    
    def send_command(self, command):
        """
        単一のGコマンドを送信
        
        Args:
            command (str): 送信するGコード
            
        Returns:
            str: GRBLからの応答
        """
        if not self.serial_conn:
            print("接続されていません")
            return None
            
        # コマンドの末尾に改行を追加
        if not command.endswith('\n'):
            command += '\n'
            
        print(f"送信: {command.strip()}")
        self.serial_conn.write(command.encode('utf-8'))
        
        # 応答を待つ
        response = ""
        while True:
            line = self.serial_conn.readline().decode('utf-8').strip()
            if line:
                response += line + "\n"
                print(f"応答: {line}")
                
                # 'ok'または'error'で応答完了
                if line.startswith('ok') or line.startswith('error'):
                    break
                    
        return response
    
    def send_gcode_file(self, filename):
        """
        Gコードファイルを送信
        
        Args:
            filename (str): 送信するGコードファイルのパス
        """
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                
            print(f"ファイル {filename} を送信開始（{len(lines)}行）")
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # 空行やコメントをスキップ
                if not line or line.startswith(';') or line.startswith('('):
                    continue
                
                print(f"[{i+1}/{len(lines)}] 送信中...")
                response = self.send_command(line)
                
                # エラーチェック
                if response and 'error' in response.lower():
                    print(f"エラーが発生しました: {response}")
                    user_input = input("続行しますか？ (y/n): ")
                    if user_input.lower() != 'y':
                        break
                
                time.sleep(0.1)  # 次のコマンドまで少し待つ
                
            print("ファイル送信完了")
            
        except FileNotFoundError:
            print(f"ファイル {filename} が見つかりません")
        except Exception as e:
            print(f"ファイル送信エラー: {e}")
    
    def get_status(self):
        """現在のステータスを取得"""
        return self.send_command("?")
    
    def home(self):
        """ホーミング実行"""
        print("ホーミング実行中...")
        return self.send_command("$H")
    
    def reset(self):
        """ソフトリセット実行"""
        print("リセット実行中...")
        self.serial_conn.write(b"\x18")  # Ctrl+X
        time.sleep(2)
    
    def unlock(self):
        """アラーム状態の解除"""
        return self.send_command("$X")
    
    def disconnect(self):
        """接続を切断"""
        if self.serial_conn:
            self.serial_conn.close()
            print("接続を終了しました")
    
    def mark_position(self, row, column):
        """
        マークシートの指定位置にマークを塗る
        
        Args:
            row (int): 行番号（0から開始）
            column (int): 列番号（0から開始）
        """
        # 行番号に基づくX方向のオフセット計算、列番号に基づくY方向のオフセット計算
        x_offset = row * 0.26
        y_offset = column * 0.5
        
        # 基本座標にオフセットを追加
        self.send_command("M3 S255")
        self.send_command(f"X{0.12 + x_offset} Y{0.07 + y_offset}")
        self.send_command("M3 S0")
        self.send_command(f"Y{0.33 + y_offset}")
        self.send_command("M3 S255")
        self.send_command(f"X{0.15 + x_offset} Y{0.37 + y_offset}")
        self.send_command("M3 S0")
        self.send_command(f"Y{0.03 + y_offset}")
        self.send_command("M3 S255")
        self.send_command(f"X{0.2 + x_offset} Y{0.01 + y_offset}")
        self.send_command("M3 S0")
        self.send_command(f"Y{0.39 + y_offset}")
        self.send_command("M3 S255")
        self.send_command(f"X{0.25 + x_offset} Y{0.37 + y_offset}")
        self.send_command("M3 S0")
        self.send_command(f"Y{0.03 + y_offset}")
        self.send_command("M3 S255")
        self.send_command(f"X{0.28 + x_offset} Y{0.07 + y_offset}")
        self.send_command("M3 S0")
        self.send_command(f"Y{0.33 + y_offset}")
        self.send_command("M3 S255")
        self.send_command("X0 Y0")

# 使用例
if __name__ == "__main__":
    # ポート名を環境に合わせて変更してください
    # Windows: 'COM3', 'COM4' など
    # Linux/Mac: '/dev/ttyUSB0', '/dev/ttyACM0' など
    PORT = '/dev/cu.usbmodem2201'  # ここを適切なポートに変更
    
    sender = GRBLServoSender(PORT)
    
    if sender.connect():
        try:
            # ホーミング実行
            sender.home()
            # 現在位置をワーキング座標系の原点に設定
            sender.send_command("G92X0Y0")
            
            # マークシートの指定行目指定列目にマークする
            sender.mark_position(4, 4)
                        
            # ステータス確認
            sender.get_status()
            
        except KeyboardInterrupt:
            print("\n中断されました")
            sender.reset()
        finally:
            sender.disconnect()
    else:
        print("接続に失敗しました")