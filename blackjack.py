import pygame
import random

class Card:
    def __init__(self, name):
        self.name = name

    def load_image(self):
        return pygame.image.load(f'resources/cards/{self.name}.png')

    @staticmethod
    def generate_deck():
        numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
        suits = ['c', 'd', 'h', 's']
        deck = [Card(f'{number}{suit}') for number in numbers for suit in suits]
        random.shuffle(deck)
        return deck

class Blackjack:
    def __init__(self):
        self.deck = Card.generate_deck()
        self.player_hand = []
        self.dealer_hand = []

    def deal_card(self):
        return self.deck.pop()

    def start_game(self):
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]

    def get_value(self, hand):
        value = 0
        aces = 0
        for card in hand:
            # this tries to convert the entire string except for the suit to an int
            if card.name[:-1].isnumeric():
                value += int(card.name[:-1])
            elif card.name[0] in ['j', 'q', 'k']:
                value += 10
            elif card.name[0] == 'a':
                value += 11
                aces += 1
        # blackjack aces implementation
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

def main():
    pass

if __name__ == '__main__':
    main()