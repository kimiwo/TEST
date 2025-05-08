import json
from dataclasses import dataclass
from typing import List

@dataclass
class request_entry:
    cloud: str
    vrf: str
    dxgw_id: str
    dxgw_name: str
    account: str
    vgw_id: str
    prefix: List[str]
    date: str

def load_json(file_path: str) -> List[request_entry]:
    """JSONファイルを読み込み、request_entryのリストを返す"""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [request_entry(
            cloud=item["cloud"],
            vrf=item["vrf"],
            dxgw_id=item["dxgw-id"],
            dxgw_name=item["dxgw-name"],
            account=item["account"],
            vgw_id=item["vgw-id"],
            prefix=item["prefix"],
            date=item["date"]
        ) for item in data]

def filter_aws_entries(entries: List[request_entry]) -> List[request_entry]:
    """cloudが'aws'のエントリのみをフィルタリング"""
    return [entry for entry in entries if entry.cloud == 'aws']

def get_aws_entries(file_path: str) -> List[request_entry]:
    """指定されたファイルからcloudが'aws'のエントリを取得"""
    entries = load_json(file_path)
    return filter_aws_entries(entries)
