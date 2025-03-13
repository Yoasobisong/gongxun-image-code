import cv2
import numpy as np
from cam_open import CamOpen
from send_web import VideoStream
import threading

class LineDetector:
    def __init__(self):
        self.angle = None
        self.distance = None

    def detect(self, image):
        height = image.shape[0]
        cropped_frame = image[:height-95, :]
        border_size = 20
        cropped_frame_o = cv2.copyMakeBorder(cropped_frame, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        hsv = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
        
        # 应用阈值
        h_binary = cv2.inRange(hsv[:,:,0], 72, 255)
        s_binary = cv2.inRange(hsv[:,:,1], 0, 255)
        v_binary = cv2.inRange(hsv[:,:,2], 38, 255)

        # 合并阈值结果
        binary = cv2.bitwise_and(h_binary, s_binary)
        binary = cv2.bitwise_and(binary, v_binary)
        binary = cv2.bitwise_not(binary)
        binary = cv2.copyMakeBorder(binary, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        blurred = cv2.GaussianBlur(binary, (3, 3), 0)
        width = blurred.shape[1]
        blurred[:, :width // 3] = 0
        contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) <= 0:
            self.distance = None
            self.angle = None
            return cropped_frame_o
        
        largest_contour = max(contours, key=cv2.contourArea)
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)
        
        if len(approx) == 4:
            # cv2.drawContours(cropped_frame_o, [approx], -1, (0, 255, 0), 2)
            
            # 找到最下面的两个点
            bottom_points = sorted(approx, key=lambda p: p[0][1], reverse=True)[:2]
            p1, p2 = bottom_points[0][0], bottom_points[1][0]

            # 确保p1在左边，p2在右边
            if p1[0] > p2[0]:
                p1, p2 = p2, p1
            cv2.line(cropped_frame_o, tuple(p1), tuple(p2), (0, 0, 255), 2)
            
            line_center_y = (p1[1] + p2[1]) / 2
            self.distance = line_center_y
            self.angle = np.degrees(np.arctan2(p2[1] - p1[1], p2[0] - p1[0]))
            
            text = f"Distance: {self.distance:.2f}, Angle: {self.angle:.2f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottom_left_corner_of_text = (10, cropped_frame.shape[0] - 10)
            font_scale = 0.5
            font_color = (0, 0, 0)
            line_type = 2

            cv2.putText(cropped_frame_o, text, 
                            bottom_left_corner_of_text, 
                            font, 
                            font_scale,
                            font_color,
                            line_type)
        else:
            self.distance = None
            self.angle = None   
        return cropped_frame_o
        
        

if __name__ == "__main__":
    cam = CamOpen(0, in_use=True)
    cam.open()
    cam.start()
    video_stream = VideoStream(5000)
    flask_thread = threading.Thread(target=video_stream.run)
    flask_thread.start()
    line_detector = LineDetector()
    while cam.thread_running:
        img = cam.read()
        if img is not None and img.size >= 10:
            img = line_detector.detect(img)
            video_stream.update_frame(img)
            # print(line_detector.distance, line_detector.angle)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.stop()  
            cam.release()
            break
