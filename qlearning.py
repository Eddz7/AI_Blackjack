import numpy as np
import random
from blackjack import Card, Blackjack

class CustomCard(Card):
    def get_value(self):
        # This tries to convert the entire string except for the suit to an int
        if self.name[:-1].isnumeric():
            return int(self.name[:-1])
        elif self.name[0] in ['j', 'q', 'k']:
            return 10
        elif self.name[0] == 'a':
            return 11
    
    def generate_deck():
        numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
        suits = ['c', 'd', 'h', 's']
        deck = [CustomCard(f'{number}{suit}') for number in numbers for suit in suits]
        random.shuffle(deck)
        return deck

class CustomBlackjack(Blackjack):
    def __init__(self):
        self.deck = CustomCard.generate_deck()

    def player_action(self, action):
        if action == "hit":
            self.player_hand.append(self.deal_card())
        return self.get_value(self.player_hand)

    def dealer_action(self, output=True):
        while self.get_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deal_card())
            if output:
                print("Dealer hits and has:", [card.name for card in self.dealer_hand], self.get_value(self.dealer_hand))

    def game_result(self):
        self.dealer_action(output=False)
        player_value = self.get_value(self.player_hand)
        dealer_value = self.get_value(self.dealer_hand)
        if player_value > 21:
            return "loss"
        elif dealer_value > 21 or player_value > dealer_value:
            return "win"
        elif player_value == dealer_value:
            return "draw"
        else:
            return "loss"

class BlackjackQLearning:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        # alpha: increase = faster learning but potentially unstable, decrease = slower learning but potentially more stable
        # gamma: increase = prioritizes long-term rewards, more far-sighted decision-making, decrease = prioritizes immediate rewards, more near=sighted
        # epsilon: increase = more exploration, discovering new strategies, decrease = more exploitation of known strategies

        # Initialize Q-table with small random values
        # Player sum, dealer card, usable ace, action
        self.Q = np.random.random((32, 12, 2, 2))

    def choose_action(self, player_sum, dealer_card, usable_ace):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(["hit", "stay"])
        else:
            action_values = self.Q[player_sum, dealer_card, usable_ace]
            action_idx = np.argmax([self.Q[player_sum, dealer_card, usable_ace, 0], self.Q[player_sum, dealer_card, usable_ace, 1]])
            # decides whether to hit or stay based on the max q value 
            return "hit" if action_idx == 0 else "stay"

    #Q-learning algorithm
    def update(self, player_sum, dealer_card, usable_ace, action, reward, new_player_sum, new_dealer_card, new_usable_ace):
        # Determine the index of the action (hit: 0, stay: 1)
        action_idx = 0 if action == "hit" else 1
        # Retrieve the current Q-value for the chosen action
        old_value = self.Q[player_sum, dealer_card, usable_ace, action_idx]
        # Calculate the maximum Q-value for the next state
        future_max = np.max(self.Q[new_player_sum, new_dealer_card, new_usable_ace])
        # Update the Q-value using the Q-learning formula
        updated_value = old_value + self.alpha * (reward + self.gamma * future_max - old_value)
        # Update the Q-table with the new Q-value
        self.Q[player_sum, dealer_card, usable_ace, action_idx] = updated_value


    @staticmethod
    def has_usable_ace(hand):
        blackjack = CustomBlackjack()
        value = blackjack.get_value(hand)
        return True if (value <= 21 and "a" in card[0] for card in hand) else False

    def train(self, episodes):
        one_percent = round(episodes / 100)
        for ep in range(episodes):
            game = CustomBlackjack()
            game.start_game()
            if ep % one_percent == 0:
                progress = (ep/episodes) * 100
                print(f"Training progress: {progress:.2f}%")

            dealer_card = game.dealer_hand[0].get_value()
            status = "continue"
            while status == "continue":
                player_sum = game.get_value(game.player_hand)
                usable_ace = self.has_usable_ace(game.player_hand)
                action = self.choose_action(player_sum, dealer_card, usable_ace)
                status = game.player_action(action)
                new_player_sum = game.get_value(game.player_hand)
                new_usable_ace = self.has_usable_ace(game.player_hand)

            final_result = game.game_result()
            final_reward = 1 if final_result == "win" else (-1 if final_result == "loss" else 0)
            self.update(player_sum, dealer_card, usable_ace, action, final_reward, new_player_sum, dealer_card, new_usable_ace)

    def play(self):
        game = CustomBlackjack()
        game.start_game()
        print("Dealer shows:", [game.dealer_hand[0].name])
        print("Player hand:", [card.name for card in game.player_hand], game.get_value(game.player_hand))
        status = "continue"
        while status == "continue":
            player_sum = game.get_value(game.player_hand)
            usable_ace = self.has_usable_ace(game.player_hand)
            dealer_card = game.dealer_hand[0].get_value()
            action_idx = np.argmax(self.Q[player_sum, dealer_card, usable_ace])
            action = "hit" if action_idx == 0 else "stay"
            status = game.player_action(action)
            if action == "stay":
                break
            print("Player hand:", [card.name for card in game.player_hand], game.get_value(game.player_hand))

        if status == "continue":
            print("Dealer has:", [card.name for card in game.dealer_hand], game.get_value(game.dealer_hand))
            game.dealer_action()
        final_result = game.game_result()
        return final_result

# Train the agent
agent = BlackjackQLearning()
agent.train(1000000)
test_games = 100000
wins = 0
losses = 0
draws = 0

for _ in range(test_games):
    print("-----")
    result = agent.play()
    print(result)
    if result == "win":
        wins += 1
    elif result == "loss":
        losses += 1
    else:
        draws += 1
print(f"Wins: {wins}, Losses: {losses}, Draws: {draws}")
print(f"Win rate: {wins/(wins + losses)*100:.2f}%")
