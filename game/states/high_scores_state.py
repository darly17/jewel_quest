import pygame
import os
from .base import BackgroundState
from .menu_state import MenuState
from ..utils.config_loader import ConfigLoader

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)


class HighScoresState(BackgroundState):
    def __init__(self, game):
        super().__init__(game, 'scores')
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 36)
        self.font_small = pygame.font.SysFont('Arial', 24)
        self.high_scores = ConfigLoader.load_high_scores("high_scores.xml")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.set_state(MenuState(self.game))

    def update(self, dt):
        pass

    def draw(self, screen):
        self.draw_background(screen)
        title = self.font_large.render("High Scores", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        if not self.high_scores:
            no_scores = self.font_medium.render(
                "No high scores yet!", True, WHITE)
            screen.blit(
                no_scores,
                (SCREEN_WIDTH //
                 2 -
                 no_scores.get_width() //
                 2,
                 150))
        else:
            for i, score in enumerate(self.high_scores[:10]):
                score_text = self.font_medium.render(
                    f"{
                        i +
                        1}. {
                        score['name']}: {
                        score['points']} ({
                        score['level']}, {
                        score['mode']})",
                    True, WHITE
                )
                screen.blit(
                    score_text,
                    (SCREEN_WIDTH //
                     2 -
                     score_text.get_width() //
                     2,
                     150 +
                     i *
                     40))
        back_text = self.font_small.render(
            "Press ESC to return to menu", True, WHITE)
        screen.blit(
            back_text,
            (SCREEN_WIDTH //
             2 -
             back_text.get_width() //
             2,
             SCREEN_HEIGHT - 50))