from abc import ABC, abstractmethod
from ..constants import *
import pygame
from typing import List

class GameState(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_events(self, events: List):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

class BackgroundState(GameState):
    def __init__(self, game, bg_key: str):
        super().__init__(game)
        self.bg_key = bg_key
        self.bg_image = self.game.backgrounds.get(bg_key)

    def draw_background(self, screen):
        from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT
        scaled_bg = pygame.transform.scale(
            self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))
        
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))