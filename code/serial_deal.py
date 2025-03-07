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
    def __init__(self, port='/dev/hx430', baudrate=9600, qr_send_times=50):
        try:
            self.ser = serial.Serial(port, baudrate)
            self.thread_running = True
            print(f"{GREEN}Serial port {port} opened successfully{RESET}")
            self.qr_send_times = qr_send_times
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
            data = self.read_byte()
            if data != None:
                print(f"{YELLOW}Receive data: {data}{RESET}")
            if gongxun.task != 0:
                
                if data == 0x02 and gongxun.task != 2:
                    gongxun.task = 2
                    print(f"{BLUE}change task to 2{RESET}")
                elif data == 0x03 and gongxun.task != 3:
                    gongxun.task = 3
                    print(f"{BLUE}change task to 3{RESET}")
                elif data == 0x04 and gongxun.task != 4:
                    # time.sleep(0.3)
                    gongxun.task = 4
                    print(f"{BLUE}change task to 4{RESET}")
                elif data == 0x01 and gongxun.task != 0:
                    gongxun.task = 0
                    gongxun.qr_data = None
                    gongxun.cam1.in_use = True
                    gongxun.cam0.in_use = False
                    print(f"{BLUE}change task to 0 and open cam0 close cam1{RESET}")
                elif data == 0x05:
                    gongxun.disk5.clear()
                    gongxun.task = 5
                    print(f"{BLUE}change task to 5{RESET}")
                    gongxun.last_error_xy = None
                elif data == 0x06:
                    gongxun.disk6.clear()
                    gongxun.task = 6
                    gongxun.last_error_xy = None
                    print(f"{BLUE}change task to 6{RESET}")
                elif data == 0x07 and gongxun.task == 5 and gongxun.disk5.session != 2:
                    # gongxun.disk5.first_color[1] = True
                    gongxun.disk5.session = 2
                    print(f"{BLUE}Disk5 adjust okay!{RESET}")
                elif data == 0x08 and gongxun.task == 6 and gongxun.disk6.session != 2:
                    # gongxun.disk6.first_color[1] = True
                    gongxun.disk6.session = 2
                    print(f"{BLUE}Disk6 adjust okay!{RESET}")

            else: # from task 0 change to others
                if data == 0x02:
                    gongxun.task = 2
                    gongxun.cam1.in_use = False
                    gongxun.cam0.in_use = True
                    print(f"{BLUE}change task to 2{RESET}")
                elif data == 0x03:
                    gongxun.task = 3
                    gongxun.cam1.in_use = False
                    gongxun.cam0.in_use = True
                    print(f"{BLUE}change task to 3{RESET}")
                elif data == 0x04:
                    # time.sleep(0.3)
                    gongxun.task = 4
                    gongxun.cam1.in_use = False
                    gongxun.cam0.in_use = True
                    print(f"{BLUE}change task to 4{RESET}")
                elif data == 0x05:
                    gongxun.disk5.clear()
                    gongxun.task = 5
                    gongxun.cam1.in_use = False
                    gongxun.cam0.in_use = True
                    print(f"{BLUE}change task to 5{RESET}")
                elif data == 0x06:
                    gongxun.disk6.clear()
                    gongxun.task = 6
                    gongxun.cam1.in_use = False
                    gongxun.cam0.in_use = True
                    print(f"{BLUE}change task to 6{RESET}")
                
            time.sleep(0.1)
        print(f"{YELLOW}Serial thread end{RESET}")
            
            
    def send_qr_data(self, data):
        # print(f"sending qr_data: {data}")
        if isinstance(data, str):
            self.ser.write(bytearray([0x0d]))  # Frame header
            for char in data:
                if char.isdigit():
                    self.send_byte(ord(char) - 48)
            self.ser.write(bytearray([0xff]))  # Frame tail
            self.ser.write(bytearray([0xef]))

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
            self.ser.write(bytearray([0xef]))

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
            self.ser.write(bytearray([0xef]))
    
    def send_line_data(self, data):
        # print(data)
        if len(data) == 2:
            self.ser.write(bytearray([0x0e]))  # Frame header
            self.ser.write(bytearray([int(data[0]) // 256]))
            self.ser.write(bytearray([int(data[0]) % 256]))
            self.ser.write(bytearray([1]) if data[1] > 0 else bytearray([0]))
            # print(f"data[1]: {abs(int(data[1]))}")
            self.ser.write(bytearray([abs(int(data[1]))]))
            self.ser.write(bytearray([abs(int(data[1] * 100) % 100)]))
            self.ser.write(bytearray([0xff])) 
            self.ser.write(bytearray([0xef]))
            
    def grab_mat(self):
        self.ser.write(bytearray([0x0f])) # Frame header
        self.ser.write(bytearray([0x11]))
        self.ser.write(bytearray([0x22]))
        self.ser.write(bytearray([0x33]))
        self.ser.write(bytearray([0xff]))
        self.ser.write(bytearray([0xef]))
        
    def go_away(self):
        self.ser.write(bytearray([0x1f])) # Frame header
        self.ser.write(bytearray([0x11]))
        self.ser.write(bytearray([0x22]))
        self.ser.write(bytearray([0x33]))
        self.ser.write(bytearray([0x44]))
        self.ser.write(bytearray([0xff]))
        self.ser.write(bytearray([0xef]))
        
if __name__ == "__main__":
    try:
        serial = Serial()
        # serial_thread = threading.Thread(target=serial.get_data).start()
        while True:
            serial.send_mat_data([-100, 100, 1])
            time.sleep(0.3)
    except Exception as e:
        print(f"An error occurred: {e}")
