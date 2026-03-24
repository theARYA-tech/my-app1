import random

num_passwords = int(input("how many passwords do you want to generate?: "))
length = int(input("How long should the password be? "))
characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

include_numbers= input ("Would you like numbers included? (y/n): ")
include_symbols= input ("Would you like to include symbols? (y/n): ")

if include_numbers == "y":
    characters+= "0123456789"

if include_symbols == "y":
    characters+= "!@#$%^&*"    



for i in range(num_passwords):
    password = " "

    for j in range(length):
       password += random.choice(characters)

    print("Your password is:", i + 1, ":", password)