import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QTimer, Qt, QObject, QPoint, QUrl
from PyQt5.QtGui import QPainter, QPixmap


class Pix(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Play")
        self.layout = QHBoxLayout()
        self.label = QLabel()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)  # 设置布局
        self.timer = QTimer(self)
        self.idx = 1
        self.idx_min = 1
        self.idx_max = 625
        self.image_path = "E:\\Computer\\Desktop\\static\\2"
        self.player = QMediaPlayer(self)
        self.movie_state = 0  # 0表示非动画状态，1表示动画状态
        self.is_circle = True  # 是否循环播放
        self.is_music = True  # 是否播放音乐

        random.seed()  # 初始化随机数种子
        self.resize(800, 600)
        self.setWindowTitle("Pix")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)  # 开启鼠标追踪

        self.timer.setInterval(33)
        self.timer.timeout.connect(self.movie_timer)
        self.timer.start()

    def play_music(self):
        if self.is_music:
            media_content = QMediaContent(QUrl.fromLocalFile(os.path.join(self.image_path, "music.wav")))
            self.player.setMedia(media_content)
            self.player.play()
            print("play music")
    def stop_music(self):
        if self.is_music:
            self.player.stop()
            print("stop music")

    def movie_timer(self):
        if self.is_circle:
            self.movie_circle()
        else:
            self.movie_single()

    def movie_circle(self):
        if self.movie_state != 1:
            self.movie_state = 1
        
        if self.idx == 1:
            self.play_music()

        if self.idx == self.idx_max:
            self.stop_music()

        self.idx = self.idx % self.idx_max + 1
        self.pixmap = QPixmap(os.path.join(self.image_path, f"{self.idx}.png"))
        self.update()

    def movie_single(self):
        if self.idx < self.idx_max:
            if self.movie_state != 1:
                self.movie_state = 1
            if self.idx == 1 or self.is_music:
                self.play_music()
            self.idx = (self.idx + 1) % self.idx_max + 1
            self.pixmap = QPixmap(os.path.join(self.image_path, f"{self.idx}.png"))
            self.update()
        else:
            self.stop_music()
            self.is_music = False
            if self.movie_state != 0:
                self.movie_state = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStartPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragStartPosition = QPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.dragStartPosition)
            event.accept()

    def paintEvent(self, event):
        painter = QPainter(self)
        if hasattr(self, 'pixmap'):
            painter.drawPixmap(0, 0, self.pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Pix()
    window.show()
    sys.exit(app.exec_())
