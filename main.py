# from videoplayer import VideoPlayer 
from pix import Pix
from PyQt5.QtWidgets import QApplication
import sys
import subprocess
if __name__ == "__main__":
    bat_file_path = r"E:\Computer\miHoYo-Inference\!启动!.bat"
    subprocess.run([bat_file_path], shell=True)
    app = QApplication(sys.argv)
    window = Pix()
    window.show()
    sys.exit(app.exec_())



# from myRequest import AIRequest, TTSRequest
# if __name__ == "__main__":
#     ai_test = AIRequest()
#     test = ai_test.get_Response("hi")
#     tts = TTSRequest()
#     tts.TTSwrite(test)
#     print(test)



