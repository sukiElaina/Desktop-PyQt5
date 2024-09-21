# from videoplayer import VideoPlayer 
from pix import Pix
from PyQt5.QtWidgets import QApplication
import sys
import subprocess
import json
if __name__ == "__main__":
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        TTS_path = config['TTS_path']
    subprocess.run(TTS_path,shell=True)
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