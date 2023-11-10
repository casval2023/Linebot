# config_loader.py
import json  # jsonモジュールをインポートします。これによりJSON形式のファイルを扱うことができます。

# ConfigLoaderという名前のクラスを定義します。
class ConfigLoader:
    # クラスの初期化メソッドです。インスタンスが作成されるときに自動的に呼び出されます。
    def __init__(self, file_name):
        self.file_name = file_name  # file_nameという引数をインスタンス変数に代入します。
        self.settings = self.load_settings()  # load_settingsメソッドを呼び出して、設定を読み込みます。

    # 設定をファイルから読み込むメソッドです。
    def load_settings(self):
        # ファイルを読み込むコンテキストを開始します。'r'は読み込みモードを意味します。
        with open(self.file_name, 'r') as file:
            # json.loadを使って、開いたファイルの内容をJSONとして読み込みます。
            # 読み込んだデータはPythonの辞書形式に変換されます。
            return json.load(file)
