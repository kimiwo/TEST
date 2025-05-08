from modules.data import request_list, DataLoader
import os


def main():
    # スクリプトのバージョン
    script_ver = "0.0.1"
    # リクエストJSONファイルのパス
    file_name = os.path.join(os.path.dirname(__file__), "req.json")
    # リクエストJSONファイルのデータを読み込む
    request_json = DataLoader(file_name)
    # 読み込んだJSONをデータクラスに格納
    data_list = request_list(request_json.load_data)
    print(data_list)

    all_list   = [data_list_check(item) for item in data_list.all_data]
    #final_list   = list(filter(lambda x: x is not None, final_list))

    print(len(all_list))

def data_list_check(data):
    print(f"VRF:       {data.vrf}")
    print(f"Date:      {data.date}")
    print(f"Account:   {data.account}")
    print(f"Prefix:    {data.prefix}")
    print(f"DXGW ID:   {data.dxgw_id}")
    print(f"DXGW Name: {data.dxgw_name}")
    print(f"VGW ID:    {data.vgw_id}")
    print("-" * 40)
    return data.vgw_id


if __name__ == "__main__":
    main()
