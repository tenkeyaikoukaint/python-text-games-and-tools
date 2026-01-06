import random

qlist = [
            [
             "Where is the capital city of France?",
             "Paris",
             "Rome",
             "london",
             1
            ],
            [
             "Where is the capital city of Japan?",
             "London",
             "Tokyo",
             "Rome",
             2
            ]
        ]

qnum = random.randint(0, len(qlist) - 1)
print(qlist[qnum][0])
for i in range(1, 4):
    print(f"{i} : {qlist[qnum][i]}")
inp = int(input("> "))
if inp == qlist[qnum][4]:
    print("Correct!")
else:
    print("Wrong...")
