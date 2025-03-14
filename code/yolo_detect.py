import time
t1 = time.time()
import os
# os.environ['YOLO_VERBOSE'] = str(False)
from ultralytics import YOLO
from cam_open import CamOpen
import cv2
import threading
from send_web import VideoStream
import torch
import numpy as np
import argparse
import math
# from serial_send import SerialSend

class Yolo_detect():
    def __init__(self, model_path, conf=0.80, line_width=1):
        self.model = YOLO(model_path)
        self.x_y = np.array([])
        self.image = None
        self.conf = conf
        self.line_width = line_width
        self.center_xy = None
        self.classes = None
        self.angle = -255
        
    def detect(self, img):
        self.image = img
        # print("self.image.shape[1]:", self.image.shape[1])
        results = self.model(source=img, conf=self.conf, line_width=self.line_width)
        self.x_y = results[0].boxes.xywh.cpu().numpy()
        self.classes = results[0].boxes.cls.cpu().numpy()
        self.deal_x_y()
        self.image = results[0].plot()
        for i in range(len(self.x_y)):
            cv2.circle(self.image, (int(self.x_y[i][0]), int(self.x_y[i][1])), 5, (0, 0, 255), -1)
        if(len(self.x_y) == 0):
            self.center_xy = None
            self.angle = -255
        else:
            if len(self.x_y) >= 2:
                self.angle = self.get_angle()
                pass
            else:
                self.angle = -255
            self.get_center()
        return self.image
        
    def deal_x_y(self):
        # for i, xy in enumerate(self.x_y):
        #     if  xy[2] / xy[3] > 1.2:
        #         xy[1] = 1 if xy[1] < self.image.shape[0] / 2 else 479
        #     elif xy[2] / xy[3] < 0.8:
        #         xy[0] = 1 if xy[0] < self.image.shape[1] / 2 else 639
        for i, xy in enumerate(self.x_y):
            w, h = xy[2:]
            if w/h >= 1.1:
                err = (xy[2] - xy[3]) / 2
                xy[1] = (xy[1] - err) if xy[1] < 240 else (xy[1] + err)
            elif w/h <=0.9:
                err = (xy[3] - xy[2]) / 2
                xy[0] = (xy[0] - err) if xy[0] < 320 else (xy[0] + err)
        
    def get_center(self):
        """
        get the error of the object
        """
        img_center_x = self.image.shape[1] / 2
        img_center_y = self.image.shape[0] / 2
        min_distance = float('inf')
        closest_point = None
        for i, point in enumerate(self.x_y):
            x, y = point[:2]
            distance = ((x - img_center_x) ** 2 + (y - img_center_y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_point = np.array([x, y, self.classes[i]])
        self.center_xy = closest_point



    def calculate_angle(self, x1, y1, x2, y2):
        angle_rad = math.atan2(abs(y2 - y1), abs(x2 - x1))  # 计算弧度
        angle_deg = math.degrees(angle_rad)  # 转换为角度
        return ((y2 - y1)/(x2 - x1))/(abs((y2 - y1)/(x2 - x1)))*angle_deg

    def _cal_center(self, point):
        w, h = point[2:]
        if w/h >= 1.1:
            err = (point[2]-point[3])/2
            point = [point[0], (point[1] - err) if point[1]<240 else (point[1] + err)]
        else:
            err = (point[3]-point[2])/2
            point = [(point[0] - err) if point[0]<320 else (point[0] + err), point[1]]
        return point    
            
    def get_right_points(self):
        points_a = []
        points_b = []
        for i, point in enumerate(self.x_y):
            w, h = point[2:]
            if 0.9 < w/h < 1.1:
                points_a.append(point[:2])
                
            else:
                points_b.append(point[:2])
        return (points_a + points_b)[:2]
        
            
            
    
    def get_angle(self):
        """_summary_
        get the angle of two points
        """
        points = self.get_right_points()
        angle = self.calculate_angle(points[0][0], points[0][1], points[1][0], points[1][1])
        cv2.line(self.image, (int(points[0][0]), int(points[0][1])), (int(points[1][0]), int(points[1][1])), (0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
        # print(f"angle: {angle}")
        return angle  

#
    
if __name__ == "__main__":
    cam = CamOpen(0)
    cam.open()
    cam.start()
    parser = argparse.ArgumentParser(description="openvino detect")
    parser.add_argument('--show', type=bool, default=True, help='是否进行显示img')
    args = parser.parse_args()
    if args.show:
        video_stream = VideoStream(5001)
        flask_thread = threading.Thread(target=video_stream.run)
        flask_thread.start()
    yolo_detect = Yolo_detect("../mat_pt/mat.pt")
    while cam.thread_running:
        results = yolo_detect.detect(cam.read())
        try:
            print(results[0].boxes.xywh.cpu().numpy())
        except:
            pass
        t2 = time.time()
        print("center_xy:", yolo_detect.center_xy)
        print("time:", t2 - t1)
        t1 = t2
        if args.show:
            video_stream.update_frame(yolo_detect.image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.stop()
            cam.release()
            break
