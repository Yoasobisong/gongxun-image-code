RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'
import serial
import time
import numpy
import threading
class Serial:
    def __init__(self, port='/dev/hx430', baudrate=9600):
        try:
            self.ser = serial.Serial(port, baudrate)
            self.thread_running = True
            print(f"{GREEN}Serial port {port} opened successfully{RESET}")
        except Exception as e:
            print(f"{YELLOW}Error opening serial port: {e}{RESET}")
            self.ser = None
            self.thread_running = False

    def send_byte(self, byte_data):
        if isinstance(byte_data, int):
            self.ser.write(bytearray([byte_data]))

    def read_byte(self):
        try:
            return self.ser.read(1)[0]
        except Exception as e:
            return None
    
    def get_data(self, gongxun):
        while self.thread_running:
            if gongxun.task != 0:
                data = self.read_byte()
                print(f"{YELLOW}Receive data: {data}{RESET}")
                if data == 0x02 and gongxun.task != 2:
                    gongxun.task = 2
                    print(f"{BLUE}change task to 2{RESET}")
                elif data == 0x03 and gongxun.task != 3:
                    gongxun.task = 3
                    print(f"{BLUE}change task to 3{RESET}")
                elif data == 0x04 and gongxun.task != 4:
                    gongxun.task = 4
                    print(f"{BLUE}change task to 4{RESET}")
            time.sleep(0.1)
        print(f"{YELLOW}Serial thread end{RESET}")
            
            
    def send_qr_data(self, data):
        if isinstance(data, str):
            self.ser.write(bytearray([0x0d]))  # Frame header
            for char in data:
                if char.isdigit():
                    self.send_byte(ord(char) - 48)
            self.ser.write(bytearray([0xff]))  # Frame tail
            
    def send_ann_data(self, data):
        data = [int(i) for i in data]
        if len(data) == 3:
            self.ser.write(bytearray([0x0c]))  # Frame header
            for i, value in enumerate(data):
                if i == 0:
                    self.send_byte(1 if value > 0 else 0)
                    self.send_byte(abs(value) // 256 if abs(value) > 255 else 0)
                    self.send_byte(abs(value) % 256)
                elif i == 1:
                    self.send_byte(1 if value > 0 else 0)
                    self.send_byte(abs(value))
                elif i == 2:
                    self.send_byte(abs(value))
            self.ser.write(bytearray([0xff]))  
            
    def send_mat_data(self, data):
        data = [int(i) for i in data]
        if len(data) == 3:
            self.ser.write(bytearray([0x0b]))  # Frame header
            for i, value in enumerate(data):
                if i == 0:
                    self.send_byte(1 if value > 0 else 0)
                    self.send_byte(abs(value) // 256 if abs(value) > 255 else 0)
                    self.send_byte(abs(value) % 256)
                elif i == 1:
                    self.send_byte(1 if value > 0 else 0)
                    self.send_byte(abs(value))
                elif i == 2:
                    self.send_byte(abs(value))
            self.ser.write(bytearray([0xff]))  # Frame tail
    
    def send_line_data(self, data):
        if len(data) == 2:
            self.ser.write(bytearray([0x0e]))  # Frame header
            self.ser.write(bytearray([int(data[0]) // 256]))
            self.ser.write(bytearray([int(data[0]) % 256]))
            self.ser.write(bytearray([1]) if data[1] > 0 else bytearray([0]))
            # print(f"data[1]: {abs(int(data[1]))}")
            self.ser.write(bytearray([abs(int(data[1]))]))
            self.ser.write(bytearray([abs(int(data[1]) * 100 % 100)]))
            self.ser.write(bytearray([0xff])) 
            
            
if __name__ == "__main__":
    try:
        serial = Serial()
        # serial_thread = threading.Thread(target=serial.get_data).start()
        while True:
            serial.send_mat_data([-100, 100, 1])
            time.sleep(0.3)
    except Exception as e:
        print(f"An error occurred: {e}")
