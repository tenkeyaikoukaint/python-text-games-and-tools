import random
import time
import sys

class AdvancedSnowballFight:
    def __init__(self):
        # 自軍設定
        self.max_troops = 50
        self.troops = self.max_troops
        self.snowballs = 20  # 初期の雪玉数
        
        # ゲーム進行設定
        self.stage = 1
        self.max_stage = 3
        
        # 敵データ [人数, 城壁HP, 名前]
        self.stages = {
            1: {"enemy": 10, "wall": 50,  "name": "近所の悪ガキ団"},
            2: {"enemy": 30, "wall": 150, "name": "隣町のスポーツ少年団"},
            3: {"enemy": 50, "wall": 300, "name": "帝国の精鋭雪合戦部隊"}
        }

        # 役割データ
        # cost:消費雪玉, acc:命中率(対人), aggro:ヘイト(被弾倍率)
        self.roles_config = {
            "maker":  {"name": "玉つくり", "cost": 0, "acc": 0.0, "aggro": 1.0, "desc": "雪玉+3 (安全)"},
            "normal": {"name": "通常攻撃", "cost": 1, "acc": 0.4, "aggro": 1.0, "desc": "雪玉1 (基本)"},
            "sling":  {"name": "スリング", "cost": 3, "acc": 0.9, "aggro": 1.5, "desc": "雪玉3 (高命中)"},
            "ram":    {"name": "ラム　　", "cost": 0, "acc": 0.0, "aggro": 8.0, "desc": "対城壁 (超危険)"},
            "tower":  {"name": "やぐら　", "cost": 2, "acc": 0.8, "aggro": 4.0, "desc": "雪玉2 (壁無視/危険)"},
        }

    def print_slow(self, text, delay=0.01):
        """雰囲気を出すための演出出力"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def get_input(self, role_key, remaining):
        """人数割り当ての入力処理"""
        config = self.roles_config[role_key]
        while True:
            try:
                prompt = f"  {config['name']} [{config['desc']}] (残{remaining}人) > "
                user_input = input(prompt)
                if user_input == "": # Enterのみなら0
                    return 0
                val = int(user_input)
                if 0 <= val <= remaining:
                    return val
                print(f"  ! 0〜{remaining}の間で入力してください")
            except ValueError:
                print("  ! 数字を入力してください")

    def battle_phase(self, enemy_max, enemy_curr, wall_curr):
        turn = 1
        
        while enemy_curr > 0 and self.troops > 0:
            print("\n" + "-"*60)
            print(f"【 ターン {turn} 】")
            
            # --- バランス調整: 壁がある間はお互い命中率ダウン ---
            # これがないと敵50人のステージ3で即死するため
            wall_status = "崩壊" if wall_curr <= 0 else f"耐久{wall_curr}"
            
            base_acc = 0.3 # 敵の基本命中率
            if wall_curr > 0:
                enemy_acc_curr = 0.15 # 壁がある間は敵も当てにくい(視界不良)
                wall_msg = " (双方視界不良 / 命中ダウン)"
            else:
                enemy_acc_curr = base_acc
                wall_msg = " (総力戦！)"

            print(f" 自軍: {self.troops}人 | ❄️ 雪玉: {self.snowballs}個")
            print(f" 敵軍: {enemy_curr}/{enemy_max}人 | 🧱 城壁: {wall_status}{wall_msg}")
            print("-" * 60)

            # --- 1. アサイン入力 ---
            alloc = {}
            remaining = self.troops
            
            # 入力処理（変更なし）
            input_order = ["maker", "ram", "sling", "tower"]
            for r in input_order:
                if remaining > 0:
                    count = self.get_input(r, remaining)
                    alloc[r] = count
                    remaining -= count
                else:
                    alloc[r] = 0
            alloc["normal"] = remaining
            if remaining > 0:
                print(f"  通常攻撃 [雪玉1 (基本)] に残り {remaining} 人を配置しました。")
            
            print("\n>>> 作戦実行 >>>")
            time.sleep(0.5)

            # --- 2. 自軍アクション ---
            
            # 先に雪玉製造
            made = alloc["maker"] * 3
            self.snowballs += made
            if alloc["maker"] > 0:
                print(f"📦 玉つくり部隊が雪玉を {made} 個製造 (在庫: {self.snowballs})")

            # 【修正点A】ラム（壁破壊）を先に実行する
            # これにより、同じターン内に壁が壊れれば、即座に射撃部隊の命中率が上がる
            ram_dmg = 0
            if alloc["ram"] > 0:
                for _ in range(alloc["ram"]):
                    if random.random() < 0.6: ram_dmg += 15
                
                if ram_dmg > 0:
                    wall_curr = max(0, wall_curr - ram_dmg)
                    print(f"🐏 ラム部隊が城壁を破壊！ {ram_dmg} ダメージを与えた！")
                    if wall_curr == 0:
                        print("💥 敵の城壁が完全に崩壊した！ 敵は丸裸だ！")

            # 攻撃処理
            wall_factor = 0.2 if wall_curr > 0 else 1.0
            total_hits = 0
            
            # 射撃部隊の処理
            shooters = ["tower", "sling", "normal"]
            for role in shooters:
                count = alloc[role]
                if count == 0: continue
                
                conf = self.roles_config[role]
                cost = conf["cost"]
                needed = count * cost
                
                # 雪玉不足チェック
                actual_shooters = count
                if self.snowballs < needed:
                    actual_shooters = self.snowballs // cost if cost > 0 else 0
                    self.snowballs = 0
                    print(f"⚠️ {conf['name']}部隊: 雪玉不足で {count - actual_shooters} 人が攻撃不能！")
                else:
                    self.snowballs -= needed
                
                # 命中判定
                hit_prob = conf["acc"]
                if role == "tower":
                    # やぐらは壁の影響を軽減
                    hit_prob *= (wall_factor + (1.0 - wall_factor) * 0.6)
                else:
                    hit_prob *= wall_factor

                role_hits = 0
                for _ in range(actual_shooters):
                    if random.random() < hit_prob:
                        role_hits += 1
                
                if role_hits > 0:
                    print(f"⚔️ {conf['name']}部隊: {role_hits} 人の敵に命中！")
                    total_hits += role_hits

            enemy_curr = max(0, enemy_curr - total_hits)
            if enemy_curr == 0:
                return True, self.troops

            # --- 3. 敵の反撃（バグ修正版） ---
            print("\n🔻 敵の反撃 🔻")
            time.sleep(0.5)
            
            enemy_hits = 0
            for _ in range(enemy_curr):
                if random.random() < enemy_acc_curr:
                    enemy_hits += 1
            
            if enemy_hits > 0:
                print(f"敵の雪玉が {enemy_hits} 発飛んできた！")
                
                dead_log = {r: 0 for r in self.roles_config}
                
                # 【修正点B】1発ごとに生存者を確認してターゲットを再計算
                # これにより「死体ガード」を防ぐ
                for _ in range(enemy_hits):
                    if self.troops <= 0: break
                    
                    # 生存しているロールのみを候補にする
                    candidates = []
                    weights = []
                    for r, count in alloc.items():
                        if count > 0:
                            candidates.append(r)
                            # 重み = 人数 * ヘイト
                            weights.append(count * self.roles_config[r]["aggro"])

                    if not candidates: break

                    hit_role = random.choices(candidates, weights=weights, k=1)[0]
                    
                    alloc[hit_role] -= 1
                    dead_log[hit_role] += 1
                    self.troops -= 1
                
                for r, count in dead_log.items():
                    if count > 0:
                        msg = f"💀 {self.roles_config[r]['name']}が {count} 名脱落..."
                        if self.roles_config[r]['aggro'] > 2.0:
                            msg += " (集中砲火)"
                        print(msg)
            else:
                print("敵の攻撃はすべて外れた！")

            turn += 1

        return False, self.troops

    def run(self):
        self.print_slow("\n❄️ 戦略シミュレーション：アドバンスド雪合戦 ❄️")
        print("敵の城壁を崩し、部隊を指揮して雪原を制圧せよ！")
        time.sleep(1)

        while self.stage <= self.max_stage:
            data = self.stages[self.stage]
            
            print("\n" + "="*50)
            print(f" STAGE {self.stage}: VS {data['name']}")
            print("="*50)
            time.sleep(1)
            
            win, survivors = self.battle_phase(data["enemy"], data["enemy"], data["wall"])
            
            if not win:
                print("\n" + "="*50)
                print(" 💀 DEFEAT... 部隊は全滅しました...")
                print("="*50)
                break
            else:
                print("\n" + "="*50)
                print(f" 🎉 STAGE {self.stage} CLEAR! ({data['name']}を撃破)")
                
                if self.stage < self.max_stage:
                    # 救済措置：部隊の回復
                    recover = 10
                    self.troops = min(self.max_troops, self.troops + recover)
                    print(f" 🚑 救護班が到着し、{recover}名が戦線復帰しました。")
                    self.print_slow(" 次の戦いに備えてください...")
                    time.sleep(2)
                self.stage += 1

        if self.troops > 0:
            print("\n" + "*"*50)
            print(" 🏆 CONGRATULATIONS! 全ての敵を倒し、完全勝利しました！")
            print("*"*50)

if __name__ == "__main__":
    game = AdvancedSnowballFight()
    game.run()
inp = input("Hit ENTER key to exit : ")