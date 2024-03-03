import pygame
from pygame.locals import *
import random

# Initialize pygame
pygame.init()
# Set display dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

icon = pygame.image.load('resources/icon.png')
cardback = pygame.image.load('resources/cards/cardback.png')
pygame.display.set_icon(icon)

# Define Card class
class Card:
    def __init__(self, name):
        self.name = name
        self.value = self.get_value()

    def get_value(self):
        # this tries to convert the entire string except for the suit to an int
        if self.name[:-1].isnumeric():
            return int(self.name[:-1])
        elif self.name[0] in ['j', 'q', 'k']:
            return 10
        # future implementation: use a boolean to check if hand has an ace and total value > 21, then subtract 10
        elif self.name[0] == 'a':
            return 11
        else:
            raise ValueError("Invalid card name")

    def load_image(self):
        return pygame.image.load(f'resources/cards/{self.name}.png')

    @staticmethod
    def generate_deck():
        numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
        suits = ['c', 'd', 'h', 's']
        deck = [Card(f'{number}{suit}') for number in numbers for suit in suits]
        random.shuffle(deck)
        return deck

# Load card images
deck = Card.generate_deck()

for card in deck:
    card.image = card.load_image()

total = 0
for i in range(len(deck)):
    total += deck[i].get_value()
print(total)
# Display first card image
first_card_image = deck[0].image
screen.blit(first_card_image, (screen_width//2 - first_card_image.get_width()//2, screen_height//2 - first_card_image.get_height()//2))
pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit pygame
pygame.quit()