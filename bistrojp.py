"""bistro management simulation"""
"""from Frazer Management Simulation Games by J.Ronald Frazer"""

drink_price_average = 0

class Player:

    def __init__(self):
        self.name = ""
        self.band = 0
        self.charge_price = 0
        self.drink_price = 0
        self.customer_number = 0
        self.income_total = 0

    def set_name(self, string):
        self.name = string

    def order_average(self):
        if self.drink_price > 35:
            return 5 - ((self.drink_price - 35) / 30)
        else:
            return 5 + ((35 - self.drink_price) / 5)

    def income(self):
        return int(self.charge_price * self.customer_number +  \
               (self.drink_price - 30) * self.customer_number * \
               int(self.order_average()) - self.band_cost())

    def add_income(self):
        self.income_total = self.income_total + self.income()

    def customer_per_band(self):
        band_list = [300, 600, 750, 900]
        return band_list[self.band]

    def band_cost(self):
        band_cost_list = [0, 10000, 20000, 40000]
        return band_cost_list[self.band]

    def calc_customer(self):
        global drink_price_average
        self.customer_number = int(self.customer_per_band() + \
            300 - 6 * self.charge_price + \
            (drink_price_average - self.drink_price) * 30)

def description():
    print()
    print("ビストロ（音楽を楽しめるカフェバー）を経営するゲームです。")
    print("より有名なバンドを入れると多くの顧客がつきます。")
    print("有名な度合いにあわせて報酬（コスト）がかかります。")
    print("カバーチャージ（入場料）が５０円を超えると")
    print("客の人数が減ります。")
    print("ドリンクには３０円の原価がかかります。")
    print("ドリンクが高くなりすぎると注文数が減ります。")
    print()

def input_number(string, min, max):
    is_accepted = False
    while not is_accepted:
        inputed_string = input(string)
        if inputed_string.isnumeric():
            inputed_number = int(inputed_string)
            if inputed_number >= min:
                if inputed_number <= max:
                    result = inputed_number
                    is_accepted = True
                else:
                    print(f"最大値は{max}です")
            else:
                print(f"最小値は{min}です")
        else:
            print("数値を入力してください")
    return result

def main():
    inp = input("説明が必要ですか？(y or other)：").lower().strip()
    if inp == "y" or inp == "yes":
        description()
    global drink_price_average
    player_number = input_number("何人でプレイしますか:", 1, 10)
    week_number = 1
    players = []
    for i in range(1,player_number + 1):
        players.append(Player())
    for i, player in enumerate(players):
        player.set_name(input(f"プレイヤー{i+1}の名前："))
    for j in range(1,7):
        week_name = ""
        if j == 1:
            week_name = str(j) + "st"
        elif j == 2:
            week_name = str(j) + "nd"
        elif j == 3:
            week_name = str(j) + "rd"
        else:
            week_name = str(j) + "th"
        print(f"{week_name} week:")
        for i, player in enumerate(players):
            print(f"プレイヤー No.{i + 1} {player.name}さん:")
            print(f"0:バンドなし 1:無名のバンド 2:標準的なバンド 3:有名なバンド")
            player.band = input_number("店で雇うバンドを決めてください:", 0, 3)
            player.charge_price = input_number("カバーチャージ（入場料）:", 0, 1000)
            player.drink_price = input_number("ドリンクの値段:", 0, 1000)
        sum = 0
        for i in players:
            sum = sum + i.drink_price
        drink_price_average = sum / player_number
        print(f"{week_name} week:")
        for i, player in enumerate(players):
            player.calc_customer()
            player.add_income()
            print(f"プレイヤー No.{i + 1}　{player.name}さん") 
            print(f"    収益 : {player.income()}")
            print(f"    客の人数 : {player.customer_number}")
            print(f"　　現在までの総収益 : {player.income_total}")
    print()
    print("6週終了")
    print("結果発表：")
    for i, player in enumerate(players):
        print(f"　　プレイヤー No.{i+1} {player.name}さん　総収益：{player.income_total}")

if __name__ == '__main__':
    main()
