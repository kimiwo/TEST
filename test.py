from modules.aws import get_aws_entries
from modules.gtr import generate_cisco_commands
import os

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