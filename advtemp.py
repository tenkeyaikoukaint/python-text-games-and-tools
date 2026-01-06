"""Python simplest adventure game(logic test)"""

acceptable_verbs = ["look", "search", "get", "open"]

class GameObject:

    def look(self):
        raise NotImplementedError

    def get(self, game):
        if is_on_place(game, self):
            if self.align == "not movable":
                print("Too heavy to carry.")
            else:
                game.place.objects.remove(self)
                game.inventory.objects.append(self)
                print("Taken.")

    def open(self, game):
        print("You can not open it.")

    def search(self, game):
        print("You found nothing.")

    def get_place(self, game):
        return game.position_query(self)

class MailBox(GameObject):

    def __init__(self):
        self.state = "closed"
        self.align = "not movable"

    def name(self):
        return "mailbox"

    def look(self):
        print("An old fashioned mailbox.")

    def search(self, game):
        if is_visible(game, game.key):
            print("There is nothing more.")
        else:
            print("You found a key.")
            appear(game, game.key)

class Door(GameObject):

    def __init__(self):
        self.state = "locked"
        self.align = "not movable"

    def name(self):
        return "door"

    def look(self):
        print("a normal door.")
        if self.state == "locked":
            print("It is locked.")
        else:
            print("It is opened.")

    def open(self, game):
        if self.state == "locked":
            if is_possess(game, game.key):
                print("The door is unlocked.")
                self.state = "open"
            else:
                print("You do not have any kind of keys.")
        else:
            print("The door is already unlocked.")

class Key(GameObject):

    def __init__(self):
        self.align = "movable"

    def name(self):
        return "key"

    def look(self):
        print("A pretty golden key.")

class Shelf(GameObject):

    def name(self):
        return "shelf"

    def look(self):
        pass

class Picture(GameObject):

    def name(self):
        return "picture"

    def look(self):
        pass

class Crowbar(GameObject):

    def look(self):
        pass

class Lid(GameObject):

    def look(self):
         pass

class Disk(GameObject):

    def look(self):
        pass


class Place:

    def description(self):
        pass

    def look(self, game):
        self.description()
        for i in self.objects:
            print(f"There is a {i.name()}.")

class HouseFront(Place):

    def __init__(self, game):
        self.objects = [game.mailbox, game.door]
        self.hidden_objects = [game.key]

    def description(self):
        print("You are in front of the house.")

    def north(self, game):
        if game.door.state == "locked":
            print("the door is locked.")
            return game.place
        else:
            print("You go north.")
            return game.entrance

class Entrance(Place):

    def __init__(self, game):
        self.objects = [game.shelf, game.picture]
        self.hidden_object = [game.crowbar, game.lid, game.disk]

    def description(self):
        print("You are at the entrance of the house.")



class Inventory(Place):

    def __init__(self, game):
        self.objects = []

class Game:

    def __init__(self):

        self.is_run = True

        self.door = Door()
        self.mailbox = MailBox()
        self.picture = Picture()
        self.shelf = Shelf()
        self.lid = Lid()
        self.key = Key()
        self.crowbar = Crowbar()
        self.disk = Disk()

        self.inventory = Inventory(self)
        self.housefront = HouseFront(self)
        self.entrance = Entrance(self)

        self.scenes = [self.housefront, self.entrance]
        self.place = self.housefront

    def position_query(self, object):
        scene = None
        for i in self.scenes:
            for j in i.objects:
                if j == object:
                    scene = i
        return scene

def is_visible(game, object):
    if object.get_place(game) in [game.place, game.inventory]:
        return True
    else:
        return False

def is_possess(game, object):
    if object in game.inventory.objects:
        return True
    else:
        return False

def is_on_place(game, object):
    if object in game.place.objects:
        return True
    else:
        return False

def appear(game, object):
    game.place.hidden_objects.remove(object)
    game.place.objects.append(object)

def description(game):
    game.place.description()

def parse(stmt):
     sliced_stmt = stmt.split()
     if len(sliced_stmt) > 1:
         return sliced_stmt[0], sliced_stmt[1]
     elif len(sliced_stmt) == 1:
         return sliced_stmt[0], None
     else:
         return  None, None

def command_execute(command, game):
    verb, noun = parse(command)
    if verb in acceptable_verbs:
        if noun == None:
            if verb == "look":
                game.place.look(game)
            elif verb == "inventory":
                if game.inventory.objects == []:
                   print("You have nothing.")
                else:
                    print("You have :")
                    for i in game.inventory.objects:
                        print(i.name())
            elif verb == "north":
                game.place = game.place.north(game)

        else:
            visible_objects = game.place.objects + game.inventory.objects
            is_find_object = False
            for i in visible_objects:
                if noun == i.name():
                    is_find_object = True
                    if verb == "look":
                        i.look()
                    elif verb == "get":
                        i.get(game)
                    elif verb == "open":
                        i.open(game)
                    elif verb == "search":
                        i.search(game)
            if not is_find_object:
                print(f"You can not find any {noun} here.")
    else:
        print("I do not understand what you want to do.")

game = Game()
while game.is_run:
    game.place.description()
    command = input("Enter command please : ")
    command_execute(command, game)
