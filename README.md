# 工训赛图像代码

本仓库包含了工训赛相关的计算机视觉代码实现，主要功能包括：

## 功能模块

- 目标检测
- 二维码识别
- 线条检测
- 摄像头操作

## 目录结构

- `code/`: 主要代码文件
- `images/`: 测试图片
- `mat_data/`: 数据文件
- `ann_pt/`, `mat_vino/`, `ann_vino/`, `mat_pt/`: 模型相关文件

## 环境要求

- Python 3.x
- OpenCV
- PyTorch
- 其他依赖库（详见代码中的import）

## 使用说明

1. 克隆仓库
```bash
git clone https://github.com/Yoasobisong/工训赛图像代码.git
```

2. 安装依赖
```bash
pip install -r requirements.txt  # (如果有requirements.txt)
```

3. 运行相应的Python脚本
```bash
python code/yolo_detect.py  # 目标检测
python code/qr_code.py      # 二维码识别
python code/line_detect.py  # 线条检测
```

## 联系方式

- 邮箱：3133824384@qq.com
- GitHub：[@Yoasobisong](https://github.com/Yoasobisong) 