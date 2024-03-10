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
    font = pygame.font.SysFont('arial', 20)
    gameover_font = pygame.font.SysFont('bold', 30)
    hit_txt = font.render('Hit', 1, black)
    stand_txt = font.render('Stand', 1, black)
    restart_txt = font.render('Restart', 1, black)
    gameover_txt = gameover_font.render('GAME OVER', 1, black)
    #display background and hit/stand buttons
    hit_b = pygame.draw.rect(background, (gray), (360, 600, 80, 30))
    stand_b = pygame.draw.rect(background, (gray), (460, 600, 80, 30))
    screen.blit(background, (0, 0))
    pygame.display.update()

    #initialize game and starting vars:
    game_end = False
    stand = False
    win_count = 0
    lose_count = 0

    game = Blackjack()
    for card in game.deck:
        card.image = card.load_image()
    game.start_game()
    player_value = (game.get_value(game.player_hand))
    player_val_txt = font.render(f'Player Value: {player_value}', 1, black)
    dealer_value = (game.get_value(game.dealer_hand))
    dealer_val_txt = font.render(f'Dealer Value: {dealer_value}', 1, white)

    #main game loop
    while True:
        #always keep track of player and dealer value
        player_value = (game.get_value(game.player_hand))
        dealer_value = (game.get_value(game.dealer_hand))
        #immediately end game if player value > 21
        game_end = True if (player_value > 21) else False
        #display number of wins and losses in the session
        win_count_txt = font.render(f'Wins: {win_count}', 1, black)
        lose_count_txt = font.render(f'Losses: {lose_count}', 1, black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not (game_end or stand) and hit_b.collidepoint(pygame.mouse.get_pos()):
                game.player_hand.append(game.deal_card())
                player_value = game.get_value(game.player_hand)
                if player_value > 21:
                    game_end = True
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_end and stand_b.collidepoint(pygame.mouse.get_pos()):
                stand = True
                while dealer_value < 17:
                    game.dealer_hand.append(game.deal_card())
                    dealer_value = game.get_value(game.dealer_hand)
            elif event.type == pygame.MOUSEBUTTONDOWN and (game_end or stand) and restart_b.collidepoint(pygame.mouse.get_pos()):
                if player_value == dealer_value:
                    pass
                elif player_value <= 21 and player_value > dealer_value or dealer_value > 21:
                    win_count += 1
                else:
                    lose_count += 1
                #reset game
                game_end = False
                stand = False
                game = Blackjack()
                for card in game.deck:
                    card.image = card.load_image()
                game.start_game()
                player_value = (game.get_value(game.player_hand))
                dealer_value = (game.get_value(game.dealer_hand))
                #color over restart box
                restart_b = pygame.Rect(0, 255, 75, 75)
                restart_b_x = (screen_width - restart_b.width) // 2
                restart_b = pygame.draw.rect(background, background_color, (restart_b_x, 340, 75, 25))

        #continuously display background and necessary text
        screen.blit(background, (0, 0))
        player_val_txt = font.render(f'Player Value: {player_value}', 1, black)
        screen.blit(player_val_txt, ((screen_width - player_val_txt.get_width()) // 2, 560))
        screen.blit(hit_txt, (390, 604))
        screen.blit(stand_txt, (480, 604))
        screen.blit(win_count_txt, ((screen_width - win_count_txt.get_width()) // 4, (450)))
        screen.blit(lose_count_txt, ((screen_width - lose_count_txt.get_width()) // 4, 470))
        #continously display player's hand
        for card in game.player_hand:
            x = (screen_width // 2 - card.image.get_width()) + game.player_hand.index(card) * 100
            screen.blit(card.image, (x, 400))
        #displays only the first card of dealer's hand
        starting_x = game.dealer_hand[0].image.get_width()
        screen.blit(game.dealer_hand[0].image, ((screen_width // 2 - starting_x, 100)))
        screen.blit(cardback, (screen_width // 2 - starting_x + 100, 100))
        #checks if player input is done
        if game_end or stand:
            gameover_x = (screen_width - gameover_txt.get_width()) // 2
            screen.blit(gameover_txt, (gameover_x, 300))

            restart_txt_x = (screen_width - restart_txt.get_width()) // 2
            screen.blit(restart_txt, (restart_txt_x, 340))
            
            restart_b = pygame.Rect(0, 255, 75, 75)
            restart_b_x = (screen_width - restart_b.width) // 2
            restart_b = pygame.draw.rect(background, gray, (restart_b_x, 340, 75, 25))
            for card in game.dealer_hand:
                x = (screen_width // 2 - card.image.get_width()) + game.dealer_hand.index(card) * 100
                screen.blit(card.image, (x, 100))
            #display dealer value at the end
            dealer_val_txt = font.render(f'Dealer Value: {dealer_value}', 1, black)
            screen.blit(dealer_val_txt, ((screen_width - dealer_val_txt.get_width()) // 2, 260))
        pygame.display.update()
            
if __name__ == '__main__':
    main()