
import pygame
import random


# Инициализация Pygame
pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Memory Game')

# Часы для управления частотой обновления экрана
clock = pygame.time.Clock()

# Игровой механизм
grid_size = (4, 4)  # Размер сетки для карточек (4x4)
card_size = (100, 100)  # Размер одной карточки
margin = 10  # Отступ между карточками




class Card:
    def __init__(self, image, pos):
        self.image = image  # Изображение карточки
        self.rect = self.image.get_rect(topleft=pos)  # Прямоугольник карточки
        self.is_up = False  # Переменная для состояния карточки (перевернута ли она лицевой стороной)
        self.can_flip = True  # Можно ли перевернуть карточку

    def draw(self, surface):
        if not self.is_up:
            pygame.draw.rect(surface, RED, self.rect)  # Рисуем обратную сторону карточки
        else:
            surface.blit(self.image, self.rect)  # Рисуем лицевую сторону карточки

    def flip(self):
        if self.can_flip:
            self.is_up = not self.is_up

    def disable(self):
        self.can_flip = False




# Генерация карточек
def generate_cards(images):
    cards = []
    # Новые вычисления позиций
    start_x = (SCREEN_WIDTH - (grid_size[0] * (card_size[0] + margin) - margin)) // 2
    start_y = (SCREEN_HEIGHT - (grid_size[1] * (card_size[1] + margin) - margin)) // 2
    positions = [(start_x + x * (card_size[0] + margin), start_y + y * (card_size[1] + margin))
                 for x in range(grid_size[0]) for y in range(grid_size[1])]
    random.shuffle(positions)
    for i, img in enumerate(images * 2):
        pos = positions[i]
        card = Card(img, pos)
        cards.append(card)
    return cards

def check_match(cards):
    flipped_cards = [card for card in cards if card.is_up and card.can_flip]
    if len(flipped_cards) == 2:
        if flipped_cards[0].image == flipped_cards[1].image:
            for card in flipped_cards:
                card.disable()
            return True
        else:
            return False
    return None

def reset_flipped_cards(cards):
    for card in cards:
        if card.is_up and card.can_flip:
            card.flip()


def main():
    # Загрузка изображений для карточек
    card_images = [
        pygame.image.load('C:/Users/khach/git/final-projects/Pymemory/images/card1.png').convert(),
        pygame.image.load('C:/Users/khach/git/final-projects/Pymemory/images/card2.png').convert(),
        pygame.image.load('C:/Users/khach/git/final-projects/Pymemory/images/card3.png').convert(),
        pygame.image.load('C:/Users/khach/git/final-projects/Pymemory/images/card4.png').convert(),
        pygame.image.load('C:/Users/khach/git/final-projects/Pymemory/images/card5.png').convert(),
        pygame.image.load('C:/Users/khach/git/final-projects/Pymemory/images/card6.png').convert(),
        pygame.image.load('C:/Users/khach/git/final-projects/Pymemory/images/card7.png').convert(),
        pygame.image.load('C:/Users/khach/git/final-projects/Pymemory/images/card8.png').convert()
    ]

    cards = generate_cards(card_images)
    flipped_cards = []
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for card in cards:
                    if card.rect.collidepoint(mouse_pos) and card.can_flip:
                        card.flip()
                        flipped_cards.append(card)
                        if len(flipped_cards) == 2:
                            pygame.time.wait(500)  # Задержка, чтобы игрок мог увидеть карточки
                            if not check_match(flipped_cards):
                                reset_flipped_cards(flipped_cards)
                            flipped_cards = []

        screen.fill(WHITE)


        for card in cards:
            card.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # Ограничение на 60 кадров в секунду

    pygame.quit()

if __name__ == '__main__':
    main()


