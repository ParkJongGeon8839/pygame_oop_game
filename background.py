import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800  # 700 → 800으로 증가

class Background:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, surface):
        surface.blit(self.image, (0, 0))