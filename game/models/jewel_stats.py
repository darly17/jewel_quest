import pygame
from typing import List, Dict

WHITE = (255, 255, 255)


class JewelStats:
    def __init__(self, jewels_config: List[Dict], x: int, y: int):
        self.jewels_config = jewels_config
        self.x = x
        self.y = y
        self.width = 150
        self.height = 250
        self.stats = {jewel['id']: 0 for jewel in jewels_config}
        self.font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 22, bold=True)

    def add_jewel(self, jewel_type: int):
        if jewel_type in self.stats:
            self.stats[jewel_type] += 1

    def reset(self):
        self.stats = {jewel['id']: 0 for jewel in self.jewels_config}

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (40, 40, 60), (self.x, self.y,
                         self.width, self.height), border_radius=10)
        pygame.draw.rect(screen, (70, 70, 90), (self.x, self.y,
                         self.width, self.height), 2, border_radius=10)
        title = self.title_font.render("Collected", True, WHITE)
        screen.blit(
            title, (self.x + (self.width - title.get_width()) // 2, self.y + 15))
        pygame.draw.line(screen, (100, 100, 120), (self.x + 10,
                         self.y + 45), (self.x + self.width - 10, self.y + 45), 2)
        y_offset = self.y + 60
        for jewel_type, count in sorted(self.stats.items()):
            if jewel_type < len(self.jewels_config):
                config = self.jewels_config[jewel_type]
                jewel_img = pygame.Surface((25, 25), pygame.SRCALPHA)
                color_map = {
                    'red': (255, 50, 50),
                    'blue': (50, 50, 255),
                    'green': (50, 255, 50),
                    'yellow': (255, 255, 50),
                    'purple': (180, 50, 255)
                }
                color = color_map.get(config['color'].lower(), (255, 255, 255))
                pygame.draw.rect(
                    jewel_img, color, (0, 0, 25, 25), border_radius=5)
                pygame.draw.rect(jewel_img, (220, 220, 220),
                                 (0, 0, 25, 25), 2, border_radius=5)
                screen.blit(jewel_img, (self.x + 15, y_offset))
                name_text = self.font.render(config['color'], True, WHITE)
                count_text = self.font.render(
                    f"×{count}", True, (200, 200, 255))
                screen.blit(name_text, (self.x + 50, y_offset + 3))
                screen.blit(
                    count_text, (self.x + self.width - 40, y_offset + 3))
                y_offset += 35