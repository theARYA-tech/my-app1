while True:

 import random
 choices = ["rock", "paper", "scissors"]
 player = input("choose rock, paper, scissors: ")
 computer = random.choice(choices)
 print ("computer choose: ", computer )
 if player == "paper" and computer == "rock":
  print("You win!!!")
 if player == "scissors" and computer == "paper":
   print("You win!!!")
 if player == computer:
   print("TIE")  
 else:
   print ("You LOSE")  
  
 again = input("Do another? (yes/no): ")
 if again.lower() != "yes":
    break