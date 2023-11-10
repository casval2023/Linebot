import streamlit as st
import json
import subprocess

# タイトルの設定
st.title("Settings Configuration")

# 設定ファイルのパス
config_file_path = 'settings.json'

# 設定入力用のフォームを作成
with st.form("settings_form"):
    st.write("Please enter the configuration settings:")
    ngrok_authtoken = st.text_input("NGROK_AUTHTOKEN")
    line_access_token = st.text_input("LINE_ACCESS_TOKEN")
    line_channel_secret = st.text_input("LINE_CHANNEL_SECRET")
    submitted = st.form_submit_button("Submit")

    # フォームが送信された場合、入力された設定をJSONファイルとして保存
    if submitted:
        settings = {
            "NGROK_AUTHTOKEN": ngrok_authtoken,
            "LINE_ACCESS_TOKEN": line_access_token,
            "LINE_CHANNEL_SECRET": line_channel_secret
        }
        with open(config_file_path, 'w') as config_file:
            json.dump(settings, config_file, indent=4)

        st.success("Settings saved successfully!")
        # `main.py`をサブプロセスとして起動
        subprocess.run(["python", "main.py"])
