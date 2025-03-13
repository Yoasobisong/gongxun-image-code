from yolo_detect import Yolo_detect
from openvino_detect import detect_Openvino
from cam_open import CamOpen
import threading
import cv2

class Test:
    def __init__(self, yolo):
        self.yolo = yolo
        self.yolo_vino = False

    def if_yolo_run(self):
        try:
            self.yolo.detect('../images/14.jpg')
            self.yolo.detect('../images/14.jpg')
            print("change to yolov8")
            self.yolo_vino = True
        except Exception as e:
            print(f"Yolo detection failed: {e}")
        return True

if __name__ == "__main__":
    cam = CamOpen(1)
    cam.open()
    cam.start()
    yolo = Yolo_detect("../ann.pt")
    openvino = detect_Openvino("../mat_vino/mat.xml")
    
    test = Test(yolo)
    yolo_thread = threading.Thread(target=test.if_yolo_run)
    yolo_thread.start()
    while cam.thread_runing:
        if not test.yolo_vino:
            img = cam.read()
            frame = img.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = openvino.detect(frame)
            print(openvino.center_xy)
        else:
            img = yolo.detect(cam.read())
            print(yolo.center_xy)
