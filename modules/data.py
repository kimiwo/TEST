from dataclasses import dataclass
from typing import List
import json
import ipaddress
from datetime import date

@dataclass
class req_data:
    """リクエストデータを保持するクラス"""
    cloud :     str
    vrf :       str
    date :      str
    account :   str
    prefix :    List[str]
    dxgw_id :   str
    dxgw_name : str
    vgw_id :    str

    def __post_init__(self):
        """リクエストデータの整形を行う
        リクエストデータの整形を行い、AWSに関連するデータのみを抽出する
        """
        ### データの整形 ###
        try:
            self.prefix = [item for item in self.prefix if ipaddress.ip_network(item)]
        except ValueError:
            print("IPアドレスが無効です。")
            self.prefix = []
        # dateのデータフォーマットをYYYY-mm-ddに変換
        try:
            year, month, day = map(int, self.date.split("/"))
            self.date = str(date(year, month, day))
        except ValueError:
            print("Invalid date format")

@dataclass
class request_list:
    """リクエストデータのリストを保持するクラス
    Attributes:
        all_data (List[req_data]): リクエストデータのリスト
    Methods:
        __post_init__(): リクエストデータの整形を行う
    """
    all_data : List[req_data]
    def __post_init__(self):
        """リクエストデータの整形を行う
        リクエストデータの整形を行い、AWSに関連するデータのみを抽出する
        """
        ### データの整形 ###
        self.all_data = [
            req_data(**item) if isinstance(item, dict) else item for item in self.all_data
            if isinstance(item, (dict, req_data))
            and all(
                hasattr(item, key) if isinstance(item, req_data) else key in item
                for key in ['cloud', 'vrf', 'date', 'account', 'prefix', 'dxgw_id', 'dxgw_name', 'vgw_id']
            )
            and (
                item.cloud.lower() if isinstance(item, req_data) else item.get('cloud', '').lower()
            ) == 'aws'
        ]

class DataLoader:
    """DataLoaderクラス
    JSONファイルからデータを読み込むクラス
    
    Attributes:
        file_name (str): JSONファイルの名前
        load_data (List[req_data]): 読み込んだデータのリスト
    Methods:
        __init__(file_name: str): DataLoaderの初期化
        load_json(file_name: str): JSONファイルからデータを読み込む
        convert(data_item): 辞書のキーを特定の形式に変換する(ハイフンをアンダースコアに置換)
    """
    def __init__(self, file_name: str):
        """DataLoaderの初期化
        
        Args:
            file_name (str): JSONファイルの名前
        """
        self.file_name = file_name
        self.load_data = self.load_json(file_name)
    def load_json(self, file_name: str):
        """JSONファイルからデータを読み込む
        
        Args:
            file_name (str): JSONファイルの名前
        Returns:
            List[req_data]: 読み込んだデータのリスト
        """
        with open(self.file_name, 'r') as file:
            data = json.load(file)
        data_list = [req_data(**self.convert(item)) for item in data if isinstance(item, dict)]
        return data_list
    def convert(self, data_item):
        """辞書のキーを特定の形式に変換する
        辞書キーのハイフンをアンダースコアに置換する
        
        Args:
            data_item (dict): 辞書データ
        Returns:
            dict: 変換後の辞書データ
        例:
            {'key-name': 'value'} -> {'key_name': 'value'}
        """
        mydata = {key.replace("-", "_"): value for key, value in data_item.items()}
        return mydata

