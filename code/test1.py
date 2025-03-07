from yolo_detect import Yolo_detect
from cam_open import CamOpen
import cv2
import time

if __name__ == "__main__":
    cam = CamOpen(1)
    cam.open()
    cam.start()
    start_time = time.time()
    print(f"start time: {time.time() - start_time}")
    yolo1 = Yolo_detect("../mat_pt/mat.pt")
    yolo2 = Yolo_detect("../ann.pt")
    print(f"yolo init time: {time.time() - start_time}")
    # yolo2.detect("../images/14.jpg")
    for i in range(10):
        yolo1.detect("../images/14.jpg")
    print(f"yolo1 time: {time.time() - start_time}")
    
    time.sleep(10)
    print(f"10s time: {time.time() - start_time}")
    for i in range(10):
        yolo2.detect("../images/14.jpg")
    print(f"yolo2 time: {time.time() - start_time}")
    