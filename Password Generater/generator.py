import random

print("Welcome To Your Password Generator!\n")
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!$%&*().,/';[]=_0123456789"

number = int(input("Amount of passwords to generate: "))
length = int(input("Enter your password length: "))

print("\nHere are your passwords:")
for _ in range(number):
    print("".join(random.choice(chars) for _ in range(length)))