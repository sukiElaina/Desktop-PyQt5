import os
import random
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QTimer, Qt, QPoint, QUrl, QThread
from PyQt5.QtGui import QPainter, QPixmap,QFont
from myRequest import AIRequest, TTSRequest
class AIThread(QThread):
    def __init__(self, input_text, ai_request,tts,player1,tts_path):
        super().__init__()
        self.tts_path = tts_path
        self.player1 = player1
        self.input_text = input_text
        self.ai_request = ai_request
        self.tts = tts
        self.response = ""

    def run(self):
        # 调用 AI 请求并获取响应
        self.response = self.ai_request.get_Response(self.input_text)
        # 请求完成后，获取响应并处理
        reply = self.response
        # 调用 TTS 请求并播放声音
        self.tts.TTSwrite(reply)
        # 清除任何已设置的媒体
        self.player1.setMedia(QMediaContent())  # 清空媒体内容
        media_content = QMediaContent(QUrl.fromLocalFile(os.path.join(self.tts_path, "output.wav")))
        self.player1.setMedia(media_content)
        self.player1.play()
class Pix(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pix")  # 设置窗口标题
        self.resize(800, 600)  # 设置窗口大小

        # 创建按钮和文本输入框
        self.button = QPushButton("发送", self)
        self.button.setGeometry(350, 60, 100, 30)  # 设置按钮的位置和大小

        self.text_input = QLineEdit(self)  # 创建文本输入框并设置默认内容
        self.text_input.setPlaceholderText("你想对芙宁娜说什么？")  # 设置提示文字
        self.text_input.setGeometry(350, 10, 150, 35)  # 设置文本框的位置和大小
        self.text_input.setFont(QFont("华文新魏", 10))  # 设置字体和大小

        # 设置基本属性
        self.timer = QTimer(self)
        self.idx = 1
        self.idx_min = 1
        self.idx_max = 625
        self.image_path = "E:\\Computer\\Desktop\\static\\2"
        self.tts_path = "E:\\Computer\\Desktop"
        self.player = QMediaPlayer(self)
        self.player1 = QMediaPlayer(self)
        self.ai = AIRequest()
        self.tts = TTSRequest()
        self.movie_state = 0
        self.is_circle = True
        self.is_music = True

        random.seed()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.button.clicked.connect(self.on_button_click)

        self.timer.setInterval(32)
        self.timer.timeout.connect(self.movie_timer)
        self.timer.start()
        
        # 添加定时器来检查 player1 的状态
        self.volume_timer = QTimer(self)
        self.volume_timer.setInterval(100)  # 每100毫秒检查一次
        self.volume_timer.timeout.connect(self.check_player1_status)
        self.volume_timer.start()
    def check_player1_status(self):
        # 检查 player1 是否在播放
        if self.player1.state() == QMediaPlayer.PlayingState:
            # player1 正在播放，减少 player 的音量为一半
            self.player.setVolume(50)  # 假设默认音量为 100，设置为 50
        else:
            # player1 没有播放，还原 player 的音量
            self.player.setVolume(100)  # 还原到默认音量

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
            
    def on_button_click(self):
        input_text = self.text_input.text()
        self.text_input.clear()
        # 创建线程并执行
        self.thread = AIThread(input_text, self.ai,self.tts,self.player1,self.tts_path)
        self.thread.start()

