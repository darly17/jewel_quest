import time
import os
from .constants import *
import pygame
import xml.etree.ElementTree as ET

from .states.menu_state import MenuState

from .utils.config_loader import ConfigLoader
from .utils.audio_manager import AudioManager


class JewelQuestGame:
    def __init__(self):

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jewel Quest")
        self.clock = pygame.time.Clock()
        self.running = True
        self.backgrounds = self._load_backgrounds()
        self.levels_config = ConfigLoader.load_levels_config("levels.xml")
        self.jewels_config = ConfigLoader.load_jewels_config("jewels.xml")
        from .models.jewel_factory import JewelFactory
        self.jewel_factory = JewelFactory(self.jewels_config)
        self.audio = AudioManager()
        self.audio.play_music()
        self.state = None

    def _load_backgrounds(self) -> dict[str, pygame.Surface]:
        try:
            return {
                'menu': pygame.image.load('assets/backgrounds/menu_bg.jpg').convert(),
                'game': pygame.image.load('assets/backgrounds/game_bg.jpg').convert(),
                'help': pygame.image.load('assets/backgrounds/help_bg.jpg').convert(),
                'scores': pygame.image.load('assets/backgrounds/scores_bg.jpg').convert()
            }
        except Exception:
            default = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            default.fill(BACKGROUND_COLOR)
            return {
                'menu': default.copy(),
                'game': default.copy(),
                'help': default.copy(),
                'scores': default.copy()
            }

    def set_state(self, new_state):
        self.state = new_state

    def is_high_score(self, score):
        if not os.path.exists("high_scores.xml"):
            root = ET.Element('high_scores')
            tree = ET.ElementTree(root)
            tree.write("high_scores.xml")

        try:
            self.scores = ConfigLoader.load_high_scores("high_scores.xml")
        except Exception:
            self.scores = []
        is_high_score = False

        if not self.scores:
            is_high_score = True
        elif score > int(self.scores[0]['points']):
            is_high_score = True

        if not is_high_score:
            is_high_score = False
        return is_high_score

    def save_high_score(self, mode: str, level: int,
                        score: int, time_left=0, player_name=None):

        if mode != TIME_ATTACK:
            return

        new_record = {
            'name': player_name,
            'points': str(score),
            'level': f"Level: {level}",
            'mode': "Time Attack",
            'date': time.strftime("%Y-%m-%d")
        }

        self.scores.insert(0, new_record)

        self.scores.sort(key=lambda x: int(x['points']), reverse=True)
        self.scores = self.scores[:10]

        ConfigLoader.save_high_scores("high_scores.xml", self.scores)

    def run(self):
        last_time = time.time()
        while self.running:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            dt = min(dt, 0.1)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.state.handle_events(events)
            self.state.update(dt)
            self.state.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)
