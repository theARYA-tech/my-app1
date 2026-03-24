import random

secret_number = random.randint(1, 10)
attempts = 3

for i in range(attempts):
 guess = int(input("Guess a number between 1 and 10: "))

 if guess < secret_number:
    print( "too low.")
 elif guess > secret_number:
    print("Too high!")
 else:
    print("Yaaay!")
    break
    
 print("attempts left:", attempts - i - 1)   

print("!!! The number Is:", secret_number)