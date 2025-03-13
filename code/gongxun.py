RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

from cam_open import CamOpen
from line_detect import LineDetector
from openvino_detect import detect_Openvino
from qr_code import QrCode
from send_web import VideoStream
from serial_deal import Serial
from yolo_detect import Yolo_detect
import argparse
import threading
import time
import cv2
import signal
import sys

class Gongxun:
    def __init__(self, args, ann_model_path = "../ann_pt/ann4.pt", 
                 mat_model_path = "../mat_pt/mat.pt", 
                 openvino_mat_path = "../mat_vino/mat.xml",
                 port = 5000, 
                 serial_port = "/dev/hx430",
                 serial_baudrate = 9600,
                 cam0_pth = "/dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB_Camera-video-index0", # later
                 cam1_pth = "/dev/v4l/by-id/usb-HD_720P_Webcam_HD_720P_Webcam_20170301-video-index0", # qr
                 qr_send_times = 50,
                 mat_conf=0.8,
                 ann_conf=0.8
                 ):
        # basic prepare
        self.args = args
        self.task = self.args.task
        self.running = True
        # cam prepare
        if self.task == 0:
            self.cam0 = CamOpen(cam0_pth, in_use = False)
        else:
            self.cam0 = CamOpen(cam0_pth, in_use = True) 
        self.cam0.open()
        self.cam0.start()
        if self.task == 0:
            self.cam1 = CamOpen(cam1_pth, in_use = True)
            print(f"{YELLOW} task != 0, dont use cam1!{RESET}")
        else:
            self.cam1 = CamOpen(cam1_pth, in_use = False)
        self.cam1.open()
        self.cam1.start()
            
        # qr code prepare
        self.qr_code = QrCode()
        self.qr_send_times = qr_send_times
        self.sending_qr = False
        self.qr_send_interval = 0.01
        # line detect prepare
        self.line_detect = LineDetector()
        # yolo and openvino prepare
        self.yolo_detect_mat = Yolo_detect(mat_model_path, conf=mat_conf)
        self.yolo_detect_ann = Yolo_detect(ann_model_path, conf=ann_conf)
        self.openvino_detect = detect_Openvino(openvino_mat_path)
        self.init_yolo_thread = threading.Thread(target=self.init_yolo)
        self.init_yolo_thread.start()
        # serial prepare
        self.serial = Serial(serial_port, serial_baudrate)
        self.serial_thread = threading.Thread(target=self.serial.get_data, args=(self, ))
        self.serial_thread.start()
        self.serial_send_interval = 0.02
        # data prepare
        self.close_openvino = False 
        self.error_xy = None
        # self.center_xy = None
        # thread prepare
        self.serial_send_thread = threading.Thread(target=self.ready_send_data)
        self.serial_send_thread.start()
        # video stream prepare
        if args.web:
            self.video_stream = VideoStream(args.port)
            self.thread_video_stream = threading.Thread(target=self.video_stream.run).start()
        # thread prepare
        self.width = 640
        self.height = 480
        # data prepare
        self.qr_data = None
        
        # Register signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def __iter__(self):
        return iter(self.task)
        
    def __del__(self):
        self.cleanup()

    def signal_handler(self, sig, frame):
        print(f'{YELLOW}You pressed Ctrl+C!{RESET}')
        self.cleanup()
        sys.exit(0)

    def cleanup(self):
        self.running = False
        if self.args.web:
            self.video_stream.running = False 
        self.serial.thread_running = False
        if self.cam0.thread_running:
            self.cam0.thread_running = False
            self.cam0.stop()
            self.cam0.release()
        try:
            if self.cam1.thread_running:
                self.cam1.thread_running = False
                self.cam1.stop()
                self.cam1.release()
        except:
            print(f"{RED}cam1 not open at all!{RESET}")
        if self.serial.ser:
            self.serial.ser.close()
        print(f"{GREEN}cleanup success{RESET}")

    def init_yolo(self):
        try:
            print(f"{GREEN}Starting init yolo mat{RESET}")
            self.yolo_detect_mat.detect("../images/14.jpg")
            self.close_openvino = True
            print(f"{GREEN}init yolo mat success{RESET}")
        except Exception as e:
            print(f"{RED}init yolo error: {e}{RESET}")
            
            
    def ready_send_data(self):
        while self.running:
            if self.sending_qr:
                for i in range(self.qr_send_times):
                    self.serial.send_qr_data(self.qr_data)
                    time.sleep(self.qr_send_interval)
                self.sending_qr = False
                self.cam0.in_use = True
                print(f"{GREEN}send qr data success{RESET}")

            if self.task == 1 or self.task == 2:
                if self.error_xy is not None:
                    self.serial.send_mat_data(self.error_xy)
            elif self.task == 3:
                if self.error_xy is not None:
                    self.serial.send_ann_data(self.error_xy)
            elif self.task == 4:
                if self.line_detect.distance is not None:
                    self.serial.send_line_data([self.line_detect.distance, self.line_detect.angle])
                    
            time.sleep(self.serial_send_interval)
        pass
        print(f"{YELLOW}Serial send thread end{RESET}")
    
    def get_error(self, center_xy):
        if center_xy is None:
            return None
        return [center_xy[0] - self.width / 2, center_xy[1] - self.height / 2, center_xy[2] + 1]
    
    def delay(self, seconds):
        time.sleep(seconds)

    def run(self):
        try:
            while self.running:
                if self.task == 0:
                    frame = self.cam1.read()
                else:
                    frame = self.cam0.read()
                if self.task == 0:
                    try:
                        self.qr_data = self.qr_code.get_qr_data(frame)
                    except Exception as e:
                        continue
                    if self.qr_data is not None:
                        self.sending_qr = True
                        self.task = 1
                        print(f"{GREEN}qr_data: {self.qr_data}{RESET}")
                        # print(f"{YELLOW}Ready to detect qr_code using openvino!{RESET}")
                        # self.cam1.stop()
                        # self.cam1.release()
                elif self.task == 1:
                    frame = self.openvino_detect.detect(frame)
                    
                    if self.close_openvino:
                        self.task = 2
                        print(f"{YELLOW}Ready to detetct using yolo!{RESET}")
                    # print("2")
                    pass
                elif self.task == 2:
                    frame = self.yolo_detect_mat.detect(frame)
                elif self.task == 3:
                    frame = self.yolo_detect_ann.detect(frame)
                elif self.task == 4:
                    frame = self.line_detect.detect(frame)
                    
                center_x = 320
                center_y = 240
                color = (255, 255, 255)
                thickness = 2
                cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), color, thickness)
                cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), color, thickness)
                cv2.putText(frame, f"task: {self.task}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if self.task == 1:
                    self.error_xy = self.get_error(self.openvino_detect.center_xy)
                elif self.task == 2:
                    self.error_xy = self.get_error(self.yolo_detect_mat.center_xy)
                elif self.task == 3:
                    self.error_xy = self.get_error(self.yolo_detect_ann.center_xy)
                    
                    
                # print(self.center_xy)
                if self.task != 0 and self.error_xy is not None:
                    cv2.putText(frame, f"{self.error_xy[0]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, f"{self.error_xy[1]}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame, f"{self.error_xy[2]}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    
                if self.args.web:
                    self.video_stream.update_frame(frame)
        except Exception as e:
            self.cleanup()
            print(f"{RED}run error: {e}{RESET}")
               
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="openvino detect")
    parser.add_argument('--web', type=bool, default=True, help='if display img on web')
    parser.add_argument('--task', type=int, default=0, help='task type')
    parser.add_argument('--port', type=int, default=5000, help='web send port')
    args = parser.parse_args()
    
    gongxun = Gongxun(args)
    gongxun.run()
