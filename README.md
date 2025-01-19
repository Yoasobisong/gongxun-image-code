# 工训赛图像处理代码

本仓库包含了工训赛相关的计算机视觉代码实现，用于机器人视觉任务处理。主要包括目标检测、二维码识别、线条检测等功能模块的实现。

## 主要功能

- **目标检测**: 使用YOLO模型进行物体识别和定位
- **二维码识别**: 实现二维码的检测和解码功能
- **线条检测**: 实现直线、曲线等几何特征的检测
- **摄像头操作**: 支持实时视频流处理和图像采集

## 项目结构

```
gongxun_demo/
├── code/              # 核心代码文件
│   ├── yolo_detect.py    # 目标检测实现
│   ├── qr_code.py        # 二维码识别
│   ├── line_detect.py    # 线条检测
│   └── cam_open.py       # 摄像头操作
├── images/            # 测试图片目录
├── mat_data/          # 训练数据和标注
├── ann_pt/            # 神经网络模型文件
└── mat_vino/          # OpenVINO优化模型
```

## 环境要求

- Python 3.x
- OpenCV-Python
- PyTorch
- OpenVINO (推理优化)
- pyzbar (二维码处理)
- numpy

## 快速开始

1. 克隆仓库
```bash
git clone https://github.com/Yoasobisong/gongxun-image-code.git
cd gongxun-image-code
```

2. 安装依赖
```bash
pip install -r requirements.txt  # (如果有requirements.txt)
```

3. 运行示例
```bash
# 目标检测
python code/yolo_detect.py

# 二维码识别
python code/qr_code.py

# 线条检测
python code/line_detect.py
```

## 使用说明

- 目标检测模块支持自定义模型导入
- 二维码识别支持多种码制
- 线条检测可调整参数适应不同场景
- 支持实时视频流处理

## 维护者

- [@Yoasobisong](https://github.com/Yoasobisong)

## 联系方式

- 邮箱：3133824384@qq.com
- GitHub：[@Yoasobisong](https://github.com/Yoasobisong)

## 许可证

[MIT](LICENSE) © Yoasobisong 