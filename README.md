# Blackjack Game and Q-Learning Agent

This repository contains two files, `blackjack.py` and `qlearning.py`, implementing the game of blackjack and a Q-learning agent to play the game.

## Files

1. **blackjack.py**: This script simulates the game of blackjack using the Pygame library. The file allows a player to interactively play blackjack against an automated dealer. It includes functionalities for dealing cards, calculating hand values, player actions (hit or stand), win and loss monitoring, and determining game outcomes.

2. **qlearning.py**: This script implements a Q-learning agent that learns to play blackjack optimally through reinforcement learning. The agent utilizes an ε-greedy strategy for action selection during training and updates the Q-table based on rewards obtained during gameplay. It is trained over a specified number of sessions to make decisions based on maximizing expected rewards.

## How to Use

To run the blackjack game, simply execute the `blackjack.py` script. Ensure you have Pygame installed (`pip install pygame`) to run the game successfully.

To train and test the Q-learning agent, run the `qlearning.py` script. The agent will be trained over a specified number of sessions (default: 50,000), after which it will play a specified number of games to evaluate its performance.

