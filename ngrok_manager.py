# ngrok_manager.py
import os
from pyngrok import ngrok
from pyngrok.conf import PyngrokConfig

class NgrokManager:
    def __init__(self, authtoken):
        self.authtoken = authtoken
        self.webhook_url = self.start_ngrok()

    def start_ngrok(self):
        # 既に実行中のngrokプロセスを終了します（もしあれば）。
        os.system('kill -9 $(pgrep ngrok)')
        # 認証トークンを設定した状態でngrokセッションを開始します。
        return ngrok.connect(addr='127.0.0.1:5000', pyngrok_config=PyngrokConfig(start_new_session=True))
