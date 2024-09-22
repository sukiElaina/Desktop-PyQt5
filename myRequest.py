import requests
import json
import os
class AIRequest:
    def __init__(self):
        self.load_config()  # 新增方法来加载配置
        self.url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={self.group_id}"
        self.headers = {"Authorization":f"Bearer {self.api_key}", "Content-Type":"application/json"}
        self.request_body = {
            "model":"abab6.5-chat",
            "tokens_to_generate":5000,
            "reply_constraints":{"sender_type":"BOT", "sender_name":"芙宁娜"},
            "messages":[],
            "bot_setting":[
                {
                    "bot_name":"芙宁娜",
                    "content":"1.是一个桌宠 2.只能回复文本消息。3.每次回复不超过50个字。",
                }
            ],
        }
    def get_Response(self, message):
        # 清空之前的响应以避免混淆
        self.response = None
        
        # 将用户消息添加到请求体中
        self.request_body["messages"].append({
            "sender_type": "USER",
            "sender_name": "Furina_Bot_User",
            "text": message
        })

        # 确保请求体中的消息数量不超过最大限制
        if len(self.request_body["messages"]) > self.message_max:
            self.request_body["messages"] = self.request_body["messages"][-self.message_max:]

        try:
            # 发送请求
            response = requests.post(self.url, headers=self.headers, json=self.request_body)
            response.raise_for_status()  # 如果响应状态码不是200，将引发异常
            reply = response.json().get('reply')  # 使用 get 方法安全获取 'reply'
            
            if reply:  # 检查回复是否存在
                # 将Bot的回复添加到请求体
                new_messages = response.json()["choices"][0]["messages"]
                        # 检查新消息数量，确保总数不超过message_max条
                if len(self.request_body["messages"]) + len(new_messages) > self.message_max:
                    self.request_body["messages"] = self.request_body["messages"][-(self.message_max - len(new_messages)):]

                self.request_body["messages"].extend(new_messages)
                return reply
            else:
                return ""
        
        except requests.exceptions.RequestException as e:
            return ""

    def load_config(self):
        # 从 JSON 配置文件中加载配置
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.group_id = config['group_id']
            self.api_key = config['api_key']
            self.message_max = config['message_max']
            # print("group_id:", self.group_id, "api_key:", self.api_key, "message_max:", self.message_max)
class TTSRequest:
    def __init__(self):
        self.url = f"http://127.0.0.1:5000/tts"
        self.params = {
            "character": "【原神】芙宁娜",
            "emotion": "default",
            "text": '',
            "speed": 0.9,
            "stream": False,
            "save_temp": True,
        }
        
    def TTSwrite(self, text):
        self.params['text'] = text
        self.response = requests.post(self.url, json=self.params)
        
        # 尝试删除已存在的文件
        if os.path.exists('output.wav'):
            try:
                os.remove('output.wav')
            except Exception as e:
                pass

        # 写入新文件
        try:
            with open('output.wav', 'wb') as f:
                f.write(self.response.content)
        except Exception as e:
            pass
