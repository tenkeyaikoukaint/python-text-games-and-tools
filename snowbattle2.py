import random

class SnowBattle:
    def __init__(self, difficulty):
        self.turn = 1
        self.my_team = 50
        self.stock = 100  # 初期雪玉
        self.wall_hp = 100
        
        # 敵レベル設定
        enemy_settings = {1: 10, 2: 30, 3: 50}
        self.enemy_team = enemy_settings.get(difficulty, 30)
        self.initial_enemy = self.enemy_team

    def show_status(self):
        print(f"\n--- 第 {self.turn} ターン ---")
        print(f"自軍: {self.my_team}人 | 敵軍: {self.enemy_team}人")
        print(f"雪玉在庫: {self.stock}個 | 敵城壁耐久: {self.wall_hp}")
        print("-" * 20)

    def run_turn(self):
        self.show_status()
        print("【人員アサイン】残り 50 人を割り振ってください")
        
        try:
            make = int(input("玉つくり（玉増産）　: "))
            atk  = int(input("通常攻撃（1玉消費） : "))
            slng = int(input("スリング（5玉消費） : "))
            ram  = int(input("ラム　　（城壁破壊） : "))
            twr  = int(input("やぐら　（高命中）　 : "))
        except ValueError:
            print("数字を入力してください。ターンをスキップします。")
            return

        if (make + atk + slng + ram + twr) > self.my_team:
            print("人数オーバーです！全員サボりました。")
            return

        # 1. 雪玉製造
        new_balls = make * 3
        self.stock += new_balls
        print(f">> 雪玉を {new_balls} 個作成した。")

        # 2. 攻撃フェーズ
        total_damage = 0
        
        # 通常攻撃 (命中率低: 城壁の影響)
        hit_rate = 0.3 if self.wall_hp > 0 else 0.6
        for _ in range(min(atk, self.stock)):
            self.stock -= 1
            if random.random() < hit_rate: total_damage += 1
        
        # スリング (大玉・高命中)
        for _ in range(min(slng, self.stock // 5)):
            self.stock -= 5
            if random.random() < 0.7: total_damage += 3

        # やぐら (高命中・高被弾)
        for _ in range(min(twr, self.stock)):
            self.stock -= 1
            if random.random() < 0.8: total_damage += 2

        # ラム (城壁攻撃)
        wall_damage = 0
        if ram > 0:
            wall_damage = ram * random.randint(2, 5)
            self.wall_hp = max(0, self.wall_hp - wall_damage)
            print(f">> ラムが突撃！城壁に {wall_damage} のダメージ！")

        self.enemy_team = max(0, self.enemy_team - total_damage)
        print(f">> 敵に {total_damage} 人の被害を与えた！")

        # 3. 反撃フェーズ (ラムとやぐらは被弾率2倍)
        enemy_attack = self.enemy_team // 3
        my_loss = 0
        for _ in range(enemy_attack):
            target_bonus = 1.0
            if (ram + twr) > 0 and random.random() < 0.5:
                target_bonus = 2.0 # ラム、やぐら担当がいると被害増
            
            if random.random() < (0.2 * target_bonus):
                my_loss += 1
        
        self.my_team = max(0, self.my_team - my_loss)
        print(f">> 敵の反撃！自軍は {my_loss} 人脱落した...")

        self.turn += 1

    def is_end(self):
        if self.my_team <= 0:
            print("\n【敗北】自軍が全滅しました...")
            return True
        if self.enemy_team <= 0:
            print(f"\n【勝利！】{self.turn}ターンで敵を全滅させました！")
            return True
        return False

# ゲーム開始
print("=== アドバンスド雪合戦 ===")
level = int(input("敵レベルを選択 (1:初級, 2:中級, 3:上級): "))
game = SnowBattle(level)

while not game.is_end():
    game.run_turn()
