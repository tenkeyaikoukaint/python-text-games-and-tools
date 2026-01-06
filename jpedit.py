import sys
from jpedlib2 import jel



COMMAND_MODE = 0
EDIT_MODE = 1

class LineEditor:

    def __init__(self):
        self.mode = COMMAND_MODE
        self.document = []
        self.line_number = 0
        self.is_line_number_visible = True

    def edit_mode(self):
        self.mode = EDIT_MODE
        while self.mode == EDIT_MODE:
            self.line_number += 1
            inp = input(f"{self.line_number}:")
            if inp == ".":
                self.mode = COMMAND_MODE
            else:
                self.document.insert(self.line_number - 1, inp)
                print(self.ed.tojp(inp))         


    def show_commands(self):
        print("l ([start line number], [end line number]) : display list")
        print("i ([address]) : insert(edit)")
        print("d ([start line number], [end line number]) : delete line(s)")
        print("n : line number display on/off")
        print("r [file name] : read file")
        print("w [file name] : write file")
        print("q : quit editor")
        print("params inside paren can omited")

    def list(self, command):
        if len(command) == 1:
            for i, n in enumerate(self.document):
                if self.is_line_number_visible:
                    print(f"{i+1}:{self.ed.tojp(n)}")
                else:
                    print(n)
        elif len(command) == 2:
            if command[1].isnumeric():
                i = int(command[1])
                if i >= 1 and i <= len(self.document):
                    print(f"{i}:{self.document[i - 1]}")
                else:
                    print("Index Out of Range")
            else:
                print("Illeagal Parameter")
        elif len(command) == 3:
            if command[1].isnumeric() and command[2].isnumeric():
                if int(command[1]) > 0 and int(command[2]) > 0:
                    try:
                       for i in range(int(command[1]), int(command[2])+1):
                           print(f"{i}:{self.ed.tojp(self.document[i - 1])}")
                    except IndexError:
                        print("Index Out of Range")
                else:
                    print("Index Out of Range")
            else:
                print("Illeagal Parameter")
        else:
            print("Too Many Parameters")

    def show_line_number(self):
        if self.is_line_number_visible == True:
            self.is_line_number_visible = False
        else:
            self.is_line_number_visible = True

    def insert(self, command):
        if len(command) == 1:
            self.edit_mode()
        elif len(command) == 2:
            self.line_number = len(self.document)
            self.line_number = int(command[1]) - 1
            self.edit_mode()

    def delete(self, command):
        if len(command) == 2:
            if command[1].isnumeric():
                if int(command[1]) <= len(self.document) and \
                   int(command[1]) > 0:
                    del(self.document[int(command[1]) - 1])
                else:
                    print("Index Out of Range")
            else:
                print("Illeagal Parameter")
        if len(command) == 3:
            if command[1].isnumeric() and command[2].isnumeric():
                if int(command[1]) > 0 and int(command[2]) > 0 and \
                   int(command[1]) <= len(self.document) and \
                   int(command[2]) <= len(self.document) and \
                   command[1] <= command[2]:
                    for i in range(int(command[1]), int(command[2])+1):
                        del(self.document[int(command[1]) - 1])
                else:
                    print("Index Out of Range")
            else:
                print("Illeagal Parameter")

    def read(self, command):
        filename = command[1]
        file = open(filename,'r')
        self.document = file.readlines()
        for i in range(0, len(self.document)):
            self.document[i] = self.document[i].rstrip()
        file.close()

    def write(self, command):
        filename = command[1]
        file = open(filename, 'w')
        for n in self.document:
            file.write(f"{self.ed.tojp(n)}\n")
        file.close()

    def quit(self):
        sys.exit()

    def main(self):
        self.ed = jel()
        while True:
            command = input("> ").replace(","," ").split()
            if command[0] == "i":
                self.insert(command)
            elif command[0] == "l":
                self.list(command)
            elif command[0] == "n":
                self.show_line_number()
            elif command[0] == "q":
                self.quit()
            elif command[0] == "w":
                self.write(command)
            elif command[0] == "d":
                self.delete(command)
            elif command[0] == "r":
                self.read(command)
            else:
                self.show_commands()

if __name__ == '__main__':
    editor = LineEditor()
    editor.main()
