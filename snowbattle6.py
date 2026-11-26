import random
import time
import sys

class AdvancedSnowballFight:
    def __init__(self):
        # 自軍設定
        self.max_troops = 50
        self.troops = self.max_troops
        self.snowballs = 25  # 初期の雪玉数
        
        # ゲーム進行設定
        self.stage = 1
        self.max_stage = 3
        
        # 敵データ
        self.stages = {
            1: {"enemy": 12, "wall": 60,  "name": "近所の悪ガキ団"},
            2: {"enemy": 30, "wall": 150, "name": "隣町のスポーツ少年団"},
            3: {"enemy": 50, "wall": 280, "name": "帝国の精鋭雪合戦部隊"}
        }

        # 役割データ
        # cost:消費雪玉, acc:命中率(対人), aggro:ヘイト(被弾倍率), max:1ターンの配置上限
        self.roles_config = {
            "maker":  {"name": "玉つくり", "cost": 0, "acc": 0.0,  "aggro": 1.0,  "max": None, "desc": "雪玉+3 (吹雪で+5)"},
            "shield": {"name": "盾役  ", "cost": 0, "acc": 0.0,  "aggro": 12.0, "max": 15,   "desc": "味方を庇う / 60%で被弾無効"},
            "ram":    {"name": "ラム  ", "cost": 0, "acc": 0.0,  "aggro": 6.0,  "max": 8,    "desc": "対城壁特化 (破壊時、敵を怯ませる)"},
            "tower":  {"name": "やぐら ", "cost": 2, "acc": 0.75, "aggro": 4.0,  "max": 10,   "desc": "雪玉2 / 壁無視＆敵の特殊行動を妨害"},
            "sling":  {"name": "スリング", "cost": 3, "acc": 0.90, "aggro": 1.5,  "max": None, "desc": "雪玉3 / 高命中＆30%で2人抜き"},
            "normal": {"name": "通常攻撃", "cost": 1, "acc": 0.40, "aggro": 1.0,  "max": None, "desc": "雪玉1 / 弾幕で敵の命中率ダウン"},
        }

        # 天候データ
        self.weathers = [
            {"name": "晴れ",     "desc": "通常コンディション", "acc_mod": 1.0, "make_bonus": 0, "dmg_bonus": 0},
            {"name": "吹雪",     "desc": "双方の命中率0.7倍 / 玉つくり+2個", "acc_mod": 0.7, "make_bonus": 2, "dmg_bonus": 0},
            {"name": "湿った雪", "desc": "雪玉が重い！ラム威力+5 / 双方の命中率1.1倍", "acc_mod": 1.1, "make_bonus": 0, "dmg_bonus": 5},
        ]

    def print_slow(self, text, delay=0.015):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def get_enemy_intent(self, wall_curr, wall_max):
        """敵の次の行動（予兆）を決定"""
        choices = ["normal", "barrage", "supply"]
        weights = [45, 30, 25]
        # 壁が削れていて、まだ残っている場合は修復の選択肢を追加
        if 0 < wall_curr < wall_max:
            choices.append("repair")
            weights.append(30)
        
        intent = random.choices(choices, weights=weights, k=1)[0]
        intents_info = {
            "normal":  {"name": "通常射撃", "desc": "標準的な攻撃をしてくる"},
            "barrage": {"name": "一斉射撃", "desc": "⚠️危険！敵の命中率1.6倍 (盾役・弾幕・やぐら妨害が有効)"},
            "repair":  {"name": "城壁修復", "desc": "🧱ターン終了時に城壁HPを回復する (やぐらで妨害可能)"},
            "supply":  {"name": "雪玉補給", "desc": "✨チャンス！敵の攻撃が弱まる (命中率0.5倍)"},
        }
        return intent, intents_info[intent]

    def get_input(self, role_key, remaining):
        config = self.roles_config[role_key]
        limit = min(remaining, config["max"]) if config["max"] is not None else remaining
        limit_str = f"最大{config['max']}人 / " if config["max"] is not None else ""

        while True:
            try:
                prompt = f"  {config['name']} [{config['desc']}] ({limit_str}残{remaining}人) > "
                user_input = input(prompt)
                if user_input == "":
                    return 0
                val = int(user_input)
                if 0 <= val <= limit:
                    return val
                print(f"  ! 0〜{limit}の間で入力してください")
            except ValueError:
                print("  ! 数字を入力してください")

    def battle_phase(self, enemy_max, wall_max):
        enemy_curr = enemy_max
        wall_curr = wall_max
        turn = 1
        
        while enemy_curr > 0 and self.troops > 0:
            # 3ターンごとに天候変化（最初は晴れ）
            if turn == 1:
                weather = self.weathers[0]
            elif turn % 3 == 1:
                weather = random.choice(self.weathers)
                print(f"\n🌤️ 天候が変わった！ 【{weather['name']}】 ({weather['desc']})")
                time.sleep(0.5)

            # 敵の行動予兆を決定
            intent_key, intent_info = self.get_enemy_intent(wall_curr, wall_max)

            print("\n" + "="*65)
            print(f"【 ターン {turn} 】 天候: {weather['name']} ({weather['desc']})")
            
            wall_status = "崩壊 (総力戦！)" if wall_curr <= 0 else f"耐久 {wall_curr}/{wall_max} (射撃命中ダウン)"
            print(f" 自軍: {self.troops}/{self.max_troops}人 | ❄️ 雪玉: {self.snowballs}個")
            print(f" 敵軍: {enemy_curr}/{enemy_max}人 | 🧱 城壁: {wall_status}")
            print(f" 🔭 敵の予兆: 【{intent_info['name']}】 {intent_info['desc']}")
            print("="*65)

            # --- 1. アサイン入力 ---
            alloc = {}
            remaining = self.troops
            input_order = ["maker", "shield", "ram", "tower", "sling"]
            
            for r in input_order:
                if remaining > 0:
                    count = self.get_input(r, remaining)
                    alloc[r] = count
                    remaining -= count
                else:
                    alloc[r] = 0
            alloc["normal"] = remaining
            if remaining > 0:
                print(f"  通常攻撃 [{self.roles_config['normal']['desc']}] に残り {remaining} 人を配置。")
            
            print("\n>>> 作戦実行 >>>")
            time.sleep(0.5)

            # --- 2. 自軍アクション ---
            
            # 1) 雪玉製造
            if alloc["maker"] > 0:
                per_maker = 3 + weather["make_bonus"]
                made = alloc["maker"] * per_maker
                self.snowballs += made
                print(f"📦 玉つくり部隊が雪玉を {made} 個製造 (在庫: {self.snowballs})")

            # 2) ラム（壁破壊）
            wall_broken_this_turn = False
            if alloc["ram"] > 0:
                if wall_curr > 0:
                    ram_dmg = 0
                    for _ in range(alloc["ram"]):
                        if random.random() < 0.65:
                            ram_dmg += (15 + weather["dmg_bonus"])
                    if ram_dmg > 0:
                        wall_curr = max(0, wall_curr - ram_dmg)
                        print(f"🐏 ラム部隊が城壁に突撃！ {ram_dmg} ダメージを与えた！(残耐久: {wall_curr})")
                        if wall_curr == 0:
                            wall_broken_this_turn = True
                            print("💥 敵の城壁が完全に崩壊！ 敵は動揺して反撃が鈍る！")
                    else:
                        print("🐏 ラム部隊の突撃は弾かれた...")
                else:
                    print("🐏 ラム部隊はすでに壁がないため待機した。")

            # 3) 射撃部隊の処理
            wall_factor = 0.25 if wall_curr > 0 else 1.0
            total_hits = 0
            intent_disrupted = False
            suppression_bonus = 0.0 # 通常攻撃の弾幕による敵命中ダウン
            
            shooters = ["tower", "sling", "normal"]
            for role in shooters:
                count = alloc[role]
                if count == 0: continue
                
                conf = self.roles_config[role]
                cost = conf["cost"]
                needed = count * cost
                
                actual_shooters = count
                if self.snowballs < needed:
                    actual_shooters = self.snowballs // cost
                    self.snowballs -= actual_shooters * cost
                    print(f"⚠️ {conf['name']}部隊: 雪玉不足で {count - actual_shooters} 人が攻撃不能！")
                else:
                    self.snowballs -= needed
                
                if actual_shooters == 0: continue

                # 命中判定
                hit_prob = conf["acc"] * weather["acc_mod"]
                if role == "tower":
                    # やぐらは壁の影響をほぼ無視
                    hit_prob *= 0.85 if wall_curr > 0 else 1.0
                else:
                    hit_prob *= wall_factor

                role_hits = 0
                double_hits = 0
                for _ in range(actual_shooters):
                    if random.random() < hit_prob:
                        role_hits += 1
                        # スリングの貫通効果
                        if role == "sling" and random.random() < 0.3:
                            role_hits += 1
                            double_hits += 1
                
                # 通常攻撃の弾幕効果（最大0.15まで敵の命中率を下げる）
                if role == "normal":
                    suppression_bonus = min(0.15, actual_shooters * 0.01)

                # やぐらの妨害効果（特殊行動をキャンセル）
                if role == "tower" and role_hits > 0 and intent_key in ["barrage", "repair"]:
                    disrupt_chance = min(0.85, 0.25 * role_hits)
                    if random.random() < disrupt_chance:
                        intent_disrupted = True

                if role_hits > 0:
                    extra_msg = f" (うち貫通{double_hits}回！)" if double_hits > 0 else ""
                    print(f"⚔️ {conf['name']}部隊: {role_hits} 人の敵に命中！{extra_msg}")
                    total_hits += role_hits

            if suppression_bonus >= 0.05:
                print(f"💨 通常攻撃の弾幕で敵を牽制！ (敵の命中率 -{int(suppression_bonus*100)}%)")

            if intent_disrupted:
                print(f"🎯 やぐら部隊の精密射撃！ 敵の【{intent_info['name']}】を妨害した！")

            enemy_curr = max(0, enemy_curr - total_hits)
            if enemy_curr == 0:
                return True, self.troops

            # --- 3. 敵の反撃 ---
            print("\n🔻 敵の反撃 🔻")
            time.sleep(0.5)

            # 城壁修復の処理
            if intent_key == "repair" and not intent_disrupted and wall_curr > 0:
                heal = min(wall_max - wall_curr, enemy_curr * 2)
                wall_curr += heal
                print(f"🧱 敵が城壁を修復した！ (耐久 +{heal} -> {wall_curr})")

            # 敵の命中率計算
            enemy_acc = 0.16 if wall_curr > 0 else 0.28
            enemy_acc *= weather["acc_mod"]
            
            if intent_key == "barrage" and not intent_disrupted:
                print("🔥 敵の一斉射撃が降り注ぐ！")
                enemy_acc *= 1.6
            elif intent_key == "supply":
                print("📦 敵は雪玉の補給を優先している。")
                enemy_acc *= 0.5
            
            if wall_broken_this_turn:
                enemy_acc *= 0.5
            
            enemy_acc = max(0.03, enemy_acc - suppression_bonus)

            enemy_hits = sum(1 for _ in range(enemy_curr) if random.random() < enemy_acc)
            
            if enemy_hits > 0:
                print(f"敵の雪玉が {enemy_hits} 発飛んできた！")
                dead_log = {r: 0 for r in self.roles_config}
                shield_blocks = 0
                
                for _ in range(enemy_hits):
                    if self.troops <= 0: break
                    
                    candidates = [r for r, c in alloc.items() if c > 0]
                    if not candidates: break
                    weights = [alloc[r] * self.roles_config[r]["aggro"] for r in candidates]

                    hit_role = random.choices(candidates, weights=weights, k=1)[0]
                    
                    # 盾役のガード判定
                    if hit_role == "shield" and random.random() < 0.6:
                        shield_blocks += 1
                        continue
                    
                    alloc[hit_role] -= 1
                    dead_log[hit_role] += 1
                    self.troops -= 1
                
                if shield_blocks > 0:
                    print(f"🛡️ 盾役部隊が {shield_blocks} 発の雪玉を弾き返した！")

                for r, count in dead_log.items():
                    if count > 0:
                        msg = f"💀 {self.roles_config[r]['name']}が {count} 名脱落..."
                        if self.roles_config[r]['aggro'] >= 4.0:
                            msg += " (集中砲火)"
                        print(msg)
            else:
                print("敵の攻撃はすべて外れた！")

            turn += 1

        return False, self.troops

    def run(self):
        self.print_slow("\n❄️ 戦略シミュレーション：アドバンスド雪合戦 Ver.2 ❄️")
        print("敵の予兆と天候を読み、6つの役割を組み合わせて雪原を制圧せよ！")
        time.sleep(1)

        while self.stage <= self.max_stage:
            data = self.stages[self.stage]
            print("\n" + "#"*55)
            print(f" STAGE {self.stage}: VS {data['name']}")
            print("#"*55)
            time.sleep(1)
            
            win, survivors = self.battle_phase(data["enemy"], data["wall"])
            
            if not win:
                print("\n" + "="*50)
                print(" 💀 DEFEAT... 部隊は全滅しました...")
                print("="*50)
                break
            else:
                print("\n" + "="*50)
                print(f" 🎉 STAGE {self.stage} CLEAR! ({data['name']}を撃破)")
                
                if self.stage < self.max_stage:
                    recover = 12
                    self.troops = min(self.max_troops, self.troops + recover)
                    self.snowballs += 15
                    print(f" 🚑 救護班と補給部隊が到着！(部隊+{recover}名 / 雪玉+15個)")
                    self.print_slow(" 次の戦いに備えてください...")
                    time.sleep(1.5)
                self.stage += 1

        if self.troops > 0:
            print("\n" + "*"*55)
            print(f" 🏆 CONGRATULATIONS! 完全勝利！(残存部隊: {self.troops}名)")
            print("*"*55)

if __name__ == "__main__":
    game = AdvancedSnowballFight()
    game.run()
    input("\nHit ENTER key to exit : ")