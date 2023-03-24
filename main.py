import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials



scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#ダウンロードしたjsonファイルをドライブにアップデートした際のパス
json = '/content/afdb2023-dee7ec1a7c0d.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)

gc = gspread.authorize(credentials)

#書き込み先のスプレッドシートキーを追加
SPREADSHEET_KEY = '1T3K4khm4CQ3JcWOKO1NtJFie37WEDxDWJ7SiIOlSKTk'

#共有設定したスプレッドシートの1枚目のシートを開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

#全てを取得
list_of_lists=worksheet.get_all_values()

df = pd.DataFrame(list_of_lists[1:], columns=list_of_lists[0])


# ここからUI
st.set_page_config(
    page_title="マネートラックアフィリエイターリスト", 
    layout="wide")


st.subheader('マネートラックアフィリエイターリスト')

# Streamlitで検索キーワードを入力
search_term = st.text_input('検索キーワードを入力してください', '')

# 検索キーワードを含む行をフィルタリング
if search_term:
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(search_term).any(), axis=1)]
else:
    filtered_df = df

# インデックス番号を非表示にする
# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Streamlitでデータフレームを表示
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.write('キーワード: ' + search_term)
st.table(filtered_df)
