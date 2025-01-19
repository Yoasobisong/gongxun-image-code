# Industrial Training Competition Computer Vision Code

This repository contains computer vision code implementations for industrial training competition robotics tasks, including object detection, QR code recognition, and line detection modules. The code is specifically optimized for deployment on Jetson Nano platform.

## Demo

Below is a demo video showing material detection in action:

https://user-images.githubusercontent.com/YOUR_USER_ID/gongxun-image-code/assets/runs/mat_o.mp4

<div align="center">
  <video src="runs/mat_o.mp4" width="640" height="480" controls>
    Your browser does not support the video tag.
  </video>
</div>

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
- Implements YOLO-based material detection
- Supports real-time object detection and tracking
- Features:
  - Multi-class material detection
  - Bounding box visualization
  - Confidence score filtering
  - Real-time processing optimization

#### 2. QR Code Recognition (`qr_code.py`)
- Implements QR code detection and decoding
- Features:
  - Multi-format QR code support
  - Real-time detection
  - Error correction
  - Position tracking

#### 3. Line Detection (`line_detect.py`)
- Implements line and geometric feature detection
- Features:
  - Straight line detection
  - Curve detection
  - Edge detection
  - Perspective transformation

#### 4. Camera Operations (`cam_open.py`)
- Manages camera input and video streaming
- Features:
  - Multiple camera support
  - Frame rate optimization
  - Auto-exposure control
  - Image preprocessing

### Supporting Modules

#### 5. Main Competition Logic (`gongxun.py`)
- Coordinates all modules for competition tasks
- Implements state machine for task switching
- Handles competition timing and scoring
- Integrates all subsystem controls

#### 6. OpenVINO Inference (`openvino_detect.py`)
- Optimizes model inference using OpenVINO
- Features:
  - Model optimization for Jetson Nano
  - Inference acceleration
  - Memory usage optimization
  - Batch processing support

#### 7. Web Communication (`send_web.py`)
- Handles web-based data transmission
- Features:
  - Real-time data streaming
  - Status reporting
  - Remote control interface
  - Error logging

#### 8. Serial Communication (`serial_deal.py`)
- Manages serial port communication
- Features:
  - Protocol implementation
  - Data synchronization
  - Error handling
  - Device control

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

## Quick Start

1. Clone the repository
```bash
git clone https://github.com/Yoasobisong/gongxun-image-code.git
cd gongxun-image-code
```

2. Install dependencies


3. Run examples
```bash
# Object Detection
python3 code/yolo_detect.py

# QR Code Recognition
python3 code/qr_code.py

# Line Detection
python3 code/line_detect.py

# Full Competition Mode
python3 code/gongxun.py
```

## Usage Guide

### Object Detection
- Supports custom model import via YOLO format
- Adjustable confidence thresholds
- Real-time visualization options
- Multiple detection classes support

### QR Code Recognition
- Supports multiple QR code formats
- Adjustable scan frequency
- Position tracking capabilities
- Error correction levels

### Line Detection
- Adjustable parameters for different scenarios
- Multiple detection algorithms
- Custom filter options
- Real-time processing support

### System Integration
- Modular design for easy customization
- Comprehensive logging system
- Error handling and recovery
- Performance monitoring

## Performance Optimization

- Optimized for Jetson Nano using TensorRT
- OpenVINO acceleration for inference
- Multi-threading for real-time processing
- Memory optimization for embedded deployment
- Custom CUDA kernels for specific operations

## Maintainer

- [@Yoasobisong](https://github.com/Yoasobisong)

## Contact

- Email: 3133824384@qq.com
- GitHub: [@Yoasobisong](https://github.com/Yoasobisong)

## License

[MIT](LICENSE) © Yoasobisong 