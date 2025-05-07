from modules.aws import get_aws_entries
import os
import ipaddress

def generate_cisco_commands(entry):
    """エントリからCiscoコマンドを生成する関数"""
    return list(map(
        lambda ip: (
            # vrfが"default"の場合の処理
            f"show ip route {ip}" if entry.vrf == "default" and ipaddress.ip_network(ip).version == 4 else
            f"show ipv6 route {ip}" if entry.vrf == "default" and ipaddress.ip_network(ip).version == 6 else
            # vrfが"default"以外の場合の処理
            f"show ip route vrf {entry.vrf} {ip}" if ipaddress.ip_network(ip).version == 4 else
            f"show ipv6 route vrf {entry.vrf} {ip}",
            # BGPのルートを表示するコマンド
            f"show bgp vrf {entry.vrf} neighbor routes {ip}" if entry.vrf != "default" and ipaddress.ip_network(ip).version == 4 else
            f"show bgp vrf {entry.vrf} neighbor ipv6 routes {ip}" if entry.vrf != "default" and ipaddress.ip_network(ip).version == 6 else ""
        ),
        entry.prefix
    ))

def process_entry(entry):
    """エントリを処理する関数"""
    commands = generate_cisco_commands(entry)
    list(map(lambda cmd_pair: print(f"{cmd_pair[0]}\n{cmd_pair[1]}" if cmd_pair[1] else f"{cmd_pair[0]}"), commands))
    print("-" * 20)  # 区切り線を表示

def main():
    file_name = "req.json"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    aws_entries = get_aws_entries(file_path)

    # 各エントリを関数型プログラミングで処理
    list(map(process_entry, aws_entries))

if __name__ == "__main__":
    main()
