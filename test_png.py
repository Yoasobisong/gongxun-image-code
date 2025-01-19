import io
import cv2
import threading
import queue
import time
from sixel import SixelWriter
from ultralytics import YOLO

# 数据结构
class Data:
    def __init__(self, identifier, frame, ending=False):
        self.identifier = identifier
        self.frame = frame
        self.ending = ending

# 初始化模型和摄像头
model = YOLO("./mat_pt/mat.pt")
cap = cv2.VideoCapture(0)

# 创建队列
read_queue = queue.Queue(maxsize=4)  # 设置队列最大容量
write_queue = queue.Queue(maxsize=4)  # 设置队列最大容量

# 全局标识符
global_identifier = 0
lock = threading.Lock()

# 处理线程
def worker():
    global global_identifier
    while True:
        data = read_queue.get()
        if data.ending:
            break
        
        # 处理数据
        results = model.predict(source=data.frame, conf=0.8)
        # print(results)
        plot = results[0].plot()

        with lock:
            if data.identifier == global_identifier + 1:
                global_identifier += 1
                # Convert result image to bytes
                im_bytes = cv2.imencode(".png", plot)[1].tobytes()
                mem_file = io.BytesIO(im_bytes)
                write_queue.put(mem_file)

        read_queue.task_done()

# 启动处理线程
threads = []
for i in range(4):
    thread = threading.Thread(target=worker)
    thread.start()
    threads.append(thread)

frame_id = 0
start_time = time.time()
frames_processed = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 增加标识符并存储数据
    frame_id += 1
    small_frame = cv2.resize(frame, (320, 240))  # 调整大小
    data = Data(frame_id, small_frame)

    # 等待队列有空位置
    read_queue.put(data, block=True)

    # 计算处理帧率
    frames_processed += 1
    if time.time() - start_time >= 1:
        print(f"Processed frames in the last second: {frames_processed}")
        frames_processed = 0
        start_time = time.time()

    # 检查写队列
    while not write_queue.empty():
        write_queue.get()  # 处理写队列，避免积压

# 结束信号
for _ in range(4):
    read_queue.put(Data(0, None, ending=True))  # 发送结束信号

# 等待所有线程完成
read_queue.join()
for thread in threads:
    thread.join()

# 释放资源
cap.release()
