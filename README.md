# Industrial Training Competition Computer Vision Code

This repository contains computer vision code implementations for industrial training competition robotics tasks, including object detection, QR code recognition, and line detection modules. The code is specifically optimized for deployment on Jetson Nano platform.

## Demo

Below is a demo video showing material detection in action:

https://github.com/Yoasobisong/gongxun-image-code/raw/main/runs/mat_o.avi

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
│   └── cam_open.py       # Camera operations
├── ann_pt/            # Neural network model files
└── mat_vino/          # OpenVINO optimized models
```

## Deployment Environment

### Hardware Requirements
- **Platform**: Jetson Nano
- **RAM**: 4GB
- **Storage**: 16GB+ recommended

### Software Requirements
- **OS**: Ubuntu 18.04
- **Python**: 3.6
- **CUDA**: 10.2
- **cuDNN**: 8.0

### Dependencies
- OpenCV-Python
- PyTorch (with CUDA support)
- OpenVINO (for inference optimization)
- pyzbar (for QR code processing)
- numpy
- Other dependencies (see requirements.txt)

## Quick Start

1. Clone the repository
```bash
git clone https://github.com/Yoasobisong/gongxun-image-code.git
cd gongxun-image-code
```

2. Install dependencies
```bash
pip3 install -r requirements.txt
```

3. Run examples
```bash
# Object Detection
python3 code/yolo_detect.py

# QR Code Recognition
python3 code/qr_code.py

# Line Detection
python3 code/line_detect.py
```

## Usage Guide

- Object detection module supports custom model import
- QR code recognition supports multiple code formats
- Line detection parameters can be adjusted for different scenarios
- Supports real-time video stream processing on Jetson Nano

## Performance Optimization

- Optimized for Jetson Nano using TensorRT
- Supports OpenVINO acceleration
- Multi-threading for real-time processing
- Memory optimization for embedded deployment

## Maintainer

- [@Yoasobisong](https://github.com/Yoasobisong)

## Contact

- Email: 3133824384@qq.com
- GitHub: [@Yoasobisong](https://github.com/Yoasobisong)

## License

[MIT](LICENSE) © Yoasobisong 