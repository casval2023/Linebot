# main.py
# 必要なクラスを他のファイルからインポートします。
from config_loader import ConfigLoader
from ngrok_manager import NgrokManager
from line_bot import LineBot
# from youri_bot import YouriBot

# このスクリプトが直接実行された時だけ、以下のコードが実行されます。
if __name__ == '__main__':
    # 設定ファイル 'settings.json' を読み込むために ConfigLoader クラスを使用します。
    config_loader = ConfigLoader('settings.json')

    # 設定ファイルから読み込んだ設定を取得します。
    settings = config_loader.settings

    # Ngrokを管理するためのクラスをインスタンス化し、ngrokのAuthtokenを渡します。
    ngrok_manager = NgrokManager(settings['NGROK_AUTHTOKEN'])

    # ngrokによって生成されたWebhook URLを出力します。
    print(f"Webhook URL: {ngrok_manager.webhook_url}")

    # LINE Botのインスタンスを作成します。これには、設定から取得したアクセストークンと
    # チャネルシークレットを渡します。
    bot = LineBot(settings['LINE_ACCESS_TOKEN'], settings['LINE_CHANNEL_SECRET'])
    # bot = YouriBot(settings['LINE_ACCESS_TOKEN'], settings['LINE_CHANNEL_SECRET'])

    # Flaskアプリケーションを作成します。
    app = bot.create_app()

    # アプリケーションを起動します。これにより、Webサーバーが起動し、
    # LINEからのリクエストを待機する状態になります。
    app.run()
