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
            #this tries to convert the entire string except for the suit to an int
            if card.name[:-1].isnumeric():
                value += int(card.name[:-1])
            elif card.name[0] in ['j', 'q', 'k']:
                value += 10
            elif card.name[0] == 'a':
                value += 11
                aces += 1
        #blackjack aces implementation
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

def main():
    #initialize pygame
    pygame.init()
    #set display dimensions
    screen_width, screen_height = 900, 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    #load icon and cardback images
    icon = pygame.image.load('resources/icon.png')
    cardback = pygame.image.load('resources/cards/cardback.png')
    pygame.display.set_caption('Blackjack')
    pygame.display.set_icon(icon)
    #initialize background
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (128,128,128)
    background_color = (134, 36, 42)
    background = pygame.Surface(screen.get_size())
    background.fill(background_color)
    #initialize buttons and text
    font = pygame.font.SysFont('arial', 15)
    hit_txt = font.render('Hit', 1, black)
    stand_txt = font.render('Stand', 1, black)
    restart_txt = font.render('Restart', 1, white)
    gameover_txt = font.render('GAME OVER', 1, (255,255,255))
    #display background and hit/stand buttons
    hit_b = pygame.draw.rect(background, (gray), (360, 450, 80, 30))
    stand_b = pygame.draw.rect(background, (gray), (460, 450, 80, 30))
    screen.blit(background, (0, 0))
    screen.blit(hit_txt, (392, 455))
    screen.blit(stand_txt, (484, 455))
    pygame.display.update()

    #main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

if __name__ == '__main__':
    main()