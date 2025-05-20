import pygame
from .base import BackgroundState
from ..constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE



class HelpState(BackgroundState):
    def __init__(self, game):
        super().__init__(game, 'help')
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 24)
        self.font_small = pygame.font.SysFont('Arial', 18)
        self.help_text = [
            "Jewel Quest Game Instructions",
            "",
            "Game Modes:",
            "- Time Attack: Reach the target score before time runs out",
            "- Score Challenge: Reach the target score as quickly as possible",
            "",
            "How to Play:",
            "1. Click on a jewel to select it",
            "2. Click on an adjacent jewel to swap them",
            "3. Match 3 or more jewels of the same type to clear them",
            "4. Longer matches give more points",
            "",
            "Jewel Types:",
            "- Each jewel type has different point values",
            "- Some jewels have special effects when matched",
            "",
            "Good luck and have fun!"
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                from .menu_state import MenuState
                self.game.set_state(MenuState(self.game))

    def update(self, dt):
        pass

    def draw(self, screen):
        self.draw_background(screen)
        title = self.font_large.render("Help", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 70))
        for i, line in enumerate(self.help_text):
            if i == 0:
                text = self.font_medium.render(line, True, WHITE)
                screen.blit(
                    text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))
            else:
                text = self.font_small.render(line, True, WHITE)
                screen.blit(text, (50, 90 + i * 30))
        back_text = self.font_small.render(
            "Press ESC to return to menu", True, WHITE)
        screen.blit(
            back_text,
            (SCREEN_WIDTH //
             1.45 -
             back_text.get_width() //
             2,
             SCREEN_HEIGHT - 50))