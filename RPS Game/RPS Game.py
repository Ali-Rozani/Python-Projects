import random

def rps_game():
    possible_actions = ["rock", "paper", "scissors"]
    print("Welcome to Rock, Paper, Scissors!")
    
    while True:
        # Ask the user for their input
        user = input("Enter a choice (rock, paper, scissors) or 'quit' to exit: ").lower()

        # Exit condition
        if user == "quit":
            print("Thanks for playing! Goodbye!")
            break
        
        # Input validation
        if user not in possible_actions:
            print("Invalid input. Please choose 'rock', 'paper', or 'scissors'.")
            continue

        # Computer makes its choice
        computer = random.choice(possible_actions)
        print(f"You chose {user}, computer chose {computer}.")
        
        # Determine the result
        if user == computer:
            print(f"Both players selected {user}. It's a tie!")
        elif (user == "rock" and computer == "scissors") or \
             (user == "paper" and computer == "rock") or \
             (user == "scissors" and computer == "paper"):
            print("You win!")
        else:
            print("You lose!")

        print("\n--- Play again or type 'quit' to exit ---")

rps_game()