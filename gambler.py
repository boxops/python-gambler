# Challenge: Write a program that use a red and black roulette gambling strategy to make profit
# The purpose of this program is to simulate the success and failure of real life gambling scenarios
import random
import json
import time

records_file = "records.json"
with open(records_file, "r") as rd:
    read_file = json.load(rd)
    budget_at_start = read_file["budget"]

# Only adjust these variables
# ------------------------------
# Change budget in records.json
bet_on = "black"
bet_at_start = 1
max_lose_streak = 13  # 2^13 = 8192
games = 100
sleep = 1
stop_after_games = 10000
# budget_at_start = 100
# ------------------------------

budget = budget_at_start
highest_budget = 0
bet = bet_at_start
win_streak = 0
highest_win_streak = 0
lose_streak = 0
highest_lose_streak = 0
highest_lose_streak_multiplier = 0
games_played = 0
wins = 0
losses = 0

while True:
    for game in range(games):
        # Step 1: Generate random values that will return either red or black
        roulette = ["red", "black"]
        outcome = random.choice(roulette)
        # Step 2: Create a logic that handles the outcome using a gambling rule
        # Scenario 1: bet 1 on red, if the choice is red and the outcome is red, then repeat the process
        if outcome is bet_on:
            wins = wins + 1
            budget = budget + bet
            bet = bet_at_start
            win_streak = win_streak + 1
            lose_streak = 0
            if win_streak > highest_win_streak:
                highest_win_streak = win_streak
        # Scenario 2: bet 1 on red, if the choice is black, then double the next bet and repeat
        elif outcome is not bet_on:
            losses = losses + 1
            budget = budget - bet
            if budget < 0:
                with open(records_file, "w") as wr:
                    data = {"budget": budget}
                    json.dump(data, wr)
                print(f"\n---------[ End of Game ]---------\nMy budget is: {budget}")
                print(f"Add budget in {records_file} file \nand start again.")
                print("-" * 33)
                exit(0)
            bet = bet * 2
            lose_streak = lose_streak + 1
            win_streak = 0
            if lose_streak > highest_lose_streak:
                highest_lose_streak = lose_streak
            if lose_streak >= max_lose_streak:
                bet = bet_at_start
                lose_streak = 0
                highest_lose_streak_multiplier = highest_lose_streak_multiplier + 1
        else:
            print("Something went wrong")

        if budget > highest_budget:
            highest_budget = budget

        games_played = games_played + 1

    print("-" * 33)
    print(f"\nMinimum bet: {bet_at_start}")
    print(f"Original budget: {budget_at_start}")
    print(f"Played games: {games_played}")
    print(f"\nWins to Losses: {wins} / {losses}")
    print(f"Win to Loss rate: {round((wins / games_played * 100), 2)}% / {round((losses / games_played * 100), 2)}%")
    print(f"Current budget is: {budget}")
    profit = budget - budget_at_start
    print(f"Profit: +{profit}") if profit > 0 else print(f"Profit: {profit}")
    print(f"\nHighest earning: {highest_budget}")
    print(f"Highest earning multiplier: x{round(highest_budget / budget_at_start, 3)}")
    print(f"Highest win streak: {highest_win_streak}")
    print(f"Highest lose streak: {highest_lose_streak}")
    print(f"Highest lose streak multiplier: {highest_lose_streak_multiplier}")

    with open(records_file, "w") as wr:
        data = {"budget": budget}
        json.dump(data, wr)

    stop_after_games = stop_after_games - games
    if stop_after_games <= 0:
        print("\n --[ Stopping game to prevent buffer errors ]--")
        exit(0)

    time.sleep(sleep)
