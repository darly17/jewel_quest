import pygame
from .base import BackgroundState
from ..constants import *


class MenuState(BackgroundState):
    def __init__(self, game):
        super().__init__(game, "menu")
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 36)
        self.selected_option = 0
        self.mode_selection = False
        self.mode_options = [
            {"text": "Time Attack", "mode": TIME_ATTACK},
            {"text": "Score Challenge", "mode": SCORE_CHALLENGE},
            {"text": "Back", "action": self.back_to_main}
        ]
        self.mode_selected_option = 0
        self.options = [
            {"text": "Start Game", "action": self.show_mode_selection},
            {"text": "High Scores", "action": self.show_high_scores},
            {"text": "Help", "action": self.show_help},
            {"text": "Exit", "action": self.exit_game}
        ]

    

    def show_mode_selection(self):
        self.mode_selection = True

    def back_to_main(self):
        self.mode_selection = False

    def start_game(self, mode: str):
        from .playing_state import PlayingState
        self.game.set_state(PlayingState(self.game, mode, 1))

    def show_high_scores(self):
        from .high_scores_state import HighScoresState
        self.game.set_state(HighScoresState(self.game))

    def show_help(self):
        from .help_state import HelpState
        self.game.set_state(HelpState(self.game))

    def exit_game(self):
        self.game.running = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.mode_selection:
                    if event.key == pygame.K_DOWN:
                        self.mode_selected_option = (
                            self.mode_selected_option + 1) % len(self.mode_options)
                    elif event.key == pygame.K_UP:
                        self.mode_selected_option = (
                            self.mode_selected_option - 1) % len(self.mode_options)
                    elif event.key == pygame.K_RETURN:
                        option = self.mode_options[self.mode_selected_option]
                        if "action" in option:
                            option["action"]()
                        else:
                            self.start_game(option["mode"])
                    elif event.key == pygame.K_ESCAPE:
                        self.back_to_main()
                else:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (
                            self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (
                            self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.options[self.selected_option]["action"]()
                    elif event.key == pygame.K_ESCAPE:
                        self.exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if self.mode_selection:
                    for i, option in enumerate(self.mode_options):
                        option_rect = pygame.Rect(
                            SCREEN_WIDTH // 2 - 150, 300 + i * 60, 300, 50)
                        if option_rect.collidepoint(mouse_pos):
                            self.mode_selected_option = i
                            if "action" in option:
                                option["action"]()
                            else:
                                self.start_game(option["mode"])
                            break
                else:
                    for i, option in enumerate(self.options):
                        option_rect = pygame.Rect(
                            SCREEN_WIDTH // 2 - 150, 300 + i * 60, 300, 50)
                        if option_rect.collidepoint(mouse_pos):
                            self.selected_option = i
                            option["action"]()
                            break

    def update(self, dt):
        pass

    def draw(self, screen):
        self.draw_background(screen)

        if self.mode_selection:
            title = self.font_large.render("Select Game Mode", True, WHITE)
            screen.blit(
                title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

            for i, option in enumerate(self.mode_options):
                button_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - 180, 300 + i * 70, 360, 60)

                if i == self.mode_selected_option:
                    color = (80, 120, 200)
                    border_color = (120, 160, 220)
                else:
                    color = (60, 80, 120)
                    border_color = (90, 110, 150)

                pygame.draw.rect(
                    screen, (30, 30, 50), button_rect.inflate(
                        10, 10), border_radius=10)
                pygame.draw.rect(screen, color, button_rect, border_radius=8)
                pygame.draw.rect(
                    screen,
                    border_color,
                    button_rect,
                    3,
                    border_radius=8)

                text = self.font_medium.render(option["text"], True, WHITE)
                text_rect = text.get_rect(center=button_rect.center)
                screen.blit(text, text_rect)
        else:
            title = self.font_large.render("Jewel Quest", True, WHITE)
            title_shadow = self.font_large.render(
                "Jewel Quest", True, (50, 50, 80))
            screen.blit(
                title_shadow,
                (SCREEN_WIDTH //
                 2 -
                 title.get_width() //
                 2 +
                 3,
                 153))
            screen.blit(
                title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

            for i, option in enumerate(self.options):
                button_rect = pygame.Rect(
                    SCREEN_WIDTH // 2 - 200, 280 + i * 80, 400, 70)

                if i == self.selected_option:
                    for y_offset in range(button_rect.height):
                        alpha = 200 - \
                            int(150 * (y_offset / button_rect.height))
                        color = (80 + y_offset, 140 + y_offset, 220)
                        pygame.draw.line(screen, color,
                                         (button_rect.x, button_rect.y + y_offset),
                                         (button_rect.x + button_rect.width, button_rect.y + y_offset))
                else:
                    for y_offset in range(button_rect.height):
                        alpha = 150 - \
                            int(100 * (y_offset / button_rect.height))
                        color = (50 + y_offset, 80 + y_offset, 120)
                        pygame.draw.line(screen, color,
                                         (button_rect.x, button_rect.y + y_offset),
                                         (button_rect.x + button_rect.width, button_rect.y + y_offset))

                border_color = (
                    120, 180, 255) if i == self.selected_option else (
                    80, 120, 180)
                pygame.draw.rect(
                    screen,
                    border_color,
                    button_rect,
                    3,
                    border_radius=10)

                text = self.font_medium.render(option["text"], True, WHITE)
                text_shadow = self.font_medium.render(
                    option["text"], True, (0, 0, 0, 100))
                text_rect = text.get_rect(center=button_rect.center)
                screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
                screen.blit(text, text_rect)

                if i == self.selected_option:
                    pygame.draw.polygon(screen, (255, 255, 255),
                                        [(button_rect.x + 20, button_rect.centery),
                                        (button_rect.x + 35,
                                         button_rect.centery + 15),
                                        (button_rect.x + 35, button_rect.centery - 15)])