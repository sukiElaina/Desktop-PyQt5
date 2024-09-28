import os
import random
import time
from PyQt5.QtWidgets import QMainWindow, QPushButton,QMenu,QAction,QSystemTrayIcon, QLineEdit,QApplication,QTextEdit
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QTimer, Qt, QPoint, QUrl, QThread,pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap,QFont,QIcon
from myRequest import AIRequest, TTSRequest
class AIThread(QThread):
    reply_signal = pyqtSignal(str)
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
        # 发送信号给主线程
        self.reply_signal.emit(reply)
        
class Pix(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(os.getcwd() + "\\static\\icon.png"))  # 设置窗口图标
        self.setWindowTitle("Pix")  # 设置窗口标题
        self.resize(1280, 720)  # 设置窗口大小
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)  # 设置窗口置顶
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        myfont = QFont("华文新魏", 10)  # 设置字体和大小
        # 创建按钮和文本输入框
        self.button_greater = QPushButton("+", self)
        self.button_greater.setFont(myfont)  # 设置字体和大小
        self.button_greater.setGeometry(540, 160, 100, 30)  # 设置按钮的位置和大小
    
        self.button_less = QPushButton("-", self)
        self.button_less.setFont(myfont)  # 设置字体和大小
        self.button_less.setGeometry(670, 160, 100, 30)  # 设置按钮的位置和大小

        self.text_input = QLineEdit(self)  # 创建文本输入框并设置默认内容
        self.text_input.setPlaceholderText("你想对芙宁娜说什么？")  # 设置提示文字
        self.text_input.setGeometry(540, 110, 230, 35)  # 设置文本框的位置和大小
        self.text_input.setFont(myfont)  # 设置字体和大小

        self.reply_display = QTextEdit(self)  # 创建 QLabel 来显示回复内容
        self.reply_display.setGeometry(540, 0, 230, 80)  # 设置显示框的位置和大小
        self.reply_display.setFont(myfont)  # 设置字体
        self.reply_display.setReadOnly(True)  # 设置为只读
        # 在初始化时可以设置一个初始的背景图
        initial_image_path = (os.getcwd() + "\\static\\reply_bg.png")
        initial_image_path = initial_image_path.replace("\\", "/")  # 路径中不能有反斜杠
        # 设置背景图片、透明和内边距
        self.reply_display.setStyleSheet(f"""
            QTextEdit {{
                background-image: url({initial_image_path});
                border: none;
                padding: 0 30px;  /* 增加内边距来适应气泡，一个参数就是上下左右同参数，两个参数就是上下同参数，左右同参数 */
                selection-background-color: lightblue;  /* 可选：选中文本的背景色 */
                selection-color: white;  /* 可选：选中文本的颜色 */
            }}
        """)
        # 设置基本属性
        self.timer = QTimer(self)
        self.idx = 1
        self.idx_max = 625
        # 将 tts_path 设置为当前程序所处文件夹
        self.pixscale=1
        self.tts_path = os.getcwd()
        self.image_path_base = os.path.join(self.tts_path, "static\\movies")
        self.image_path = os.path.join(self.image_path_base, "initial")
        
        self.player = QMediaPlayer(self)
        self.player_default_volume = 60  # 设置默认音量大小
        self.player.setVolume(self.player_default_volume)  # 设置默认音量
        self.player1 = QMediaPlayer(self)
        self.ai = AIRequest()
        self.tts = TTSRequest()
        self.movie_state = 0
        self.is_circle = False
        self.is_music = True
        self.folers=self.read_file_folders()
        print(self.folers)

        random.seed(time.time())
        
        self.text_input.returnPressed.connect(self.on_button_click)

        # 建立按钮事件
        self.button_greater.clicked.connect(self.pixmap_scale_greater)
        self.button_less.clicked.connect(self.pixmap_scale_less)

        self.timer.setInterval(32)
        self.timer.timeout.connect(self.movie_timer)
        self.timer.start()
        
        # 添加定时器来检查 player1 的状态
        self.volume_timer = QTimer(self)
        self.volume_timer.setInterval(100)  # 每100毫秒检查一次
        self.volume_timer.timeout.connect(self.check_player1_status)
        self.volume_timer.start()
        
        
        # 初始化托盘图标
        self.init_tray_icon()
        
        
    def init_tray_icon(self):
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.getcwd() +"\\static\\icon.png"))

        # 创建托盘菜单
        tray_menu = QMenu()
        
        # 添加打开和退出选项
        hide_action = QAction("隐藏", self)
        hide_action.triggered.connect(self.hide)  # 点击后隐藏窗口

        show_action = QAction("显示", self)
        show_action.triggered.connect(self.show)  # 点击后显示窗口

        exit_action = QAction("退出", self)
        exit_action.triggered.connect(QApplication.instance().quit)  # 点击后退出应用

        # 偏好设置子菜单
        preference_menu = QMenu("偏好设置", self)
        
        # 添加文本框显示选项
        self.text_input_action = QAction("显示文本框", self, checkable=True)
        self.text_input_action.setChecked(True)  # 默认勾选
        self.text_input_action.triggered.connect(self.toggle_text_input)

        # 添加按钮显示选项
        self.button_action = QAction("显示按钮", self, checkable=True)
        self.button_action.setChecked(True)  # 默认勾选
        self.button_action.triggered.connect(self.toggle_button)
        
        # 显示气泡
        self.reply_display_action = QAction("显示回复", self, checkable=True)
        self.reply_display_action.setChecked(True)  # 默认勾选
        self.reply_display_action.triggered.connect(self.toggle_reply_display)

        # 将这些选项添加到偏好设置子菜单
        preference_menu.addAction(self.text_input_action)
        preference_menu.addAction(self.button_action)

        # 将菜单添加到系统托盘
        tray_menu.addAction(hide_action)
        tray_menu.addAction(show_action)
        tray_menu.addAction(exit_action)
        tray_menu.addMenu(preference_menu)  # 添加偏好设置

        # 将菜单添加到系统托盘
        self.tray_icon.setContextMenu(tray_menu)

        # 显示系统托盘图标
        self.tray_icon.show()

        # 连接系统托盘图标的双击事件
        self.tray_icon.activated.connect(self.tray_icon_activated)
    def toggle_text_input(self, checked):
        self.text_input.setVisible(checked)

    def toggle_button(self, checked):
        self.button_greater.setVisible(checked)
        self.button_less.setVisible(checked)
        
    def toggle_reply_display(self, checked):
        self.reply_display.setVisible(checked)

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()  # 双击时显示窗口

    def check_player1_status(self):
        # 检查 player1 是否在播放
        if self.player1.state() == QMediaPlayer.PlayingState:
            # player1 正在播放，减少 player 的音量为一半
            self.player.setVolume(int(self.player_default_volume / 2))  # 假设默认音量为 100，设置为 50
        else:
            # player1 没有播放，还原 player 的音量
            self.player.setVolume(self.player_default_volume)  # 还原到默认音量

    def play_music(self):
        if self.is_music:
            media_content = QMediaContent(QUrl.fromLocalFile(os.path.join(self.image_path, "music.wav")))
            self.player.setMedia(media_content)
            self.player.play()

    def stop_music(self):
        if self.is_music:
            self.player.stop()

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
            if self.idx == 1 and self.is_music:
                self.play_music()
            self.idx = self.idx% self.idx_max + 1
            self.pixmap = QPixmap(os.path.join(self.image_path, f"{self.idx}.png"))
            self.update()
        else:
            self.stop_music()
            self.is_music = False
            if self.movie_state != 0:
                self.movie_state = 0
            self.movie_single_end()  
            
            
    def movie_single_end(self):
        random_key=random.choice(list(self.folers.keys()))
        self.image_path = os.path.join(self.image_path_base, random_key)
        self.idx = 1
        self.idx_max = self.folers[random_key][0]
        self.is_music = self.folers[random_key][1]
        print(f"random_key：{random_key}, idx_max：{self.idx_max}, is_music：{self.is_music}")
        
        
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
            scaled_pixmap = self.pixmap.scaled(int(640*self.pixscale), int(360*self.pixscale) , Qt.KeepAspectRatio, Qt.SmoothTransformation)
            painter.drawPixmap(int(320*(1.5-self.pixscale)), int(180*(1.5-self.pixscale)), scaled_pixmap)
            
    def on_button_click(self):
        if self.text_input.text()!= "":
            input_text = self.text_input.text()
            self.text_input.clear()
            # 创建线程并执行
            self.thread = AIThread(input_text, self.ai,self.tts,self.player1,self.tts_path)
            self.thread.reply_signal.connect(self.update_reply_display)
            self.thread.start()
        else:
            print("输入不能为空")
    def update_reply_display(self, reply):
        self.reply_display.setText(reply)
    def pixmap_scale_greater(self):
        if self.pixscale < 1.5:
            self.pixscale += 0.1
            
    def pixmap_scale_less(self):
        if self.pixscale > 0.5:
            self.pixscale -= 0.1
            
    def read_file_folders(self):
        png_count_dict = {}
        # 遍历基本文件夹中的所有子文件夹
        for folder_name in os.listdir(self.image_path_base):
            folder_path = os.path.join(self.image_path_base, folder_name)
            
            # 确保这是一个目录
            if os.path.isdir(folder_path):
                # 统计该文件夹中的 PNG 图片数量
                png_count = 0
                is_music = False
                for file in os.listdir(folder_path):
                    if file.endswith('.png'):
                        png_count += 1
                        
                    if file == "music.wav":
                        is_music = True
                # 将文件夹名和对应的 PNG 数量存入字典
                png_count_dict[folder_name] = [png_count,is_music]

        return png_count_dict