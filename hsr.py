"""
THE HOLY STONE: REFORGED
Enhanced version with Visuals, Skills, and Strategy.
"""

import random
import pickle
import os
import sys
import time

# --- 演出用設定 ---

class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    # WindowsとMac/Linux両対応の画面クリア
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_bar(val, max_val, length=15, color=Color.GREEN):
    """HP/MPバーを描画する関数"""
    if max_val <= 0: max_val = 1
    val = max(0, min(val, max_val))
    fill = int((val / max_val) * length)
    bar = "█" * fill + "░" * (length - fill)
    return f"{color}[{bar}] {val:>3}/{max_val:<3}{Color.ENDC}"

# --- ゲームデータ (辞書型にして管理しやすく変更) ---
ENEMIES = [
    {"name": " ", "hp": 0, "str": 0, "exp": 0, "gold": 0},
    {"name": "Wild Rat", "hp": 15, "str": 10, "exp": 5, "gold": 5},
    {"name": "Silver Wolf", "hp": 30, "str": 20, "exp": 15, "gold": 15},
    {"name": "Assassin", "hp": 60, "str": 35, "exp": 40, "gold": 40},
    {"name": "Dark Knight", "hp": 120, "str": 50, "exp": 100, "gold": 100},
    {"name": "Fire Lizard", "hp": 250, "str": 70, "exp": 250, "gold": 200},
    {"name": "Ghost Armor", "hp": 400, "str": 90, "exp": 500, "gold": 400},
    {"name": "Chaos Dragon", "hp": 1500, "str": 150, "exp": 5000, "gold": 5000}
]

WEAPONS = [
    {"name": "Fist", "pow": 0, "price": 0},
    {"name": "Dagger", "pow": 10, "price": 50},
    {"name": "Hand Axe", "pow": 25, "price": 200},
    {"name": "Mace", "pow": 40, "price": 600},
    {"name": "Short Sword", "pow": 60, "price": 1500},
    {"name": "Broad Sword", "pow": 90, "price": 4000},
    {"name": "Great Axe", "pow": 130, "price": 10000},
    {"name": "Holy Blade", "pow": 200, "price": 30000}
]

ARMORS = [
    {"name": "Cloth", "def": 0, "price": 0},
    {"name": "Leather", "def": 10, "price": 100},
    {"name": "Chain Mail", "def": 30, "price": 1000},
    {"name": "Plate Mail", "def": 60, "price": 5000},
    {"name": "Dragon Scale", "def": 100, "price": 20000}
]

LEVEL_EXP = [0, 50, 150, 400, 1000, 2500, 6000, 15000, 40000, 100000]

# --- クラス定義 ---

class GameVals:
    def __init__(self):
        self.player_name = "Hero"
        self.hp = 100
        self.max_hp = 100
        self.mp = 20        # MPを追加
        self.max_mp = 20
        self.strength = 20
        self.weapon_id = 1
        self.armor_id = 1
        self.gold = 100
        self.exp = 0
        self.level = 1
        self.potions = 2    # ポーション所持数
        self.mx = 2
        self.my = 2
        self.is_running = True
        self.game_state = None # 初期化時にセット

class GameState:
    def __init__(self, w, h, map_data):
        self.width = w
        self.height = h
        self.map_data = map_data

    def get_tile(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.map_data[y * self.width + x]
        return 0

    def draw_ui(self, game, message=""):
        clear_screen()
        print(f"{Color.HEADER}=== THE HOLY STONE: REFORGED ==={Color.ENDC}")
        # ステータス表示
        print(f"Name: {Color.BOLD}{game.player_name}{Color.ENDC} (Lv.{game.level})")
        print(f"HP: {draw_bar(game.hp, game.max_hp, 15, Color.GREEN)}  MP: {draw_bar(game.mp, game.max_mp, 10, Color.BLUE)}")
        print(f"Gold: {Color.WARNING}{game.gold}G{Color.ENDC} | Potions: {game.potions} | Exp: {game.exp}")
        print(f"Equip: {WEAPONS[game.weapon_id]['name']} / {ARMORS[game.armor_id]['name']}")
        print("-" * 50)
        
        # マップ表示
        print("[ Map View ]")
        view_range = 2
        for y in range(game.my - view_range, game.my + view_range + 1):
            line = "  "
            for x in range(game.mx - view_range, game.mx + view_range + 1):
                if x == game.mx and y == game.my:
                    line += f"{Color.CYAN}@{Color.ENDC} " # プレイヤー
                else:
                    tile = self.get_tile(x, y)
                    if tile == 0: line += f"{Color.FAIL}#{Color.ENDC} " # 壁
                    elif tile == 1: line += ". " # 道
                    elif tile == 2: line += f"{Color.WARNING}!{Color.ENDC} " # イベント
                    else: line += "  "
            print(line)
        
        if message:
            print(f"\n> {message}")
        print("-" * 50)

class Battle:
    def start(self, game, enemy_id):
        enemy = ENEMIES[enemy_id]
        e_hp = enemy['hp']
        e_max = enemy['hp']
        
        clear_screen()
        print(f"{Color.FAIL}{Color.BOLD}!!! ENCOUNTER !!!{Color.ENDC}")
        print(f"{enemy['name']} appeared!\n")
        time.sleep(1)
        
        while game.hp > 0 and e_hp > 0:
            # 戦闘画面描画
            clear_screen()
            print(f"{Color.FAIL}[Enemy] {enemy['name']}{Color.ENDC}")
            print(draw_bar(e_hp, e_max, 20, Color.FAIL))
            print("\n      VS\n")
            print(f"{Color.GREEN}[Hero] {game.player_name}{Color.ENDC}")
            print(f"HP: {draw_bar(game.hp, game.max_hp, 15, Color.GREEN)}")
            print(f"MP: {draw_bar(game.mp, game.max_mp, 15, Color.BLUE)}")
            print("-" * 40)
            print("1: Attack")
            print("2: Heavy Slash (5 MP) - High Damage")
            print("3: Heal (8 MP) - Recover HP")
            print(f"4: Potion (Own: {game.potions})")
            print("5: Escape")
            
            cmd = input("Command? > ")
            msg = ""
            player_dmg = 0
            
            # プレイヤーの行動
            if cmd == "1":
                base = game.strength + WEAPONS[game.weapon_id]['pow']
                player_dmg = max(1, base + random.randint(-5, 5))
                # クリティカル判定
                if random.randint(0, 100) < 15:
                    player_dmg = int(player_dmg * 1.5)
                    msg = f"{Color.WARNING}CRITICAL HIT!{Color.ENDC} "
                msg += f"You hit {enemy['name']} for {player_dmg} damage."
                e_hp -= player_dmg
                
            elif cmd == "2":
                if game.mp >= 5:
                    game.mp -= 5
                    base = (game.strength + WEAPONS[game.weapon_id]['pow']) * 2
                    player_dmg = int(base * random.uniform(0.8, 1.2))
                    msg = f"{Color.CYAN}HEAVY SLASH!{Color.ENDC} You dealt {player_dmg} damage!"
                    e_hp -= player_dmg
                else:
                    msg = "Not enough MP!"
                    
            elif cmd == "3":
                if game.mp >= 8:
                    game.mp -= 8
                    heal = int(game.max_hp * 0.5)
                    game.hp = min(game.max_hp, game.hp + heal)
                    msg = f"{Color.GREEN}Heal!{Color.ENDC} Recovered {heal} HP."
                else:
                    msg = "Not enough MP!"

            elif cmd == "4":
                if game.potions > 0:
                    game.potions -= 1
                    game.hp = min(game.max_hp, game.hp + 50)
                    msg = f"{Color.GREEN}Used Potion!{Color.ENDC} Recovered 50 HP."
                else:
                    msg = "No Potions!"
            
            elif cmd == "5":
                if random.randint(0, 100) < 50:
                    print("You escaped successfully!")
                    time.sleep(1)
                    return True # Escaped
                else:
                    msg = "Failed to escape!"
            else:
                msg = "Invalid command."

            print(f"\n> {msg}")
            
            if e_hp <= 0:
                break
                
            time.sleep(1)
            
            # 敵の行動
            enemy_atk = enemy['str']
            defense = ARMORS[game.armor_id]['def']
            dmg = max(1, enemy_atk - defense + random.randint(-3, 3))
            game.hp -= dmg
            print(f"> {Color.FAIL}{enemy['name']} attacks!{Color.ENDC} You took {dmg} damage.")
            time.sleep(1)

        # 戦闘終了判定
        if game.hp <= 0:
            print(f"\n{Color.FAIL}=== YOU DIED ==={Color.ENDC}")
            game.is_running = False
            return False
        else:
            print(f"\n{Color.WARNING}VICTORY!{Color.ENDC}")
            print(f"Gained {enemy['exp']} EXP and {enemy['gold']} Gold.")
            game.exp += enemy['exp']
            game.gold += enemy['gold']
            
            # レベルアップ
            if game.level < len(LEVEL_EXP) and game.exp >= LEVEL_EXP[game.level]:
                game.level += 1
                game.max_hp += 30
                game.max_mp += 10
                game.strength += 5
                game.hp = game.max_hp
                game.mp = game.max_mp
                print(f"{Color.CYAN}LEVEL UP! You are now Level {game.level}!{Color.ENDC}")
            
            # ボス撃破
            if enemy_id == 7:
                print(f"\n{Color.WARNING}You obtained the HOLY STONE!{Color.ENDC}")
                print("The world is saved.")
                input("Press Enter to end game...")
                game.is_running = False

            input("Press Enter to continue...")
            return True

class Maze(GameState):
    def __init__(self):
        # 0:壁, 1:床, 2:イベント
        data = [
            0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,2,1,1,1,1,1,1,1,0,0,
            0,0,1,0,0,0,0,0,1,0,0,0,
            0,0,1,1,1,1,1,0,1,2,0,0,
            0,0,1,0,0,0,1,0,0,0,0,0,
            0,0,1,0,1,1,1,0,2,1,0,0,
            0,0,1,0,0,0,0,0,0,1,0,0,
            0,0,1,0,1,0,1,1,1,1,0,0,
            0,0,1,1,1,1,1,0,0,1,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0
        ]
        super().__init__(12, 12, data)
        self.battle = Battle()

    def process_command(self, game, cmd):
        dx, dy = 0, 0
        if cmd == "n": dy = -1
        elif cmd == "s": dy = 1
        elif cmd == "e": dx = 1
        elif cmd == "w": dx = -1
        elif cmd == "g":
            with open("savedata.pkl", "wb") as f:
                pickle.dump(game, f)
            return "Game Saved."
        
        nx, ny = game.mx + dx, game.my + dy
        tile = self.get_tile(nx, ny)
        
        if tile > 0:
            game.mx, game.my = nx, ny
            # イベントチェック
            if tile == 2:
                if nx == 2 and ny == 2:
                    if input("Go to Town? (y/n): ") == "y":
                        game.game_state = Town()
                        game.mx, game.my = 9, 9
                        return "Moved to Town."
                elif nx == 8 and ny == 6:
                    print(f"{Color.FAIL}BOSS WARNING!{Color.ENDC}")
                    if input("Fight Dragon? (y/n): ") == "y":
                        self.battle.start(game, 7)
            # ランダムエンカウント
            elif random.random() < 0.2:
                # レベルに応じた敵が出現
                eid = min(len(ENEMIES)-2, random.randint(1, game.level + 2))
                self.battle.start(game, eid)
        else:
            return "You hit a wall."
        return ""

class Town(GameState):
    def __init__(self):
        data = [
            0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,1,1,1,1,1,1,2,0,0,
            0,0,0,1,0,0,0,0,0,0,0,0,
            0,0,0,1,0,2,1,1,0,2,0,0,
            0,0,0,1,0,0,0,1,0,1,0,0,
            0,0,0,1,1,1,1,1,1,1,0,0,
            0,0,0,0,0,0,0,1,0,1,0,0,
            0,0,0,2,1,1,1,1,0,2,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0
        ]
        super().__init__(12, 12, data)
    
    def process_command(self, game, cmd):
        dx, dy = 0, 0
        if cmd == "n": dy = -1
        elif cmd == "s": dy = 1
        elif cmd == "e": dx = 1
        elif cmd == "w": dx = -1
        elif cmd == "r":
            if game.gold >= 20:
                game.gold -= 20
                game.hp = game.max_hp
                game.mp = game.max_mp
                return f"{Color.GREEN}Rested at Inn. HP/MP recovered.{Color.ENDC}"
            else:
                return "Not enough gold (20G)."
        elif cmd == "g":
            with open("savedata.pkl", "wb") as f:
                pickle.dump(game, f)
            return "Game Saved."

        nx, ny = game.mx + dx, game.my + dy
        tile = self.get_tile(nx, ny)
        
        if tile > 0:
            game.mx, game.my = nx, ny
            
            # 施設の判定
            if nx == 5 and ny == 5: self.shop(game, "Weapon", WEAPONS, "weapon_id")
            elif nx == 3 and ny == 9: self.shop(game, "Armor", ARMORS, "armor_id")
            elif nx == 9 and ny == 5:
                # 道具屋（ポーション）
                print("Potion (50G). Buy? (y/n)")
                if input("> ") == "y":
                    if game.gold >= 50:
                        game.gold -= 50
                        game.potions += 1
                        print("Bought Potion.")
                        time.sleep(1)
            elif nx == 9 and ny == 9:
                if input("Enter Maze? (y/n): ") == "y":
                    game.game_state = Maze()
                    game.mx, game.my = 2, 2
                    return "Entered Maze."
        else:
            return "Wall."
        return ""

    def shop(self, game, name, item_list, attr):
        clear_screen()
        print(f"[{name} Shop] Gold: {game.gold}")
        for i, item in enumerate(item_list):
            if i == 0: continue
            print(f"{i}: {item['name']} - {item['price']}G")
        print("0: Exit")
        try:
            idx = int(input("Buy > "))
            if idx > 0 and idx < len(item_list):
                if game.gold >= item_list[idx]['price']:
                    game.gold -= item_list[idx]['price']
                    setattr(game, attr, idx)
                    print("Bought and Equipped!")
                    time.sleep(1)
                else:
                    print("Not enough gold.")
                    time.sleep(1)
        except ValueError:
            pass

def main():
    game = GameVals()
    game.game_state = Maze()
    
    clear_screen()
    print(f"{Color.CYAN}THE HOLY STONE: REFORGED{Color.ENDC}")
    print("1. New Game")
    print("2. Load Game")
    if input("> ") == "2":
        try:
            with open("savedata.pkl", "rb") as f:
                game = pickle.load(f)
            print("Loaded!")
        except:
            print("No save found. Starting new.")
            time.sleep(1)
    
    while game.is_game_run:
        game.game_state.draw_ui(game)
        if isinstance(game.game_state, Maze):
            print("Move(n/s/e/w) | Save(g)")
        else:
            print("Move(n/s/e/w) | Rest(r) | Save(g)")
            
        cmd = input("> ").lower().strip()
        msg = game.game_state.process_command(game, cmd)
        if msg:
            print(msg)
            time.sleep(1)

if __name__ == '__main__':
    main()