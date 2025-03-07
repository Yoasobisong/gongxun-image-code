import time
import torch
import openvino as ov
import ipywidgets as widgets
import cv2
from ultralytics.utils.plotting import colors
from typing import Tuple
from ultralytics.utils import ops
import numpy as np
from pathlib import Path
from PIL import Image
# from ultralytics import YOLO
from typing import Tuple, Dict
import threading
from cam_open import CamOpen
import argparse
import random


RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'

class Openvino:
    def __init__(self, model_path):
        self.core = ov.Core()
        self.available_devices = self.core.available_devices
        print(f"{BLUE}Available devices:{RESET}", self.available_devices)

        # self.det_ov_model = self.core.read_model('../mat_vino_int8/best.xml')
        self.det_ov_model = self.core.read_model(model_path)
        self.device = widgets.Dropdown(
            options=self.core.available_devices + ["AUTO"],
            value='AUTO',
            description='Device:',
            disabled=False,
        )

        # self.det_model = YOLO('../mat_pt/mat.pt')
        # self.label_map = self.det_model.model.names
        # print(self.label_map)
        self.label_map = {0: 'red', 1: 'green', 2: 'blue'}
        if self.device.value != "CPU":
            self.det_ov_model.reshape({0: [1, 3, 320, 320]})
        self.det_compiled_model = self.core.compile_model(self.det_ov_model, self.device.value)
        print(f"{BLUE}{self.device}{RESET}")
        self.center_xy = None


    def letterbox(self, img: np.ndarray, new_shape: Tuple[int, int] = (320, 320), color: Tuple[int, int, int] = (114, 114, 114), auto: bool = False, scale_fill: bool = False, scaleup: bool = False, stride: int = 32):
        shape = img.shape[:2]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not scaleup:
            r = min(r, 1.0)
        ratio = r, r
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        if auto:
            dw, dh = np.mod(dw, stride), np.mod(dh, stride)
        elif scale_fill:
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]
        dw /= 2
        dh /= 2
        if shape[::-1] != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        return img, ratio, (dw, dh)

    def preprocess_image(self, img0: np.ndarray):
        img = self.letterbox(img0)[0]
        img = img.transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        return img

    def image_to_tensor(self, image: np.ndarray):
        input_tensor = image.astype(np.float32)
        input_tensor /= 255.0
        if input_tensor.ndim == 3:
            input_tensor = np.expand_dims(input_tensor, 0)
        return input_tensor

    def postprocess(self,
                    pred_boxes: np.ndarray,
                    input_hw: Tuple[int, int],
                    orig_img: np.ndarray,
                    min_conf_threshold: float = 0.7,
                    nms_iou_threshold: float = 0.7,
                    agnosting_nms: bool = False,
                    max_detections: int = 3):
        nms_kwargs = {"agnostic": agnosting_nms, "max_det": max_detections}
        preds = ops.non_max_suppression(
            torch.from_numpy(pred_boxes),
            min_conf_threshold,
            nms_iou_threshold,
            nc=3,
            **nms_kwargs
        )
        results = []
        for i, pred in enumerate(preds):
            shape = orig_img[i].shape if isinstance(orig_img, list) else orig_img.shape
            if not len(pred):
                results.append({"det": [], "segment": []})
                continue
            pred[:, :4] = ops.scale_boxes(input_hw, pred[:, :4], shape).round()
            results.append({"det": pred})
        return results

    # def get_center(self, results: Dict):

    def plot_all_box(self, boxes, source_image, label_map, points, line_thickness=1):
        for idx, (*xyxy, conf, lbl) in enumerate(boxes):
            label = f'{label_map[int(lbl)]} {conf:.2f}'
            tl = line_thickness or round(0.002 * (source_image.shape[0] + source_image.shape[1]) / 2) + 1
            color = [random.randint(0, 255) for _ in range(3)]
            c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
            cv2.rectangle(source_image, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
            if label:
                tf = max(tl - 1, 1)
                t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
                c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
                cv2.rectangle(source_image, c1, c2, color, -1, cv2.LINE_AA)
                cv2.putText(source_image, label, (c1[0], c1[1] - 2), 0, tl / 3, [0, 0, 0], thickness=tf, lineType=cv2.LINE_AA)
            cv2.circle(source_image, (points[idx][0], points[idx][1]), 5, color, -1)
        return source_image
    
    
    def get_center(self, points):
        img_center_x = 320
        img_center_y = 240
        min_distance = float('inf')
        closest_point = None
        for point in points:
            distance = ((point[0] - img_center_x) ** 2 + (point[1] - img_center_y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_point = np.array([point[0], point[1], point[3]])
        self.center_xy = closest_point

    def draw_results(self, results: Dict, source_image: np.ndarray, label_map: Dict):
            """
            中心点坐标的对应设置
            判断边框比例
            """
            boxes = results["det"]
            points = []
            for idx, (*xyxy, conf, lbl) in enumerate(boxes):
                center_x = int((xyxy[0] + xyxy[2]) / 2)
                center_y = int((xyxy[1] + xyxy[3]) / 2)
                width = xyxy[2] - xyxy[0]
                height = xyxy[3] - xyxy[1]
                points.append([center_x, center_y, width/height, lbl])
            
            for point in points:
                if point[2] > 1.2:
                    point[1] = 1 if point[1] < source_image.shape[0] / 2 else 479
                elif point[2] < 0.8:
                    point[0] = 1 if point[0] < source_image.shape[1] / 2 else 639
            
            if(len(points) > 0):
                self.get_center(points)
            else:
                self.center_xy = None
            if len(boxes) > 0:
                source_image = self.plot_all_box(boxes, source_image, label_map, points)
            
            return source_image

class detect_Openvino(Openvino):
    def __init__(self, model_path):
        super().__init__(model_path)
        self.frame = None
        
    def detect(self, image: np.ndarray):
        preprocessed_image = self.preprocess_image(image)
        input_tensor = self.image_to_tensor(preprocessed_image)
        start_time = time.time()
        result = self.det_compiled_model(input_tensor)
        end_time = time.time()
        # print(f"Inference time: {end_time - start_time:.2f} seconds")
        boxes = result[self.det_compiled_model.output(0)]
        input_hw = input_tensor.shape[2:]
        detections = self.postprocess(pred_boxes=boxes, input_hw=input_hw, orig_img=image)
        # print(f"Detections: {detections}")
        return self.draw_results(detections[0], image, self.label_map)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="openvino detect")
    parser.add_argument('--show', type=bool, default=True, help='是否进行显示img')
    args = parser.parse_args()
    
    cam = CamOpen("/dev/v4l/by-id/usb-Sonix_Technology_Co.__Ltd._USB_Camera-video-index0")
    cam.open()
    cam.start()
    if args.show:
        from send_web import VideoStream
        video_stream = VideoStream(port=5000)
        flask_thread = threading.Thread(target=video_stream.run)
        flask_thread.start()
    openvino = detect_Openvino("../mat_vino/mat.xml")
    
    while cam.thread_running:
        img = cam.read()
        frame = img.copy()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = openvino.detect(frame)
        print(openvino.center_xy)
        if args.show:
            video_stream.update_frame(img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.stop()
            cam.release()
            break