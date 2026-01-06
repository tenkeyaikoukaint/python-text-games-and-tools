import sys

class LineEditor:
    def __init__(self):
        self.buffer = []  # document -> buffer (エディタらしい名称に変更)
        self.is_line_number_visible = True

    def _get_input(self, prompt):
        try:
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D や Ctrl+C で安全に終了できるようにする
            print()
            return "q"

    def _parse_range(self, args):
        """引数から対象行の範囲（start, end）を計算して返すヘルパー関数"""
        total_lines = len(self.buffer)
        start, end = 0, total_lines  # デフォルトは全行

        try:
            if len(args) == 1:
                # 指定なし: 全行
                pass
            elif len(args) == 2:
                # 1行指定: d 5 -> 5行目のみ
                idx = int(args[1])
                start = idx - 1
                end = idx
            elif len(args) >= 3:
                # 範囲指定: d 1 5 -> 1行目から5行目
                start = int(args[1]) - 1
                end = int(args[2])
            
            # 範囲チェック
            if start < 0 or end > total_lines or start >= end:
                if len(args) > 1: # 引数があったのに範囲外の場合のみエラー
                    print("Error: Index Out of Range")
                    return None, None
                
            return start, end
        except ValueError:
            print("Error: Illegal Parameter")
            return None, None

    def cmd_edit(self, start_index=None):
        """挿入・編集モード"""
        # start_indexが指定されていなければ末尾に追加
        current_index = start_index if start_index is not None else len(self.buffer)
        
        print("(Enter '.' to return to command mode)")
        while True:
            prompt = f"{current_index + 1}: "
            line = self._get_input(prompt)
            
            if line == ".":
                break
            
            self.buffer.insert(current_index, line)
            current_index += 1

    def cmd_list(self, args):
        """表示コマンド (l)"""
        start, end = self._parse_range(args)
        if start is None: return

        for i in range(start, end):
            if self.is_line_number_visible:
                print(f"{i + 1}:{self.buffer[i]}")
            else:
                print(self.buffer[i])

    def cmd_delete(self, args):
        """削除コマンド (d)"""
        if len(args) < 2:
            print("Error: Line number required for delete")
            return

        start, end = self._parse_range(args)
        if start is None: return

        # スライス削除（安全かつ高速）
        del self.buffer[start:end]
        print(f"Deleted lines {start + 1} to {end}")

    def cmd_insert(self, args):
        """挿入コマンド (i)"""
        start_index = len(self.buffer) # デフォルトは末尾
        if len(args) >= 2 and args[1].isnumeric():
            start_index = int(args[1]) - 1
            if start_index < 0 or start_index > len(self.buffer):
                print("Error: Index Out of Range")
                return
        
        self.cmd_edit(start_index)

    def cmd_read(self, args):
        """ファイル読み込み (r)"""
        if len(args) < 2:
            print("Error: Filename required")
            return
        
        filename = args[1]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.buffer = [line.rstrip('\n') for line in f.readlines()]
            print(f"Read {len(self.buffer)} lines from {filename}")
        except FileNotFoundError:
            print("Error: File not found")
        except Exception as e:
            print(f"Error: {e}")

    def cmd_write(self, args):
        """ファイル書き込み (w)"""
        if len(args) < 2:
            print("Error: Filename required")
            return

        filename = args[1]
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for line in self.buffer:
                    f.write(f"{line}\n")
            print(f"Saved to {filename}")
        except Exception as e:
            print(f"Error: {e}")

    def cmd_toggle_number(self):
        """行番号表示切替 (n)"""
        self.is_line_number_visible = not self.is_line_number_visible
        state = "ON" if self.is_line_number_visible else "OFF"
        print(f"Line numbers: {state}")

    def show_help(self):
        print("--- Commands ---")
        print("i [line]      : Insert lines (default: end)")
        print("l [start] [end]: List lines")
        print("d [start] [end]: Delete lines")
        print("r [file]      : Read file")
        print("w [file]      : Write file")
        print("n             : Toggle line numbers")
        print("q             : Quit")

    def run(self):
        """メインループ"""
        print("Simple Line Editor (Type '?' for help)")
        while True:
            user_input = self._get_input("> ")
            # カンマをスペースに置換して分割
            parts = user_input.replace(",", " ").split()
            
            if not parts:
                continue

            cmd = parts[0].lower()

            if cmd == "q":
                print("Bye.")
                sys.exit()
            elif cmd == "i":
                self.cmd_insert(parts)
            elif cmd == "l":
                self.cmd_list(parts)
            elif cmd == "d":
                self.cmd_delete(parts)
            elif cmd == "r":
                self.cmd_read(parts)
            elif cmd == "w":
                self.cmd_write(parts)
            elif cmd == "n":
                self.cmd_toggle_number()
            elif cmd in ["?", "h", "help"]:
                self.show_help()
            else:
                print(f"Unknown command: {cmd}")

if __name__ == '__main__':
    editor = LineEditor()
    editor.run()
