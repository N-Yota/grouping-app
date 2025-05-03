# my_grouping_tool/main.py

import pandas as pd
import requests
import io
import os

from .core_logic import process_grouping  # ← 複雑な処理の起点関数（仮）

def run_from_url(url):
    try:
        # URLがローカルファイルパスかウェブURLかを判断
        if os.path.isfile(url):
            df = pd.read_excel(url, engine='openpyxl')
        else:
            content = requests.get(url).content
            df = pd.read_excel(io.BytesIO(content), engine='openpyxl')
        
        result_str = process_grouping(df)
        
        # 結果が文字列で返されるので、そのまま返す
        return result_str
    
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"




