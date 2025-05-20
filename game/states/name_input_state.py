import pygame
from .base import GameState
from .menu_state import MenuState
from .playing_state import PlayingState

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (50, 50, 70)
WHITE = (255, 255, 255)
TIME_ATTACK = "time"


class NameInputState(GameState):
    def __init__(self, game, mode: str, level: int, score: int, time_left: int = 0):
        super().__init__(game)
        self.mode = mode
        self.level = level
        self.score = score
        self.time_left = time_left
        self.player_name = ""
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 36)
        self.font_small = pygame.font.SysFont('Arial', 24)
        self.active = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.player_name:
                    self.game.save_high_score(
                        self.mode,
                        self.level,
                        self.score,
                        self.time_left,
                        self.player_name
                        
                    )
                    if self.level < len(self.game.levels_config):
                        self.game.set_state(
                            PlayingState(
                                self.game,
                                self.mode,
                                self.level + 1,
                                0))
                    else:
                        self.game.set_state(MenuState(self.game))
                elif event.key == pygame.K_ESCAPE:
                    if self.level < len(self.game.levels_config):
                        self.game.set_state(
                            PlayingState(
                                self.game,
                                self.mode,
                                self.level + 1,
                                0))
                    else:
                        self.game.set_state(MenuState(self.game))
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.unicode.isalnum() and len(self.player_name) < 10:
                    self.player_name += event.unicode

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BACKGROUND_COLOR)
        title = self.font_large.render(
            "New High Score!", True, (100, 255, 100))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        score_text = self.font_medium.render(
            f"Score: {self.score}", True, WHITE)
        screen.blit(
            score_text,
            (SCREEN_WIDTH //
             2 -
             score_text.get_width() //
             2,
             220))
        if self.mode == TIME_ATTACK:
            time_text = self.font_medium.render(
                f"Time Left: {self.time_left}s", True, WHITE)
            screen.blit(
                time_text,
                (SCREEN_WIDTH //
                 2 -
                 time_text.get_width() //
                 2,
                 260))
        name_prompt = self.font_medium.render("Enter your name:", True, WHITE)
        screen.blit(
            name_prompt,
            (SCREEN_WIDTH //
             2 -
             name_prompt.get_width() //
             2,
             320))
        name_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 370, 300, 50)
        pygame.draw.rect(screen, (80, 80, 100), name_box, border_radius=5)
        pygame.draw.rect(
            screen,
            (100,
             100,
             120) if self.active else (
                70,
                70,
                90),
            name_box,
            2,
            border_radius=5)
        name_text = self.font_medium.render(self.player_name, True, WHITE)
        screen.blit(name_text, (name_box.x + 10, name_box.y + 10))
        confirm_text = self.font_medium.render(
            "Press ENTER to confirm", True, (200, 200, 255))
        screen.blit(confirm_text, (SCREEN_WIDTH // 2 -
                    confirm_text.get_width() // 2, 450))
        cancel_text = self.font_small.render(
            "Press ESC to cancel", True, (200, 150, 150))
        screen.blit(
            cancel_text,
            (SCREEN_WIDTH //
             2 -
             cancel_text.get_width() //
             2,
             500))