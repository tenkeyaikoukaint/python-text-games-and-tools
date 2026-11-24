import csv
import os
import re
import sys
import unicodedata

# WindowsでANSIエスケープシーケンスを有効化
if os.name == "nt":
    os.system("")
    import msvcrt
else:
    import termios
    import tty

# --- 設定 ---
ROWS = 15
COLS = 8
CELL_WIDTH = 12


def get_key():
    """cursesを使わずに1キー（矢印キー含む）を取得"""
    if os.name == "nt":
        ch = msvcrt.getch()
        if ch in (b"\x00", b"\xe0"):
            ch2 = msvcrt.getch()
            return {b"H": "UP", b"P": "DOWN", b"K": "LEFT", b"M": "RIGHT"}.get(ch2, "")
        if ch == b"\r":
            return "ENTER"
        if ch == b"\x03":
            return "QUIT"
        if ch == b"\x08":
            return "BACKSPACE"
        try:
            return ch.decode("utf-8")
        except UnicodeDecodeError:
            return ""
    else:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                return {"[A": "UP", "[B": "DOWN", "[D": "LEFT", "[C": "RIGHT"}.get(seq, "ESC")
            if ch in ("\r", "\n"):
                return "ENTER"
            if ch == "\x03":
                return "QUIT"
            if ch == "\x7f":
                return "BACKSPACE"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def char_width(c):
    return 2 if unicodedata.east_asian_width(c) in "FWA" else 1


def pad_text(text, width, align="left"):
    """全角文字を考慮して指定幅に切り詰め・パディング"""
    text = str(text)
    out = []
    w = 0
    for c in text:
        cw = char_width(c)
        if w + cw > width:
            break
        out.append(c)
        w += cw
    s = "".join(out)
    pad = " " * (width - w)
    if align == "right":
        return pad + s
    if align == "center":
        left = (width - w) // 2
        return " " * left + s + " " * (width - w - left)
    return s + pad


def col_name(idx):
    return chr(ord("A") + idx)


def parse_ref(ref):
    """'A1' -> (row, col)"""
    m = re.fullmatch(r"([A-Z])(\d+)", ref.upper())
    if not m:
        return None
    c = ord(m.group(1)) - ord("A")
    r = int(m.group(2)) - 1
    if 0 <= r < ROWS and 0 <= c < COLS:
        return (r, c)
    return None


class MiniExcel:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.grid = [["" for _ in range(cols)] for _ in range(rows)]
        self.r = 0
        self.c = 0
        self.message = "矢印/hjkl:移動  Enter:編集  x:削除  s:CSV保存  l:CSV読込  q:終了"

    def eval_cell(self, r, c, visited=None):
        """数式を評価して表示用の値を返す"""
        raw = self.grid[r][c].strip()
        if not raw.startswith("="):
            return raw

        if visited is None:
            visited = set()
        if (r, c) in visited:
            return "#REF!"
        visited.add((r, c))

        expr = raw[1:].strip().upper()

        def get_num(rr, cc):
            val = self.eval_cell(rr, cc, visited.copy())
            try:
                return float(val)
            except (ValueError, TypeError):
                return 0.0

        def range_values(start_ref, end_ref):
            p1, p2 = parse_ref(start_ref), parse_ref(end_ref)
            if not p1 or not p2:
                raise ValueError("Invalid range")
            r1, c1 = min(p1[0], p2[0]), min(p1[1], p2[1])
            r2, c2 = max(p1[0], p2[0]), max(p1[1], p2[1])
            vals = []
            for rr in range(r1, r2 + 1):
                for cc in range(c1, c2 + 1):
                    vals.append(get_num(rr, cc))
            return vals

        try:
            # SUM(A1:B2), AVG(A1:B2), AVERAGE(A1:B2) の展開
            def replace_func(match):
                func, ref1, ref2 = match.group(1), match.group(2), match.group(3)
                vals = range_values(ref1, ref2)
                if func == "SUM":
                    return str(sum(vals))
                if func in ("AVG", "AVERAGE"):
                    return str(sum(vals) / len(vals) if vals else 0)
                return "0"

            expr = re.sub(
                r"\b(SUM|AVG|AVERAGE)\(([A-Z]\d+):([A-Z]\d+)\)",
                replace_func,
                expr,
            )

            # 単一セル参照 (A1 など) の展開
            def replace_cell(match):
                pos = parse_ref(match.group(0))
                if not pos:
                    raise ValueError("Invalid ref")
                return str(get_num(pos[0], pos[1]))

            expr = re.sub(r"\b[A-Z]\d+\b", replace_cell, expr)

            # 安全な文字のみ許可して評価
            if not re.fullmatch(r"[\d\.\+\-\*/\(\)\s]+", expr):
                return "#ERR!"

            res = eval(expr, {"__builtins__": None}, {})
            if isinstance(res, float) and res.is_integer():
                return str(int(res))
            return f"{res:.2f}" if isinstance(res, float) else str(res)
        except ZeroDivisionError:
            return "#DIV/0!"
        except Exception:
            return "#ERR!"

    def render(self):
        # 画面クリア & カーソルを左上へ
        buf = ["\x1b[2J\x1b[H"]

        # ヘッダー（選択中のセルと生データ）
        cell_id = f"{col_name(self.c)}{self.r + 1}"
        raw_val = self.grid[self.r][self.c]
        buf.append(f"\x1b[1;36m[PyExcel CLI]\x1b[0m  セル: \x1b[1;33m{cell_id}\x1b[0m  数式/値: {raw_val}\n")

        # 列見出し (A, B, C...)
        header = "    |" + "|".join(
            f"\x1b[1;37;44m{pad_text(col_name(c), CELL_WIDTH, 'center')}\x1b[0m"
            if c == self.c
            else f"\x1b[1m{pad_text(col_name(c), CELL_WIDTH, 'center')}\x1b[0m"
            for c in range(self.cols)
        ) + "|"
        sep = "----+" + "+".join("-" * CELL_WIDTH for _ in range(self.cols)) + "+"

        buf.append(sep + "\n")
        buf.append(header + "\n")
        buf.append(sep + "\n")

        # 各行の描画
        for r in range(self.rows):
            row_label = f"{r + 1:>3} "
            if r == self.r:
                row_label = f"\x1b[1;37;44m{row_label}\x1b[0m"
            line = [row_label + "|"]

            for c in range(self.cols):
                val = self.eval_cell(r, c)
                # 数値は右寄せ、文字は左寄せ
                try:
                    float(val)
                    align = "right"
                except ValueError:
                    align = "left"

                cell_str = pad_text(val, CELL_WIDTH, align)
                if r == self.r and c == self.c:
                    # 選択セルをハイライト（反転表示）
                    line.append(f"\x1b[7;1m{cell_str}\x1b[0m|")
                elif val.startswith("#"):
                    line.append(f"\x1b[31m{cell_str}\x1b[0m|")
                else:
                    line.append(f"{cell_str}|")
            buf.append("".join(line) + "\n")

        buf.append(sep + "\n")
        buf.append(f"\x1b[90m{self.message}\x1b[0m\n")

        sys.stdout.write("".join(buf))
        sys.stdout.flush()

    def edit_current(self):
        cell_id = f"{col_name(self.c)}{self.r + 1}"
        current = self.grid[self.r][self.c]
        try:
            new_val = input(f"{cell_id} を編集 (現在: '{current}' / 空Enterでキャンセル): ")
            if new_val != "":
                self.grid[self.r][self.c] = new_val
                self.message = f"{cell_id} を更新しました"
            else:
                self.message = "編集をキャンセルしました"
        except (KeyboardInterrupt, EOFError):
            self.message = "編集をキャンセルしました"

    def save_csv(self):
        filename = input("保存するファイル名 (デフォルト: sheet.csv): ").strip() or "sheet.csv"
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerows(self.grid)
            self.message = f"'{filename}' に保存しました"
        except Exception as e:
            self.message = f"保存エラー: {e}"

    def load_csv(self):
        filename = input("読み込むファイル名 (デフォルト: sheet.csv): ").strip() or "sheet.csv"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                rows = list(csv.reader(f))
            self.grid = [["" for _ in range(self.cols)] for _ in range(self.rows)]
            for r in range(min(len(rows), self.rows)):
                for c in range(min(len(rows[r]), self.cols)):
                    self.grid[r][c] = rows[r][c]
            self.message = f"'{filename}' を読み込みました"
        except Exception as e:
            self.message = f"読込エラー: {e}"

    def run(self):
        # サンプルデータを入れておく
        self.grid[0][0], self.grid[0][1], self.grid[0][2] = "品目", "単価", "個数"
        self.grid[0][3] = "小計"
        self.grid[1][0], self.grid[1][1], self.grid[1][2] = "りんご", "150", "3"
        self.grid[1][3] = "=B2*C2"
        self.grid[2][0], self.grid[2][1], self.grid[2][2] = "みかん", "80", "5"
        self.grid[2][3] = "=B3*C3"
        self.grid[3][0], self.grid[3][3] = "合計", "=SUM(D2:D3)"

        while True:
            self.render()
            key = get_key()

            if key in ("q", "QUIT"):
                sys.stdout.write("\x1b[2J\x1b[H")
                break
            elif key in ("UP", "k"):
                self.r = max(0, self.r - 1)
            elif key in ("DOWN", "j"):
                self.r = min(self.rows - 1, self.r + 1)
            elif key in ("LEFT", "h"):
                self.c = max(0, self.c - 1)
            elif key in ("RIGHT", "l"):
                self.c = min(self.cols - 1, self.c + 1)
            elif key == "ENTER":
                self.edit_current()
            elif key in ("x", "BACKSPACE"):
                self.grid[self.r][self.c] = ""
                self.message = f"{col_name(self.c)}{self.r + 1} をクリアしました"
            elif key == "s":
                self.save_csv()
            elif key == "o":
                self.load_csv()


if __name__ == "__main__":
    MiniExcel().run()