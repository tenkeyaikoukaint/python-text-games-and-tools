import random
import os
import time

def clear_screen():
    """画面をクリアする関数"""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board():
    """4x4のボードを作成し、カード（数字ペア）をシャッフルして配置する"""
    cards = list(range(1, 9)) * 2  # 1-8の数字を2セット
    random.shuffle(cards)
    
    board = []
    for i in range(4):
        board.append(cards[i*4 : (i+1)*4])
    return board

def print_board(board, revealed, attempts):
    """現在のボードの状態を表示する"""
    clear_screen()
    print(f"--- テキスト神経衰弱 (試行回数: {attempts}) ---")
    print("    1 2 3 4  (列)")
    print("  +---------")
    
    for r in range(4):
        line = f"{r+1} | "
        for c in range(4):
            if revealed[r][c]:
                line += f"{board[r][c]} "
            else:
                line += "* "  # 隠れているカード
        print(line)
    print("\n座標は '行 列' の形式で入力してください (例: 1 2)")

def get_valid_input(revealed):
    """有効な座標入力を受け取る"""
    while True:
        try:
            inp = input("カードを選択 >> ").split()
            if len(inp) != 2:
                print("エラー: 行と列をスペース区切りで入力してください。")
                continue
            
            row, col = int(inp[0]) - 1, int(inp[1]) - 1
            
            if 0 <= row < 4 and 0 <= col < 4:
                if revealed[row][col]:
                    print("そのカードは既にめくられています。")
                else:
                    return row, col
            else:
                print("エラー: 1から4の範囲で入力してください。")
                
        except ValueError:
            print("エラー: 数字を入力してください。")

def main():
    board = create_board()
    revealed = [[False] * 4 for _ in range(4)] # カードの裏表状態 (False=裏)
    matches_found = 0
    attempts = 0
    total_pairs = 8

    while matches_found < total_pairs:
        print_board(board, revealed, attempts)
        
        # --- 1枚目の選択 ---
        print("【1枚目】")
        r1, c1 = get_valid_input(revealed)
        revealed[r1][c1] = True
        print_board(board, revealed, attempts)
        
        # --- 2枚目の選択 ---
        print("【2枚目】")
        while True:
            r2, c2 = get_valid_input(revealed)
            if (r1, c1) == (r2, c2):
                print("エラー: 1枚目と同じ場所は選べません。")
            else:
                break
        
        revealed[r2][c2] = True
        print_board(board, revealed, attempts)
        
        # --- 判定 ---
        attempts += 1
        if board[r1][c1] == board[r2][c2]:
            print("★ 当たり！ ★")
            matches_found += 1
            time.sleep(1.5) # 結果を少し表示
        else:
            print("× ハズレ... ×")
            time.sleep(2)   # 記憶する時間を設ける
            # カードを裏に戻す
            revealed[r1][c1] = False
            revealed[r2][c2] = False

    # ゲームクリア
    clear_screen()
    print("==============================")
    print(f"   GAME CLEARED! おめでとう！")
    print(f"   総試行回数: {attempts} 回")
    print("==============================")

if __name__ == "__main__":
    main()