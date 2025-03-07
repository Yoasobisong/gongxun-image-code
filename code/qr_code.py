import cv2
import numpy as np
from pyzbar.pyzbar import decode
from serial_deal import Serial

import time

class QrCode:
    def __init__(self):
        pass

    def get_qr_data(self, img: np.ndarray) -> str:
        decoded_objects = decode(img)
        if decoded_objects:
            return decoded_objects[0].data.decode('utf-8')
        return None
    
    
if __name__ == "__main__":
    qr_code = QrCode()
    cap = cv2.VideoCapture(0)
    serial = Serial()
    # Loop through the video frames
    while cap.isOpened():
        _, img = cap.read()
        print(qr_code.get_qr_data(img))
        serial.send_qr_data(qr_code.get_qr_data(img))
        
