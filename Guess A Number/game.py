import random

def guess_number(x):
  random.number = random.randint(1, x)
  guess = 0
  while guess != random.number:
    guess = (input(f'Guess a number between 1 and {x}: '))
    if guess.isdigit():
      guess = int(guess)
    else:
      print('Please type a number.')
      continue
    print(guess)
    if guess < random.number:
      print('Sorry, guess again. Too low.')
    elif guess > random.number:
      print('Sorry, guess again. Too high.')

  print(f'Yay, congrats. You have guessed the number {random.number} correctly!')


guess_number(35)