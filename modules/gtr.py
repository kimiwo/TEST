import ipaddress

def generate_cisco_commands(entry):
    """エントリからCiscoコマンドを生成する関数"""
    return list(map(
        lambda ip: (
            # vrfが"default"の場合の処理
            f"show ip route {ip}" if entry.vrf == "default" and ip_version(ip) == 4 else
            f"show ipv6 route {ip}" if entry.vrf == "default" and ip_version(ip) == 6 else
            # vrfが"default"以外の場合の処理
            f"show ip route vrf {entry.vrf} {ip}" if ip_version(ip) == 4 else
            f"show ipv6 route vrf {entry.vrf} {ip}",
            # BGPのルートを表示するコマンド
            f"show bgp vrf {entry.vrf} neighbor routes {ip}" if entry.vrf != "default" and ip_version(ip) == 4 else
            f"show bgp vrf {entry.vrf} neighbor ipv6 routes {ip}" if entry.vrf != "default" and ip_version(ip) == 6 else ""
        ),
        entry.prefix
    ))

def ip_version(ip):
    """IPアドレスのバージョンを取得する関数"""
    try:
        return ipaddress.ip_network(ip).version
    except ValueError:
        return None
