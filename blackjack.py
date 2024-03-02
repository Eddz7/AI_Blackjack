import pygame
from pygame.locals import *
import random

# Initialize pygame
pygame.init()
# Set display dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

icon = pygame.image.load('resources/icon.png')
pygame.display.set_icon(icon)
cardback = pygame.image.load('resources/cards/cardback.png')

# Define Card class
class Card:
    def __init__(self, name):
        self.name = name

    def load_image(self):
        return pygame.image.load(f'resources/cards/{self.name}.png')

    @staticmethod
    def generate_deck():
        card_names = ['ad', 'ac', 'ah', 'as', '2d', '2c', '2h', '2s',
                      '3d', '3c', '3h', '3s', '4d', '4c', '4h', '4s', '5d', '5c', '5h',
                      '5s', '6d', '6c', '6h', '6s', '7d', '7c', '7h', '7s', '8d', '8c',
                      '8h', '8s', '9d', '9c', '9h', '9s', '10d', '10c', '10h', '10s',
                      'jd', 'jc', 'jh', 'js', 'qd', 'qc', 'qh', 'qs', 'kd', 'kc', 'kh', 'ks']
        deck = [Card(name) for name in card_names]
        return deck

# Load card images
deck = Card.generate_deck()
for card in deck:
    card.image = card.load_image()

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
