"""the holy stone light unlimited version"""
"""a role-playing game"""
"""play : about 1 hour"""

import random
import pickle

enemy_name_list = [" ", "Silver Wolf", "Assasin", "Dark Knight", "Fire Lizard", "Ghost Knight", "Dragon"]
enemy_hit_point_max = [0, 20, 50, 100, 200, 300, 1000]
enemy_strength = [0, 10, 20, 30, 40, 50, 100]
enemy_weapon_power = [0, 10, 20, 30, 40, 50, 100]
enemy_gold = [0, 10, 20, 50, 100, 200, 1000]
enemy_exp_point = [0, 10, 30, 60, 120, 240, 1000]
weapon_name = [" ", "Dagger", "Axe", "Mace", "Short sword", "Sword", "Heavy Mace", "Battle Axe"]
weapon_power = [0, 5, 10, 20, 30, 50, 60, 70]
weapon_price = [0, 10, 50, 110, 500, 1000, 2000, 5000, 10000, 25000, 50000]
armor_name = [" ", "Cloth", "Leather", "Chain Mail", "Breast Plate"]
armor_power = [0, 10, 20, 30, 50]
armor_price = [0, 100, 500, 2000, 5000]
need_exp_point_per_level = [0, 100, 200, 500, 1000, 2000, 3000, 4000, 5000, 7000, 10000, 100000, 200000, 400000, 1000000, 10000000]

MAZE = 0
BATTLE = 1

class GameVals:

    def __init__(self):
        self.is_map_visible = False
        self.player_name = "Player"
        self.player_hit_point = 100
        self.player_hit_point_max = 100
        self.player_strength = 30
        # DEX of : Dagger, Mace, Axe, Sword / Now not in use
        self.player_dexterity = [0, 10, 10, 10, 10]
        self.player_weapon = 1
        self.player_armor = 1
        self.player_luck_point = 10
        self.player_gold = 100
        self.player_exp_point = 0
        self.player_level = 0
        self.mx = 2
        self.my = 2
        self.enemy_number = 0
        self.enemy_hit_point = 0
        self.is_game_run = True
        self.command_mode = MAZE
        self.game_state = Maze()

class GameState:

    def __init__(self):
        self.map=[]

    def prompt(self, game):
        if game.is_map_visible:
            for i in range(-2,3):
                string = ""
                for j in range(-2,3):
                    if i == 0 and j == 0:
                        string = string + "O"
                    elif self.get_map(game.mx+j,game.my+i) == 1:
                        string = string + "."
                    elif self.get_map(game.mx+j,game.my+i) == 2:
                        string = string + "?"
                    else:
                        string = string + "#"
                print(string)
        string = ""
        if self.get_map(game.mx,game.my-1) >= 1:
            string = string + "north "
        if self.get_map(game.mx,game.my+1) >= 1:
            string = string + "south "
        if self.get_map(game.mx+1,game.my) >= 1:
            string = string + "east "
        if self.get_map(game.mx-1,game.my) >= 1:
            string = string + "west "
        print(f"You can go [{string}].")

    def report(self,game):
        print()
        print("[Report]")
        print(f"Name:{game.player_name}")
        print(f"HP:{game.player_hit_point}/{game.player_hit_point_max}  STR:{game.player_strength}")
        print(f"Weapon:{weapon_name[game.player_weapon]}, Armor:{armor_name[game.player_armor]}")
        print(f"Level:{game.player_level} EXP:{game.player_exp_point}")
        print(f"Gold:{game.player_gold}")
        print()

    def get_map(self,x,y):
        return self.map[y*12+x]

class Battle:

    def battle(self,game):
        strength_sum = game.player_strength + enemy_strength[game.enemy_number]
        r = random.randint(0, strength_sum)
        if r < game.player_strength:
            print("Your hit!")
            damage = random.randint(0, weapon_power[game.player_weapon])
            game.enemy_hit_point = game.enemy_hit_point - damage
            print(f"{damage} damages Enemy HP:{game.enemy_hit_point}")
            if game.enemy_hit_point <= 0:
                print("You have won!")
                print(f"You got {enemy_exp_point[game.enemy_number]}exp and {enemy_gold[game.enemy_number]}gold")
                game.player_exp_point = game.player_exp_point + enemy_exp_point[game.enemy_number]
                game.player_gold = game.player_gold + enemy_gold[game.enemy_number]
                game.command_mode = MAZE
                if game.enemy_number == 6:
                    print("You got the holy stone!")
                    print("*** Game End ***")
                    game.is_game_run = False
        else:
            print("Enemy's hit!")
            damage = random.randint(0, enemy_weapon_power[game.enemy_number])
            if armor_power[game.player_armor] < damage:
                damage = damage - armor_power[game.player_armor]
                game.player_hit_point = game.player_hit_point - damage
            else:
                damage = random.randint(0,5)
                game.player_hit_point = game.player_hit_point - damage
            print(f"{damage} damages Your HP:{game.player_hit_point}")
            if game.player_hit_point <= 0:
                print("You have lost...")
                game.command_mode = MAZE
                game.is_game_run = False
        return game

    def encount(self,game):
        while game.command_mode == BATTLE:
            print(f"{enemy_name_list[game.enemy_number]} HP:{game.enemy_hit_point}")
            inp = ""
            while inp != "f" and inp != "e":
                inp = input("f)ight or e)scape:")
                if inp == "f":
                    game = self.battle(game)
                if inp == "e":
                    r = random.randint(0,20)
                    if r <= game.player_luck_point:
                        print("You have escaped.")
                        game.command_mode = MAZE
                    else:
                        print("You have failed to escape.")
                        game = self.battle(game)
        return game

class Maze(GameState):

    def __init__(self):
        self.map=[
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
            0,0,0,0,0,0,0,0,0,0,0,0]
        map_validator()
        self.battle=Battle()

    def description(self, game):
        print("[Maze]")
        self.prompt(game)
        if game.is_map_visible == False:
            print("nsew:move r:report o:open map g:save game")
        else:
            print("nsew:move r:report c:close map g:save game")

    def event(self,game):
        if self.get_map(game.mx,game.my)==2:
            if game.mx == 2 and game.my == 2:
                print("There is a ladder to overground.")
                print("u:go up")
                inp = input(">")
                if inp == "u":
                    game.mx = 9
                    game.my = 9
                    game.game_state = Town()
            if game.mx == 9 and game.my == 4:
                if game.player_level <= 1:
                    game.enemy_number = 1
                elif game.player_level <= 3:
                    game.enemy_number = 2
                elif game.player_level <= 5:
                    game.enemy_number = 3
                elif game.player_level <= 7:
                    game.enemy_number = 4
                else:
                   game.enemy_number = 5
                game.enemy_number = r
                print("A monster is looming...")
                game.enemy_hit_point = enemy_hit_point_max[game.enemy_number]
                game.command_mode = BATTLE
                game = self.battle.encount(game)
            if game.mx == 8 and game.my == 6:
                print("< The dragon's nest! >")
                game.enemy_number = 6
                game.enemy_hit_point = enemy_hit_point_max[game.enemy_number]
                game.command_mode = BATTLE
                game = self.battle.encount(game)
        else:
            r = random.randint(0,5)
            if r == 1:
                print("An enemy appears...")
                game.enemy_number = random.randint(1,5)
                game.enemy_hit_point = enemy_hit_point_max[game.enemy_number]
                game.command_mode = BATTLE
                game=self.battle.encount(game)
        return game

    def command_execute(self, command, game):
        if command == "n" and self.get_map(game.mx,game.my-1) >= 1:
            game.my = game.my-1
        if command == "s" and self.get_map(game.mx,game.my+1) >= 1:
            game.my = game.my + 1
        if command == "e" and self.get_map(game.mx+1,game.my) >= 1:
            game.mx = game.mx + 1
        if command == "w" and self.get_map(game.mx-1,game.my) >= 1:
            game.mx = game.mx - 1
        if command == "r":
            self.report(game)
        if command == "c" and game.is_map_visible == True:
            game.is_map_visible = False
        if command=="o" and game.is_map_visible == False:
            game.is_map_visible = True
        if command == "g":
            file=open("hsdata",'wb')
            pickle.dump(game,file)
            file.close()
            print("The current game state has saved.")
        game = self.event(game)
        return game

class Maze2f(Maze):

    pass

class Maze3f(Maze):

    pass

class Town(GameState):

    def __init__(self):
        """Weapon Shop, Armor Shop, Healer, Oracle"""
        self.map=[
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
            0,0,0,0,0,0,0,0,0,0,0,0]
        map_validator()

    def description(self,game):
        print("[Town]")
        self.prompt(game)
        if game.is_map_visible == False:
            print("nsew:move r:report l:sleep on the road o:open map")
        else:
            print("nsew:move r:report l:sleep on the road c:close map")

    def command_execute(self, command, game):
        if command == "n" and self.get_map(game.mx,game.my-1) >= 1:
            game.my = game.my - 1
        if command == "s" and self.get_map(game.mx,game.my+1) >= 1:
            game.my = game.my + 1
        if command == "e" and self.get_map(game.mx+1,game.my) >= 1:
            game.mx = game.mx + 1
        if command == "w" and self.get_map(game.mx-1,game.my) >= 1:
            game.mx = game.mx-1
        if command == "r":
            self.report(game)
        if command == "c" and game.is_map_visible == True:
            game.is_map_visible = False
        if command=="o" and game.is_map_visible == False:
            game.is_map_visible = True
        if command == "l":
            print("Your HP has full recovered.")
            game.player_hit_point = game.player_hit_point_max
            r = random.randint(1,5)
            if r == 1:
                r2 = random.randint(1,3)
                if r2 == 1:
                    r3 = random.randint(1, game.player_gold)
                    print(f"{r3} gold was stolen.")
                    game.player_gold = game.player_gold - r3
                elif r2 == 2:
                    print("Your weapon was stolen.")
                    game.player_weapon = 1
                else:
                    print("Your armor was stolen.")
                    game.player_armor = 1
        if game.mx == 5 and game.my == 5:
            shop = "weapon"
            game = self.shopdo(game, shop)
        if game.mx == 3 and game.my == 9:
            shop = "armor"
            game = self.shopdo(game, shop)
        if game.mx == 9 and game.my == 5:
            shop = "healer"
            game = self.shopdo(game, shop)
        if game.mx == 9 and game.my == 3:
            shop = "oracle"
            game = self.shopdo(game, shop)
        if game.mx == 9 and game.my == 9:
            print("There is a ladder to underground")
            print("d:go down")
            inp = input(">")
            if inp == "d":
                game.mx = 2
                game.my =2
                game.game_state =Maze()
        return game

    def shop(self):
        pass

    def shopdo(self, game, shop):
        """Like Haskell's IO Monad(chain)"""
        if shop == "weapon":
            print("[Weapon Shop]")
            print("Hi, adventurer! what do you need?")
            string=""
            weapon_number = 8
            for i in range(1,weapon_number):
                string = f"{string}{i}:{weapon_name[i]}({weapon_price[i]}g) "
            print(f"{string}")
            print("other:exit")
            inputed_string = input(">")
            try:
                inputed_number = int(inputed_string)
                if inputed_number >= 1 and inputed_number <= 7:
                    if game.player_gold >= weapon_price[inputed_number]:
                        print(f"You got {weapon_name[inputed_number]}.")
                        game.player_gold = game.player_gold - weapon_price[inputed_number]
                        game.player_weapon = inputed_number
                    else:
                        print("Too expensive to buy.")
                else:
                    print("See you next time.")
            except ValueError:
                print("You have input not a number thus exit the shop.")
        if shop=="healer":
            print("[healer]")
            print("Ah...welcome. Do you need help?")
            print("h:heal l:level up other:exit")
            inp = input(">")
            if inp == "h":
                heal_price = (game.player_level+1) * 20
                print(f"{heal_price} gold. OK?(y or other)")
                inp = input(">")
                if inp == "y":
                    if game.player_gold >= heal_price:
                        print("Your HP have reached the max point.")
                        game.player_hit_point = game.player_hit_point_max
                        game.player_gold = game.player_gold - heal_price
                    else:
                        print("Your gold is not enough.")
                else:
                    print("Good bye.")
            if inp == "l":
                if game.player_level <= 14:
                    if game.player_exp_point >= need_exp_point_per_level[game.player_level + 1]:
                        game.player_level = game.player_level + 1
                        print("Level up!")
                        print(f"Now your level is:{game.player_level}")
                        game.player_hit_point_max = game.player_hit_point_max + 50
                        game.player_hit_point = game.player_hit_point_max
                        game.player_strength = game.player_strength + 5
                    else:
                        print(f"You need {need_exp_point_per_level[game.player_level+1]-game.player_exp_point} exp to the next level.")
                else:
                    print("You already became the sword master.")
        if shop == "oracle":
            print("[Oracle]")
            print("Welcome, adventurer.")
            print("f:fortunetelling m:magic charm other:exit")
            inp = input(">")
            if inp == "f":
                if game.player_weapon == 1:
                    print("You must get some stronger weapon.")
                elif game.player_level <= 1:
                    print("Be careful with fire lizards and ghost knights!")
                elif game.player_level <= 2:
                    print("Have you found monster rooms?")
                else:
                    print("Have you found the dragon's nest? It is a goal.") 
            elif inp == "m":
                print("1000 gold payment for +1 your luck point.")
                print("OK?(y or other)")
                inp = input(">")
                if inp == "y":
                    if game.player_gold >= 1000:
                        print("Your luck goes up.")
                        game.player_luck_point = game.player_luck_point + 1
                        game.player_gold = game.player_gold - 1000
                        print(f"Now your luck point is:{game.player_luck_point}")
                    else:
                        print("You have not enough gold.")
            else:
                print("Good luck.")
        if shop=="armor":
            print("[Armor Shop]")
            print("Hello! we have good stuff.")
            string = ""
            for i in range(1,5):
                string=f"{string} {i}:{armor_name[i]}({armor_price[i]}g) "
            print(f"{string}")
            print("other:exit")
            inputed_string = input(">")
            try:
                inputed_number = int(inputed_string)
                if inputed_number >= 1 and inputed_number <= 4:
                    if game.player_gold >= armor_price[inputed_number]:
                        print(f"You got {armor_name[inputed_number]}.")
                        game.player_armor=inputed_number
                        game.player_gold = game.player_gold - armor_price[inputed_number]
                    else:
                        print("Too expensive to buy.")
                else:
                    print("See you again!")
            except ValueError:
                print("You have input not a number thus exit the shop.")
        return game

def map_validator():
    pass

def main():
    game=GameVals()
    game.game_state=Maze()
    print("l:load game other:new game")
    inp = input(">")
    if inp == "l":
        try:
            file = open("hsdata",'rb')
            game = pickle.load(file)
        except FileNotFoundError:
            print("I can not find save data thus start a new game")
            game.player_name = input("Type your name:")
    else:
        game.player_name = input("Type your name:")
    while game.is_game_run:
        game.game_state.description(game)
        inputed_string = input("Command:").lower().strip()
        game = game.game_state.command_execute(inputed_string, game)

if __name__ == '__main__':
    main()
