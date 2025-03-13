RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
BLUE = '\033[94m'
from flask import Flask, Response
import cv2
import threading


class VideoStream:
    def __init__(self, port):
        self.app = Flask(__name__)
        self.latest_frame = None
        self.port = port
        self.app.add_url_rule('/video', 'video', self.video)
        self.running = True

    def update_frame(self, frame):
        """接收图像并更新最新帧"""
        self.latest_frame = frame

    def generate_frames(self):
        """生成最新帧的字节流"""
        while self.running:
            if self.latest_frame is not None:
                ret, buffer = cv2.imencode('.jpg', self.latest_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        print(f"{YELLOW}Video thread end{RESET}")

    def video(self):
        """处理视频流请求"""
        return Response(self.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def run(self):
        """运行Flask应用"""
        self.app.run(host='0.0.0.0', port=self.port)

if __name__ == '__main__':
    video_stream = VideoStream(port=5000)  # 创建 VideoStream 实例
    cap = cv2.VideoCapture(0)  # 在外部创建 cap 对象
    
    # 启动Flask应用在一个单独的线程中
    flask_thread = threading.Thread(target=video_stream.run)
    flask_thread.start()

    try:
        while True:
            ret, frame = cap.read()
            if ret:
                video_stream.update_frame(frame)  # 更新最新帧
            else:
                break
    except KeyboardInterrupt:
        print("关闭摄像头")
    finally:
        cap.release()  # 关闭摄像头
