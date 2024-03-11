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
        player_value = self.get_value(self.player_hand)
        dealer_value = self.get_value(self.dealer_hand)
        if player_value > 21:
            return "loss"
        elif player_value > dealer_value or dealer_value > 21:
            return "win"
        elif player_value == dealer_value:
            return "draw"
        else:
            return "loss"
