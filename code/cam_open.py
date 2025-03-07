RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

import cv2
import threading
import time
import numpy as np

def grab_img(cam):
    while cam.thread_running:
        fps = 30
        ret, img = cam.cap.read()
        if ret:
            cam.frame = img
            time.sleep(1/fps)
            key = cv2.waitKey(1)
            if key == ord('q'):
                cam.thread_running = False
                cam.stop()  
                cam.release()
                break
            if not cam.in_use:
                time.sleep(1.0)
        else:
            print(f"{RED}Error: Could not grab frame {cam.cap_index}.{RESET}")
            cam.thread_running = False
            cam.stop()
            cam.release()
            break
    print(f"{YELLOW}Cam{cam.cap_index} thread end{RESET}")

class CamOpen:  
    def __init__(self, cap_index, in_use = False):
        self.is_open = False
        self.thread_running = None
        self.thread = None
        self.frame = None
        self.cap = None
        self.cap_index = cap_index
        self.in_use = in_use
        
    def __del__(self):
        if self.cap is not None:
            self.cap.release()
            print(f"{YELLOW}release{RESET}")
            self.thread_running = None
        
    def open(self):
        try:
            self.cap = cv2.VideoCapture(self.cap_index)
            self.is_open = True
            print(f"{GREEN}open camera {self.cap_index}{RESET}")
        except:
            print(f"{RED}Error: Could not open video{self.cap_index}{RESET}")
            self.is_open = False
    
    def start(self):
        assert not self.thread_running
        self.thread_running = True
        self.thread = threading.Thread(target=grab_img, args=(self,))
        self.thread.start()

    def stop(self):
        self.thread_running = False
        try:
            self.thread.join()
        except:
            pass
    
    def read(self):
        return np.copy(self.frame)
    
    def release(self):
        assert not self.thread_running
        if self.cap is not None:
            self.cap.release()
            self.thread_running = None
    
    
if __name__ == "__main__":
    from send_web import VideoStream
    video_stream = VideoStream(5000)
    cam = CamOpen(1)
    cam.open()
    cam.start()
    frame_count = 0

    flask_thread = threading.Thread(target=video_stream.run)
    flask_thread.start()
    
    while cam.thread_running:
        img = cam.read()
        print(img.shape)
        frame_count += 1    
        # print(f"Frame count: {frame_count}")
        video_stream.update_frame(img)
        time.sleep(1/25)
        #  cv2.imshow("img", img)
