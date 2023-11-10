# line_bot.py
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from line_bot import LineBot  # your_line_bot_fileは、LineBotクラスを含むファイルの名前です。
import torch
from transformers import AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM  # your_model_libraryは、モデルクラスを含むライブラリの名前です。

# LineBot クラスを定義します。
# このクラスは、LINE Bot APIとのやり取りを管理するためのメソッドを含んでいます。
class YouriBot(LineBot):
    # コンストラクタでは、LINE Bot APIとWebhookHandlerの初期化を行います。
    def __init__(self, access_token, channel_secret):
        # LineBotApiオブジェクトを作成し、LINEのアクセストークンを設定します。
        self.line_bot_api = LineBotApi(access_token)
        # WebhookHandlerオブジェクトを作成し、LINEのチャネルシークレットを設定します。
        self.handler = WebhookHandler(channel_secret)
        # トークナイザーとモデルの準備
        self.tokenizer = AutoTokenizer.from_pretrained(
            "rinna/youri-7b-chat-gptq"
        )
        self.model = AutoGPTQForCausalLM.from_quantized(
            "rinna/youri-7b-chat-gptq", 
            device_map="auto",
            use_safetensors=True
        )

    def generate_response(self, prompt):
        # 推論の実行
        token_ids = self.tokenizer.encode(
            prompt, 
            add_special_tokens=False, 
            return_tensors="pt")
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids=token_ids.to(self.model.device),
                max_new_tokens=200,
                do_sample=True,
                temperature=0.5,
                pad_token_id=self.tokenizer.pad_token_id,
                bos_token_id=self.tokenizer.bos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        return self.tokenizer.decode(
            output_ids[0][token_ids.size(1):], 
            skip_special_tokens=True
        )

    # Flaskアプリケーションを作成するメソッドです。
    def create_app(self):
        # Flaskのインスタンスを作成します。
        app = Flask(__name__)

        # '/test'のパスにアクセスがあった場合の処理を定義します。
        @app.route("/test")
        def test():
            # テスト用のエンドポイントなので、"TEST OK"というレスポンスを返します。
            return "TEST OK"

        # '/'のパスにPOSTリクエストがあった場合の処理を定義します。
        # これはLINE PlatformからのWebhookを処理するためのエンドポイントです。
        @app.route("/", methods=['POST'])
        def callback():
            # LINE Platformからのリクエストに含まれる署名を取得します。
            signature = request.headers['X-Line-Signature']
            # リクエストの本体（body）をテキストとして取得します。
            body = request.get_data(as_text=True)
            # リクエストの内容をログに記録します。
            app.logger.info("Request body: " + body)

            # 署名を検証し、イベントハンドラを呼び出します。
            try:
                self.handler.handle(body, signature)
            except InvalidSignatureError:
                # 署名が無効な場合は、エラーメッセージを出力し、400エラーを返します。
                print("Invalid signature. Please check your channel access token/channel secret.")
                abort(400)

            # すべて正常に処理された場合は、'OK'のレスポンスを返します。
            return 'OK'

        # MessageEventとTextMessageを処理するイベントハンドラを定義します。
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            # 受信したメッセージの内容をログに出力します。
            print("event.message.text:{}".format(event.message.text))
            # ユーザーに送られたテキストメッセージと同じ内容で返信します。

            prompt = f"設定: あなたの優秀なAIアシスタントです。\nユーザー: {event.message.text}\nシステム: "
            print(f"prompt:{prompt}")
            # AIによるレスポンス生成
            response_text = self.generate_response(prompt)
            print(f"response_text:{response_text}")

            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text),
            )

        # Flaskアプリケーションのインスタンスを返します。
        return app
