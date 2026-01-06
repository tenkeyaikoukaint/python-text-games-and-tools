import random
import time

class AdvancedYukigassen:
    def __init__(self):
        self.my_units = 50  # 自軍は50人固定
        self.snowballs = 20 # 初期の雪玉
        self.wall_hp = 100  # 敵の城壁耐久度 (100%)
        self.turn = 1
        
        # 敵レベル設定
        self.enemy_units = 0
        self.enemy_level_name = ""

    def start_game(self):
        print("=== 戦略シミュレーション：アドバンスド雪合戦 ===")
        print("敵のレベルを選択してください：")
        print("1: 初級 (敵10人 - 小手調べ)")
        print("2: 中級 (敵30人 - 接戦)")
        print("3: 上級 (敵50人 - 死闘)")
        
        while True:
            try:
                choice = int(input("選択 (1-3) > "))
                if choice == 1:
                    self.enemy_units = 10
                    self.enemy_level_name = "初級部隊"
                    break
                elif choice == 2:
                    self.enemy_units = 30
                    self.enemy_level_name = "正規軍"
                    break
                elif choice == 3:
                    self.enemy_units = 50
                    self.enemy_level_name = "精鋭部隊"
                    break
            except ValueError:
                pass
        
        print(f"\n【戦闘開始】自軍: {self.my_units}人 vs {self.enemy_level_name}: {self.enemy_units}人 (城壁あり)")
        time.sleep(1)
        self.game_loop()

    def game_loop(self):
        while self.my_units > 0 and self.enemy_units > 0:
            self.play_turn()
            if self.enemy_units <= 0:
                print("\n" + "="*30)
                print(" 🏆 VICTORY！ 敵を殲滅しました！")
                print("="*30)
                return
            if self.my_units <= 0:
                print("\n" + "="*30)
                print(" 💀 DEFEAT... 全滅しました...")
                print("="*30)
                return
            
            self.turn += 1
            print("-" * 40)

    def play_turn(self):
        print(f"\n--- 第 {self.turn} ターン ---")
        print(f"[戦況] 自軍: {self.my_units}人 | 雪玉: {self.snowballs}個 | 敵: {self.enemy_units}人 | 敵城壁耐久: {self.wall_hp}%")
        
        # 命中率の計算（城壁があるほど命中率が下がる）
        # 城壁100%で命中率マイナス30%、城壁0%でペナルティなし
        wall_penalty = int(30 * (self.wall_hp / 100))
        print(f"[情報] 城壁による命中率ペナルティ: -{wall_penalty}%")

        # 人員配置
        print("\n【作戦タイム】メンバーを割り当ててください (合計が現在人数になるように)")
        
        remaining = self.my_units
        roles = {}
        
        try:
            # 1. 玉つくり
            print(f"  残存兵力: {remaining}")
            roles['maker'] = int(input("  雪玉製造班 (玉+3/人) > "))
            remaining -= roles['maker']
            if remaining < 0: raise ValueError
            
            # 2. ラム
            print(f"  残存兵力: {remaining}")
            roles['ram'] = int(input("  ラム班 (城壁破壊・被弾率高) > "))
            remaining -= roles['ram']
            if remaining < 0: raise ValueError

            # 3. スリング
            print(f"  残存兵力: {remaining}")
            roles['sling'] = int(input("  スリング班 (玉消費3/強攻撃・命中高) > "))
            remaining -= roles['sling']
            if remaining < 0: raise ValueError

            # 4. やぐら
            print(f"  残存兵力: {remaining}")
            roles['tower'] = int(input("  やぐら班 (命中高・被弾率高) > "))
            remaining -= roles['tower']
            if remaining < 0: raise ValueError

            # 5. 通常攻撃 (残り全て)
            roles['normal'] = remaining
            print(f"  通常攻撃班: {roles['normal']}人 (自動割り当て)")

        except ValueError:
            print(">>> エラー：人数の割り当てが不正です。再入力してください。")
            return # このターンの最初に戻る（簡易実装のためループ継続）

        print("\n--- 実行フェーズ ---")
        time.sleep(1)

        # 1. 雪玉製造
        made_balls = roles['maker'] * 3
        self.snowballs += made_balls
        print(f"🔨 製造班が {made_balls} 個の雪玉を作りました。(総数: {self.snowballs})")

        # 2. 自軍の攻撃処理
        total_hits = 0
        wall_damage = 0
        
        # 消費コスト計算
        cost_normal = roles['normal'] * 1
        cost_sling = roles['sling'] * 3
        cost_tower = roles['tower'] * 1
        
        # 雪玉不足チェック
        total_cost = cost_normal + cost_sling + cost_tower
        
        if self.snowballs < total_cost:
            print(f"⚠ 雪玉不足！ ({self.snowballs} < 必要数 {total_cost}) 全力攻撃できません！")
            # 簡易的に、不足時は命中率が激減するペナルティとする
            efficiency = self.snowballs / total_cost if total_cost > 0 else 0
            self.snowballs = 0
        else:
            efficiency = 1.0
            self.snowballs -= total_cost

        # --- 攻撃実行 ---
        
        # ラム (城壁破壊) - 敵への直接ダメージはないが城壁を削る
        if roles['ram'] > 0:
            ram_success = 0
            for _ in range(roles['ram']):
                # ラム成功率 60%
                if random.random() < 0.6:
                    ram_success += 1
            damage_to_wall = ram_success * 10 # 1成功につき10%削る
            self.wall_hp = max(0, self.wall_hp - damage_to_wall)
            wall_damage = damage_to_wall
            print(f"🐏 ラム班: {roles['ram']}人中 {ram_success}人が城壁への打撃成功！ 城壁HP -{damage_to_wall}")

        # 基本命中率 (城壁の影響を受ける)
        base_hit_rate = 50 - wall_penalty # 通常50% - ペナルティ
        
        # スリング (命中率高い +20%, 威力は1確殺だがコストが高い)
        if roles['sling'] > 0:
            hits = 0
            hit_rate = (base_hit_rate + 20) * efficiency
            for _ in range(roles['sling']):
                if random.random() * 100 < hit_rate:
                    hits += 1
            print(f"🏹 スリング班: {hits} HIT!")
            total_hits += hits

        # やぐら (命中率高い +15%)
        if roles['tower'] > 0:
            hits = 0
            hit_rate = (base_hit_rate + 15) * efficiency
            for _ in range(roles['tower']):
                if random.random() * 100 < hit_rate:
                    hits += 1
            print(f"🗼 やぐら班: {hits} HIT!")
            total_hits += hits

        # 通常攻撃
        if roles['normal'] > 0:
            hits = 0
            hit_rate = base_hit_rate * efficiency
            for _ in range(roles['normal']):
                if random.random() * 100 < hit_rate:
                    hits += 1
            print(f"⚔ 通常攻撃班: {hits} HIT!")
            total_hits += hits

        # 敵の損害適用
        self.enemy_units = max(0, self.enemy_units - total_hits)
        print(f">>> 敵軍に {total_hits} のダメージを与えた！ (敵残り: {self.enemy_units})")
        
        if self.enemy_units <= 0: return # 敵全滅ならループ終了へ

        time.sleep(1)

        # 3. 敵の反撃
        print("\n⚡ 敵の反撃！")
        # 敵の攻撃力（人数依存）
        enemy_attacks = self.enemy_units
        # 敵の命中率（固定40%とする）
        enemy_hit_rate = 40
        
        enemy_hits = 0
        for _ in range(enemy_attacks):
            if random.random() * 100 < enemy_hit_rate:
                enemy_hits += 1
        
        print(f"敵が {enemy_attacks} 個の雪玉を投げた！ >> {enemy_hits} 人に直撃！")

        # 被弾処理 (ラムとやぐらは被弾しやすい＝優先的に減る)
        # リスク係数: ラム(3倍), やぐら(2倍), その他(1倍)
        # これを重み付け抽選で誰が当たるか決める
        
        casualties = {'ram': 0, 'tower': 0, 'sling': 0, 'maker': 0, 'normal': 0}
        
        # 現在生きているユニットのリストを作成（重み付き）
        target_pool = []
        target_pool.extend(['ram'] * roles['ram'] * 3)    # ラムは3倍当たりやすい
        target_pool.extend(['tower'] * roles['tower'] * 2) # やぐらは2倍
        target_pool.extend(['sling'] * roles['sling'])
        target_pool.extend(['maker'] * roles['maker'])
        target_pool.extend(['normal'] * roles['normal'])
        
        actual_deaths = 0
        if len(target_pool) > 0:
            for _ in range(enemy_hits):
                if not target_pool: break
                hit_role = random.choice(target_pool)
                casualties[hit_role] += 1
                actual_deaths += 1
                
                # poolから該当ロールを削除（死んだので）
                # 注意: 重み付けで複数入っているので、そのロールのすべてのエントリーを消すのではなく、1体分消す処理が必要だが
                # 簡易的に「死者数」だけカウントして後で引く
                
                # 厳密なプール削除は計算コストが高いので、ここでは単純に減らす
                # ただし、同じ人が何度も死なないようにチェックが必要
                if roles[hit_role] - casualties[hit_role] < 0:
                     casualties[hit_role] -= 1 # 戻す
                     actual_deaths -= 1

        # 死者を適用
        roles['ram'] -= casualties['ram']
        roles['tower'] -= casualties['tower']
        roles['sling'] -= casualties['sling']
        roles['maker'] -= casualties['maker']
        roles['normal'] -= casualties['normal']
        
        self.my_units -= actual_deaths
        
        if actual_deaths > 0:
            details = []
            if casualties['ram'] > 0: details.append(f"ラム班-{casualties['ram']}")
            if casualties['tower'] > 0: details.append(f"やぐら班-{casualties['tower']}")
            if casualties['sling'] > 0: details.append(f"スリング班-{casualties['sling']}")
            if casualties['maker'] > 0: details.append(f"製造班-{casualties['maker']}")
            if casualties['normal'] > 0: details.append(f"通常班-{casualties['normal']}")
            print(f">>> 被害内訳: {', '.join(details)}")
        else:
            print(">>> 奇跡的に全員無傷！")

# ゲーム起動
if __name__ == "__main__":
    game = AdvancedYukigassen()
    game.start_game()
