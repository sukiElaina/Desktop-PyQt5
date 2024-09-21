import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("透明背景视频播放器")
        self.setGeometry(100, 100, 800, 600)
        # self.setAttribute(Qt.WA_TranslucentBackground)  # 设置为透明背景
        self.setWindowFlag(Qt.FramelessWindowHint)  # 去掉边框

        # 创建视频播放器和布局
        self.video_widget = QVideoWidget(self)
        self.video_widget.setAttribute(Qt.WA_TranslucentBackground)  # 让视频控件也是透明背景
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_widget)

        # 创建主窗口部件
        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # 创建媒体播放器
        self.media_player = QMediaPlayer(self)
        self.media_player.setVideoOutput(self.video_widget)

        # 设置视频文件路径（确保此路径指向有效的 MP4 文件）
        video_path = "E:\\Computer\\Desktop\\2.mp4"  # 请替换为实际视频路径
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))

        # 创建播放按钮
        self.play_button = QPushButton("播放", self)
        self.play_button.clicked.connect(self.play_video)
        self.layout.addWidget(self.play_button)

    def play_video(self):
        self.media_player.play()