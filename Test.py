import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

class VideoPlayer(QMainWindow):
    def __init__(self):
        super(VideoPlayer, self).__init__()
        self.setWindowTitle("PyQt5 Video Player with Transparency")
        self.setGeometry(100, 100, 800, 600)

        # 标签用于显示视频帧
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)

        # 使用OpenCV读取视频
        self.video_capture = cv2.VideoCapture("E:\\MMD\\视频\\CaliforniaGurls.mp4")
        
        # 定时器更新视频帧
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)  # 每33ms更新一次，约30帧每秒

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            # 将BGR转换为RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 将图像转换为QPixmap并显示
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QPixmap.fromImage(QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888))
            self.label.setPixmap(q_img)

    def closeEvent(self, event):
        self.video_capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
