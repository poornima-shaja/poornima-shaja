#stone paper sissor game in python

import random

def gamewin(comp,you):
    if comp == you:
        return None
    elif comp == 's':
        if you == 'z':
            return False
        elif you =='p':
            return True

    elif comp == 'z':
        if you == 'p':
            return False
        elif you =='s':
            return True  

    elif comp == 'p':
        if you == 's':
            return False
        elif you =='z':
            return True 

print("comp turn: stone(s) paper(p) or sissor(z)?")
randno = random.randint(1,3)
if randno == 1:
    comp = 's'
elif randno == 2:
    comp = 'z'
elif randno == 3:
    comp = 'p'

you= input("Your turn: stone(s)  paper(p) or sissor(z)?")
a= gamewin(comp,you)

print(f"Computer choose  {comp}") 
print(f"You choose  {you}")
if a == None:
    print("The game is a tie")
elif a :
        print("You win!!!")
else:
        print("You lose!!!")    