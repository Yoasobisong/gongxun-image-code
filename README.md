# Industrial Training Competition Computer Vision Code

## 2025工训赛物流搬运图像处理

This repository contains computer vision code implementations for industrial training competition robotics tasks, including object detection, QR code recognition, and line detection modules. The code is specifically optimized for deployment on Jetson Nano platform.

## Demo

Below is a demo video showing material detection in action:

![Demo Video](https://github.com/Yoasobisong/gongxun-image-code/raw/main/runs/mat_o.mp4)

## Key Features

- **Object Detection**: Material recognition and positioning using YOLO model
- **QR Code Recognition**: QR code detection and decoding functionality
- **Line Detection**: Detection of geometric features like straight lines and curves
- **Camera Operations**: Real-time video stream processing and image capture

## Project Structure

```
gongxun_demo/
├── code/              # Core implementation files
│   ├── yolo_detect.py    # Object detection implementation
│   ├── qr_code.py        # QR code recognition
│   ├── line_detect.py    # Line detection
│   ├── cam_open.py       # Camera operations
│   ├── gongxun.py        # Main competition logic
│   ├── openvino_detect.py# OpenVINO inference
│   ├── send_web.py       # Web communication
│   └── serial_deal.py    # Serial communication
├── ann_pt/            # Annotation neural network model
└── mat_pt/            # Material detection model
```

## Code Description

### Core Modules

#### 1. Object Detection (`yolo_detect.py`)

#### 2. QR Code Recognition (`qr_code.py`)

#### 3. Line Detection (`line_detect.py`)

#### 4. Camera Operations (`cam_open.py`)
### Supporting Modules

#### 5. Main Competition Logic (`gongxun.py`)

#### 6. OpenVINO Inference (`openvino_detect.py`)

#### 7. Web Communication (`send_web.py`)

#### 8. Serial Communication (`serial_deal.py`)

## Deployment Environment

### Hardware Requirements
- **Platform**: Jetson Nano
- **RAM**: 4GB
- **Storage**: 16GB+ recommended
- **Camera**: USB camera or CSI camera

### Software Requirements
- **OS**: Ubuntu 18.04
- **Python**: 3.6
- **CUDA**: 10.2
- **cuDNN**: 8.0
- **OpenVINO**: 2021.4.2

### Dependencies
- OpenCV-Python >= 4.5.0
- PyTorch >= 1.8.0 (with CUDA support)
- OpenVINO >= 2021.4.2
- pyzbar >= 0.1.8
- numpy >= 1.19.4
- pyserial >= 3.5


## Maintainer

- [@Yoasobisong](https://github.com/Yoasobisong)

## Contact

- Email: yqs0ong1@gamil.com
- GitHub: [@Yoasobisong](https://github.com/Yoasobisong)

## License

[MIT](LICENSE) © Yoasobisong 
