import pygame
import time
import random
import math
from ..utils.game_object import GameObject
from typing import Dict, List

GRID_OFFSET_X = 200
GRID_OFFSET_Y = 100
CELL_SIZE = 60
HIGHLIGHT_COLOR = (200, 230, 255)


class Jewel(GameObject):
    def __init__(self, jewel_type: int, x: int, y: int, config: Dict):
        self.type = jewel_type
        self.x = x
        self.y = y
        self.screen_x = GRID_OFFSET_X + x * CELL_SIZE
        self.screen_y = GRID_OFFSET_Y + y * CELL_SIZE
        self.color = config['color']
        self.points = config['points']
        self.effect = config.get('effect')
        self.image = self._load_image(config['image'])
        self.selected = False
        self.alpha = 255
        self.scale = 1.0
        self.rotation = 0
        self.animation_start_time = 0
        self.animating = False
        self.target_x = self.screen_x
        self.target_y = self.screen_y
        self.animation_speed = 0.1
        self.set_animation_parameters()
        self.start_x = self.screen_x
        self.start_y = self.screen_y
        self.start_alpha = self.alpha
    def set_animation_parameters(self):
        color = self.color.lower()
        if color == 'red':
            self.fade_speed = 0.5
            self.scale_speed = 2.0
            self.rotation_speed = 0
            self.animation_duration = 0.5
        elif color == 'blue':
            self.fade_speed = 0.7
            self.scale_speed = -1.5
            self.rotation_speed = 0
            self.animation_duration = 0.5
        elif color == 'green':
            self.fade_speed = 0.6
            self.scale_speed = -1
            self.rotation_speed = 5
            self.animation_duration = 0.6
        elif color == 'yellow':
            self.fade_speed = 0.4
            self.scale_speed = 1.2
            self.rotation_speed = 15
            self.animation_duration = 0.4
        elif color == 'purple':
            self.fade_speed = 0.3
            self.scale_speed = 2.5
            self.rotation_speed = 0
            self.animation_duration = 0.7
        else:
            self.fade_speed = 0.5
            self.scale_speed = 1.0
            self.rotation_speed = 0
            self.animation_duration = 0.5

    def shake_animation(self):
        self.shake_start = time.time()
        self.shake_duration = 0.5
        self.original_x = self.screen_x
        self.original_y = self.screen_y

    def update(self, dt: float):
        if self.animating and not hasattr(self, 'shake_start'):
            elapsed = time.time() - self.animation_start_time
            progress = min(elapsed / self.animation_duration, 1.0)
            progress = progress * progress * (3 - 2 * progress)
            self.screen_x = self.start_x + (self.target_x - self.start_x) * progress
            self.screen_y = self.start_y + (self.target_y - self.start_y) * progress
            if progress >= 1.0:
                self.animating = False
                self.screen_x = self.target_x
                self.screen_y = self.target_y
        if hasattr(self, 'shake_start'):
            elapsed = time.time() - self.shake_start
            if elapsed < self.shake_duration:
                shake_amount = 5 * math.sin(elapsed * 30)
                self.screen_x = self.original_x + shake_amount
            else:
                self.screen_x = self.original_x
                del self.shake_start

    def _load_image(self, image_path: str) -> pygame.Surface:
        try:
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(
                image, (CELL_SIZE - 10, CELL_SIZE - 10))
        except pygame.error:
            surface = pygame.Surface(
                (CELL_SIZE - 10, CELL_SIZE - 10), pygame.SRCALPHA)
            color_map = {
                'red': (255, 0, 0),
                'blue': (0, 0, 255),
                'green': (0, 255, 0),
                'yellow': (255, 255, 0),
                'purple': (128, 0, 128)
            }
            color = color_map.get(self.color.lower(), (255, 255, 255))
            pygame.draw.rect(
                surface, color, (0, 0, CELL_SIZE - 10, CELL_SIZE - 10))
            pygame.draw.rect(surface, (255, 255, 255),
                             (0, 0, CELL_SIZE - 10, CELL_SIZE - 10), 2)
            return surface

    def draw(self, screen: pygame.Surface):
        if self.selected:
            highlight = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            highlight.fill((*HIGHLIGHT_COLOR[:3], 100))
            screen.blit(highlight, (self.screen_x - 5, self.screen_y - 5))
        scaled_image = pygame.transform.scale(self.image,
                                              (int((CELL_SIZE - 10) * self.scale),
                                               int((CELL_SIZE - 10) * self.scale)))
        if self.rotation != 0:
            scaled_image = pygame.transform.rotate(scaled_image, self.rotation)
        if self.alpha < 255:
            scaled_image.set_alpha(self.alpha)
        img_rect = scaled_image.get_rect(center=(self.screen_x + CELL_SIZE // 2,
                                                 self.screen_y + CELL_SIZE // 2))
        screen.blit(scaled_image,
                    (self.screen_x + (CELL_SIZE - 10 - scaled_image.get_width()) // 2,
                     self.screen_y + (CELL_SIZE - 10 - scaled_image.get_height()) // 2))

    def move_to(self, x: int, y: int):
        self.x = x
        self.y = y
        self.target_x = GRID_OFFSET_X + x * CELL_SIZE
        self.target_y = GRID_OFFSET_Y + y * CELL_SIZE
        self.animating = True
        self.animation_start_time = time.time()
        self.start_x = self.screen_x
        self.start_y = self.screen_y
        self.animation_duration = 0.5
        

    def start_destroy_animation(self):
        self.animation_start_time = time.time()
        self.animating = True
        self.start_scale = self.scale
        self.start_alpha = self.alpha
        self.animation_duration = 0.4

    def is_destroy_animation_done(self) -> bool:
        if not self.animating:
            return True
        current_time = time.time()
        elapsed = current_time - self.animation_start_time
        progress = min(elapsed / self.animation_duration, 1.0)
        self.alpha = int(self.start_alpha * (1 - progress))
        if self.scale_speed > 0:
            self.scale = 1.5 + progress * self.scale_speed
        else:
            self.scale = max(0.1, 1.5 + progress * self.scale_speed)
        self.rotation = (self.rotation + self.rotation_speed) % 360
        return progress >= 1.0
