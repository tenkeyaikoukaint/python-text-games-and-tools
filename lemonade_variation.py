import random
import time
import os
import sys

# 画面表示の色設定（対応しているターミナルで色が付きます）
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class LemonadeStand:
    def __init__(self, days=7):
        self.total_days = days
        self.current_day = 1
        self.money = 2000.0  # 初期所持金
        self.reputation = 50.0 # お店の評判 (0-100)
        
        # 在庫
        self.inventory = {
            "lemons": 0,
            "sugar": 0,
            "cups": 0,
            "ice": 0
        }
        
        # 仕入れ単価
        self.cost = {
            "lemons": 30,
            "sugar": 5,
            "cups": 10,
            "ice": 3
        }
        
        # レシピ（初期値）
        self.recipe = {
            "lemon": 1,   # 1杯あたりのレモン個数
            "sugar": 3,   # 1杯あたりの砂糖単位
            "ice": 3,     # 1杯あたりの氷個数
            "price": 150  # 販売価格
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_slow(self, text, delay=0.01):
        """雰囲気を出すためのゆっくり表示"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def get_input(self, prompt, default=None):
        """入力を受け付けるヘルパー関数"""
        while True:
            try:
                val = input(f"{prompt} > ")
                if val == "" and default is not None:
                    return default
                val = int(val)
                if val < 0:
                    print(f"{Color.FAIL}  0以上の数を入力してください。{Color.ENDC}")
                    continue
                return val
            except ValueError:
                print(f"{Color.FAIL}  数字を入力してください。{Color.ENDC}")

    def get_weather(self):
        """天気を決定する"""
        weather_types = ["快晴", "晴れ", "曇り", "雨", "嵐"]
        weights = [15, 40, 25, 15, 5]
        weather = random.choices(weather_types, weights=weights)[0]
        
        # 天気に応じた気温設定
        if weather == "快晴": temp = random.randint(30, 38)
        elif weather == "晴れ": temp = random.randint(25, 32)
        elif weather == "曇り": temp = random.randint(20, 26)
        elif weather == "雨": temp = random.randint(18, 23)
        else: temp = random.randint(15, 20) # 嵐
        
        return weather, temp

    def shop_phase(self):
        """仕入れフェーズ"""
        print(f"\n{Color.HEADER}🛒 --- ショップ ---{Color.ENDC}")
        print(f"所持金: {int(self.money)}円")
        print("必要な材料を購入してください。（何も買わない場合はEnter）")
        
        items = [
            ("lemons", "🍋 レモン", self.cost["lemons"]),
            ("sugar", "🍬 砂糖　", self.cost["sugar"]),
            ("cups", "🥤 カップ", self.cost["cups"]),
            ("ice", "🧊 氷　　", self.cost["ice"])
        ]
        
        for key, name, price in items:
            max_buy = int(self.money // price)
            warning = f" {Color.WARNING}(※今日溶けます){Color.ENDC}" if key == "ice" else ""
            print(f"  {name} (@{price}円)  在庫:{self.inventory[key]}  {warning}")
            
            qty = self.get_input(f"    購入数 (最大{max_buy})", default=0)
            cost = qty * price
            
            if cost > self.money:
                print(f"    {Color.FAIL}お金が足りません！{Color.ENDC}")
            else:
                self.money -= cost
                self.inventory[key] += qty
                if qty > 0:
                    print(f"    -> {qty}個 購入しました。残金:{int(self.money)}円")

    def recipe_phase(self):
        """レシピ設定フェーズ"""
        print(f"\n{Color.HEADER}👨‍🍳 --- レシピ開発 ---{Color.ENDC}")
        print(f"現在の設定: レモン{self.recipe['lemon']} / 砂糖{self.recipe['sugar']} / 氷{self.recipe['ice']} / 価格{self.recipe['price']}円")
        print("変更しますか？ (変更しない場合はEnter連打でOK)")
        
        self.recipe['lemon'] = self.get_input(f"  🍋 レモン数 (現:{self.recipe['lemon']})", self.recipe['lemon'])
        self.recipe['sugar'] = self.get_input(f"  🍬 砂糖の量 (現:{self.recipe['sugar']})", self.recipe['sugar'])
        self.recipe['ice']   = self.get_input(f"  🧊 氷の数   (現:{self.recipe['ice']})", self.recipe['ice'])
        self.recipe['price'] = self.get_input(f"  💰 販売価格 (現:{self.recipe['price']})", self.recipe['price'])

    def simulate_day(self, weather, temp):
        """営業シミュレーション"""
        self.clear_screen()
        print(f"{Color.BOLD}🌞 デイリーレポート: {self.current_day}日目{Color.ENDC}")
        print(f"天気: {weather} / 気温: {temp}℃ / 評判: {self.reputation}")
        self.print_slow("開店しました！お客さんが通りかかります...", 0.05)
        
        # --- 需要計算ロジック ---
        # 1. 天候と評判による基礎客数
        base_customers = 30
        weather_factor = {"快晴": 1.5, "晴れ": 1.2, "曇り": 0.8, "雨": 0.5, "嵐": 0.1}
        demand = base_customers * weather_factor[weather] * (self.reputation / 50)
        
        # 2. 価格による補正 (基準150円)
        if self.recipe['price'] > 150:
            demand *= (150 / self.recipe['price']) ** 1.5 # 高いと急激に減る
        elif self.recipe['price'] < 100:
            demand *= 1.2 # 安いと増える
            
        potential_customers = int(demand)
        
        # --- 味の評価ロジック (黄金比) ---
        # レモン1に対して砂糖2〜3がベスト。氷は気温に応じて必要。
        taste_score = 0
        comments = []
        
        # バランス評価
        if self.recipe['lemon'] > 0:
            ratio = self.recipe['sugar'] / self.recipe['lemon']
            if 2.0 <= ratio <= 3.5:
                taste_score += 10
                comments.append("「美味しい！バランス最高！」")
            elif ratio < 2.0:
                taste_score -= 5
                comments.append("「すっぱい！」")
            else:
                taste_score -= 5
                comments.append("「甘すぎる...」")
        else:
            taste_score -= 20
            comments.append("「レモンの味がしない...水？」")

        # 温度評価
        ideal_ice = 0
        if temp >= 30: ideal_ice = 3
        elif temp >= 25: ideal_ice = 2
        elif temp >= 20: ideal_ice = 1
        
        if self.recipe['ice'] < ideal_ice:
            taste_score -= 10
            comments.append("「ぬるいなぁ...もっと冷やして！」")
        elif self.recipe['ice'] > ideal_ice + 2:
            taste_score -= 5
            comments.append("「氷多すぎ！量が少ないよ」")
        else:
            taste_score += 5
            
        # --- 販売処理 ---
        sold_cups = 0
        lost_opportunity = 0
        
        for _ in range(potential_customers):
            # 在庫チェック
            if (self.inventory['cups'] > 0 and 
                self.inventory['lemons'] >= self.recipe['lemon'] and
                self.inventory['sugar'] >= self.recipe['sugar'] and
                self.inventory['ice'] >= self.recipe['ice']):
                
                sold_cups += 1
                self.inventory['cups'] -= 1
                self.inventory['lemons'] -= self.recipe['lemon']
                self.inventory['sugar'] -= self.recipe['sugar']
                self.inventory['ice'] -= self.recipe['ice']
                self.money += self.recipe['price']
            else:
                lost_opportunity += 1
        
        # --- 結果表示 ---
        print("-" * 40)
        print(f"来店客数: {potential_customers}人")
        print(f"販売数　: {Color.BOLD}{sold_cups}杯{Color.ENDC}")
        print(f"売上高　: {Color.GREEN}{sold_cups * self.recipe['price']}円{Color.ENDC}")
        
        if lost_opportunity > 0:
            print(f"{Color.FAIL}⚠️ 在庫切れで {lost_opportunity}人の客を逃しました！{Color.ENDC}")
            self.reputation -= 2 # 在庫切れペナルティ
        
        # 客の声と評判更新
        if sold_cups > 0:
            feedback = random.choice(comments) if comments else "「まあまあの味だね」"
            print(f"💬 客の声: {feedback}")
            
            if taste_score > 0: self.reputation += random.randint(2, 5)
            elif taste_score < 0: self.reputation -= random.randint(2, 5)
        elif potential_customers == 0:
            print("💬 (誰もお客さんが来ませんでした...)")
        
        self.reputation = max(0, min(100, self.reputation))
        
        # 氷の融解
        melted_ice = self.inventory['ice']
        if melted_ice > 0:
            print(f"{Color.BLUE}💧 残った氷 {melted_ice}個 はすべて溶けてしまいました。{Color.ENDC}")
            self.inventory['ice'] = 0

        input("\n[Enter]キーを押して次の日へ...")

    def run(self):
        self.clear_screen()
        print(f"{Color.BOLD}{Color.WARNING}🍋 LEGENDARY LEMONADE STAND 🍋{Color.ENDC}")
        print(f"{self.total_days}日間で、最高の売上を目指しましょう！\n")
        input("スタートするにはEnterキーを押してください")

        for i in range(1, self.total_days + 1):
            self.current_day = i
            
            # 天気予報
            weather, temp = self.get_weather()
            
            # メインメニュー表示
            while True:
                self.clear_screen()
                print(f"{Color.HEADER}📅 DAY {i} / {self.total_days}{Color.ENDC}")
                print(f"💰 所持金: {int(self.money)}円  |  ⭐ 評判: {self.reputation}")
                print(f"🌤 天気予報: {weather} ({temp}℃)")
                if temp >= 30: print(f"  {Color.FAIL}🔥 猛暑です！冷たいレモネードが売れます！{Color.FAIL}")
                if weather == "雨": print(f"  {Color.BLUE}☔ 雨です。客足は鈍そうです...{Color.ENDC}")
                print("-" * 40)
                print("1. 仕入れに行く")
                print("2. レシピと価格の設定")
                print("3. 店を開ける（1日を始める）")
                
                cmd = input("選択 > ")
                if cmd == '1':
                    self.shop_phase()
                elif cmd == '2':
                    self.recipe_phase()
                elif cmd == '3':
                    # カップがない場合の警告
                    if self.inventory['cups'] == 0:
                        print(f"{Color.FAIL}⚠️ カップの在庫が0です！これでは売れません！{Color.ENDC}")
                        time.sleep(1.5)
                        continue
                    break
            
            self.simulate_day(weather, temp)
            
            # 破産判定
            if self.money < 10 and self.inventory['cups'] == 0:
                print(f"\n{Color.FAIL}💸 資金が尽き、商品も作れません... ゲームオーバー 💸{Color.ENDC}")
                break

        # 最終結果
        self.clear_screen()
        profit = int(self.money - 2000)
        print(f"{Color.BOLD}🎉 GAME FINISHED 🎉{Color.ENDC}")
        print(f"最終所持金: {int(self.money)}円")
        print(f"純利益　　: {profit}円")
        
        if profit > 10000:
            print(f"{Color.WARNING}🏆 ランク: レモネード王（伝説の経営者！）{Color.ENDC}")
        elif profit > 3000:
            print(f"{Color.GREEN}🥈 ランク: 大繁盛店（素晴らしい！）{Color.ENDC}")
        elif profit > 0:
            print(f"{Color.CYAN}🥉 ランク: 黒字達成（おめでとう！）{Color.ENDC}")
        else:
            print(f"{Color.FAIL}💀 ランク: 赤字経営（次は頑張ろう...）{Color.ENDC}")

if __name__ == "__main__":
    game = LemonadeStand()
    game.run()