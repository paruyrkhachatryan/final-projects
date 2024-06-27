"""
Memory Game using Pygame.

This module implements a simple memory game where the player flips cards to find matching pairs.
"""

import random
import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRID_SIZE = (4, 4)
CARD_SIZE = (100, 100)
MARGIN = 10

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Memory Game')
clock = pygame.time.Clock()

class Card:
    """Represents a card in the memory game."""
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.is_up = False
        self.can_flip = True

    def draw(self, surface):
        """Draws the card on the given surface."""
        if not self.is_up:
            pygame.draw.rect(surface, RED, self.rect)
        else:
            surface.blit(self.image, self.rect)

    def flip(self):
        """Flips the card."""
        if self.can_flip:
            self.is_up = not self.is_up

    def disable(self):
        """Disables the card from being flipped."""
        self.can_flip = False

def generate_cards(images):
    """Generates a list of Card objects with shuffled positions."""
    cards = []
    start_x = (SCREEN_WIDTH - (GRID_SIZE[0] * (CARD_SIZE[0] + MARGIN) - MARGIN)) // 2
    start_y = (SCREEN_HEIGHT - (GRID_SIZE[1] * (CARD_SIZE[1] + MARGIN) - MARGIN)) // 2
    positions = [(start_x + x * (CARD_SIZE[0] + MARGIN), start_y + y * (CARD_SIZE[1] + MARGIN))
                 for x in range(GRID_SIZE[0]) for y in range(GRID_SIZE[1])]
    random.shuffle(positions)
    for i, img in enumerate(images * 2):
        pos = positions[i]
        cards.append(Card(img, pos))
    return cards

def check_match(cards):
    """Checks if there is a match among flipped cards."""
    flipped_cards = [card for card in cards if card.is_up and card.can_flip]
    if len(flipped_cards) == 2:
        if flipped_cards[0].image == flipped_cards[1].image:
            for card in flipped_cards:
                card.disable()
            return True
        return False
    return None

def reset_flipped_cards(cards):
    """Resets the flipped cards that do not match."""
    for card in cards:
        if card.is_up and card.can_flip:
            card.flip()

def main():
    """Main function for the Memory Game."""
    card_images = [pygame.image.load(f'C:/Users/khach/git/final-projects/Pymemory/images/card{i}.png').convert()
                   for i in range(1, 9)]

    cards = generate_cards(card_images)
    flipped_cards = []
    running = True

    while running:
        running = handle_events(cards, flipped_cards, running)
        screen.fill(WHITE)
        for card in cards:
            card.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def handle_events(cards, flipped_cards, running):
    """Handle events in the game loop."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_button_down_event(event, cards, flipped_cards)
    return running

def handle_mouse_button_down_event(event, cards, flipped_cards):
    """Handle mouse button down events."""
    mouse_pos = pygame.mouse.get_pos()
    for card in cards:
        if card.rect.collidepoint(mouse_pos) and card.can_flip:
            card.flip()
            flipped_cards.append(card)
            if len(flipped_cards) == 2:
                pygame.time.wait(500)
                if not check_match(flipped_cards):
                    reset_flipped_cards(flipped_cards)
                flipped_cards.clear()

if __name__ == '__main__':
    main()
