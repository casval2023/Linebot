# line_bot.py
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# LineBot クラスを定義します。
# このクラスは、LINE Bot APIとのやり取りを管理するためのメソッドを含んでいます。
class LineBot:
    # コンストラクタでは、LINE Bot APIとWebhookHandlerの初期化を行います。
    def __init__(self, access_token, channel_secret):
        # LineBotApiオブジェクトを作成し、LINEのアクセストークンを設定します。
        self.line_bot_api = LineBotApi(access_token)
        # WebhookHandlerオブジェクトを作成し、LINEのチャネルシークレットを設定します。
        self.handler = WebhookHandler(channel_secret)

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
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text),
            )

        # Flaskアプリケーションのインスタンスを返します。
        return app
