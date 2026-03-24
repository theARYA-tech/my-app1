
print("You are in an adventure game")

name=input("what is your name, player?: ")
choice=input(" You are in a forest. Go left or right: ")

if choice == "left":
    action = input(" Do you swim across or walk along the river? ")

    if action == "swim":
        print(name, " A crocodile appears! Game over.")
    elif action == "walk":
        print(name, " You find a hidden treasure!")
elif choice == "right":
    action = input("You meet a wooden bridge on fire. Do you run across or get an extinguisher?: ")
    if action == "run":
        print(name, " You are dead, half way across, due to total bridge collapse")
    elif choice == "extinguisher":
        print (name, " Yaay, you made it across withiut any prize")    

else:
    print (name, " Pick a SIDE!!!!")