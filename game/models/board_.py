import pygame
import random
from typing import List, Dict, Tuple, Optional
from .jewel import Jewel
from .jewel_factory import JewelFactory
from ..utils.audio_manager import AudioManager
from ..constants import*

class Board:
    def __init__(self, width: int, height: int,
                 jewel_factory: JewelFactory, audio: AudioManager):
        self.width = width
        self.height = height
        self.jewel_factory = jewel_factory
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        self.selected_jewel = None
        self.animations = []
        self.fill_board(avoid_matches=True)
        self.audio = audio  
        self.is_moving = False
    def fill_board(self, avoid_matches=True):
        for y in range(self.height):
            for x in range(self.width):
               
                possible_types = list(range(self.jewel_factory.type_count))

                if avoid_matches:
                    
                    if x >= 2:
                        left1 = self.grid[y][x -
                                             1].type if self.grid[y][x -
                                                                     1] else None
                        left2 = self.grid[y][x -
                                             2].type if self.grid[y][x -
                                                                     2] else None
                        if left1 == left2 and left1 in possible_types:
                            possible_types.remove(left1)

                    if y >= 2:
                        up1 = self.grid[y -
                                        1][x].type if self.grid[y -
                                                                1][x] else None
                        up2 = self.grid[y -
                                        2][x].type if self.grid[y -
                                                                2][x] else None
                        if up1 == up2 and up1 in possible_types:
                            possible_types.remove(up1)

                jewel_type = random.choice(possible_types)
                self.grid[y][x] = self.jewel_factory.create_jewel(
                    jewel_type, x, y)

    def get_jewel_at(self, x: int, y: int) -> Optional[Jewel]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def is_valid_swap(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        
        if not self.get_jewel_at(x1, y1) or not self.get_jewel_at(x2, y2):
            return False

        self.grid[y1][x1], self.grid[y2][x2] = self.grid[y2][x2], self.grid[y1][x1]

      
        has_matches = False

        for y, x in [(y1, x1), (y2, x2)]:
            
            if not self.grid[y][x]:
                continue

            
            left = x
            while left > 0 and self.grid[y][left -
                                            1] and self.grid[y][left - 1].type == self.grid[y][x].type:
                left -= 1

            
            right = x
            while right < self.width - \
                    1 and self.grid[y][right + 1] and self.grid[y][right + 1].type == self.grid[y][x].type:
                right += 1

           
            if right - left + 1 >= 3:
                has_matches = True
                break

        
        if not has_matches:
            for y, x in [(y1, x1), (y2, x2)]:
                if not self.grid[y][x]:
                    continue

                
                up = y
                while up > 0 and self.grid[up - 1][x] and self.grid[up -
                                                                    1][x].type == self.grid[y][x].type:
                    up -= 1

                
                down = y
                while down < self.height - \
                        1 and self.grid[down + 1][x] and self.grid[down + 1][x].type == self.grid[y][x].type:
                    down += 1

               
                if down - up + 1 >= 3:
                    has_matches = True
                    break

        
        self.grid[y1][x1], self.grid[y2][x2] = self.grid[y2][x2], self.grid[y1][x1]

        return has_matches

    def swap_jewels(self, x1: int, y1: int, x2: int, y2: int) -> bool:
       
        if not self.is_valid_swap(x1, y1, x2, y2):
            
            return False

        jewel1 = self.get_jewel_at(x1, y1)
        jewel2 = self.get_jewel_at(x2, y2)

        if jewel1 and jewel2:
            
            self.grid[y1][x1], self.grid[y2][x2] = self.grid[y2][x2], self.grid[y1][x1]

            jewel1.x, jewel1.y = x2, y2
            jewel2.x, jewel2.y = x1, y1

            jewel1.move_to(x2, y2)
            jewel2.move_to(x1, y1)
            self.audio.play_sound('swap_success')  
            return True

        return False

    
    def select_jewel(self, x: int, y: int) -> Tuple[bool, Optional[Tuple[int, int]]]:
        jewel = self.get_jewel_at(x, y)
        if not jewel:
            return False, None
        self.audio.play_sound('select')
        if self.selected_jewel:
            if self.selected_jewel.x == x and self.selected_jewel.y == y:
                
                self.selected_jewel.selected = False
                self.selected_jewel.scale = 1.0
                self.selected_jewel = None
                return True, None

            if ((abs(self.selected_jewel.x - x) == 1 and self.selected_jewel.y == y) or
                    (abs(self.selected_jewel.y - y) == 1 and self.selected_jewel.x == x)):
                if self.is_valid_swap(self.selected_jewel.x, self.selected_jewel.y, x, y):
                    
                    self.selected_jewel.selected = False
                    self.selected_jewel.scale = 1.0
                    self.swap_jewels(self.selected_jewel.x, self.selected_jewel.y, x, y)
                    self.selected_jewel = None
                    return True, None
                else:
        
                    invalid_pos = (self.selected_jewel.x, self.selected_jewel.y)
                    self.selected_jewel.selected = False
                    self.selected_jewel.shake_animation()  
                    jewel.shake_animation()  
                    self.selected_jewel = None
                    return False, invalid_pos
            else:
                
                self.selected_jewel.selected = False
                self.selected_jewel.scale = 1.0
                self.selected_jewel = jewel
                jewel.selected = True
                jewel.scale = 1.1 
                return True, None
        else:
            
            self.selected_jewel = jewel
            jewel.selected = True
            jewel.scale = 1.1
            return True, None
    
    def deselect_jewel(self):
        if self.selected_jewel:
            self.selected_jewel.selected = False
            self.selected_jewel = None

    def find_matches(self) -> List[List[Tuple[int, int]]]:
        matches = []

   
        for y in range(self.height):
            x = 0
            while x < self.width - 2:
                jewel = self.grid[y][x]
                if jewel:
                    match_length = 1
                    while x + \
                            match_length < self.width and self.grid[y][x + match_length] and self.grid[y][x + match_length].type == jewel.type:
                        match_length += 1

                    if match_length >= 3:
                        matches.append([(x + i, y)
                                       for i in range(match_length)])
                        x += match_length
                        continue
                x += 1

       
        for x in range(self.width):
            y = 0
            while y < self.height - 2:
                jewel = self.grid[y][x]
                if jewel:
                    match_length = 1
                    while y + \
                            match_length < self.height and self.grid[y + match_length][x] and self.grid[y + match_length][x].type == jewel.type:
                        match_length += 1

                    if match_length >= 3:
                        matches.append([(x, y + i)
                                       for i in range(match_length)])
                        y += match_length
                        continue
                y += 1

        return matches

    def remove_matches(
            self, matches: List[List[Tuple[int, int]]]) -> Tuple[int, Dict]:
        points = 0
        jewels_to_remove = set()
        jewel_types_collected = {}
        
        
        for match in matches:
            for x, y in match:
                if (x, y) not in jewels_to_remove:
                    jewels_to_remove.add((x, y))
                    jewel_type = self.grid[y][x].type
                    jewel_types_collected[jewel_type] = jewel_types_collected.get(jewel_type, 0) + 1
        
        
        for x, y in list(jewels_to_remove):
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in jewels_to_remove:
                    jewel = self.grid[ny][nx]
                    if jewel:
                       
                        jewel.shake_animation()
        
 
        for x, y in jewels_to_remove:
            self.grid[y][x].start_destroy_animation()
            self.animations.append(self.grid[y][x])
            points += self.grid[y][x].points
            self.grid[y][x] = None
        
        return points, jewel_types_collected

    def collapse_columns(self):
        for x in range(self.width):
            empty_spaces = []
            for y in range(self.height - 1, -1, -1):
                if self.grid[y][x] is None:
                    empty_spaces.append(y)
                elif empty_spaces:
                    lowest_empty = empty_spaces.pop(0)
                    self.grid[lowest_empty][x] = self.grid[y][x]
                    self.grid[y][x] = None
                    self.grid[lowest_empty][x].move_to(x, lowest_empty)
                    empty_spaces.append(y)

    def refill_board(self):
        column_delay = 0.3
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] is None:
                    new_jewel = self.jewel_factory.create_random_jewel(x, y)
                    new_jewel.screen_y = GRID_OFFSET_Y - CELL_SIZE
                    new_jewel.move_to(x, y)
                    self.grid[y][x] = new_jewel

    def update(self, dt: float):
        self.is_moving = any(jewel.animating for row in self.grid for jewel in row if jewel)
        for row in self.grid:
            for jewel in row:
                if jewel:
                    jewel.update(dt)

        self.animations = [
            anim for anim in self.animations if not anim.is_destroy_animation_done()]

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, BACKGROUND_COLOR,
                         (GRID_OFFSET_X - 5, GRID_OFFSET_Y - 5,
                          GRID_SIZE * CELL_SIZE + 10, GRID_SIZE * CELL_SIZE + 10))

        for x in range(GRID_SIZE + 1):
            pygame.draw.line(screen, GRAY,
                             (GRID_OFFSET_X + x * CELL_SIZE, GRID_OFFSET_Y),
                             (GRID_OFFSET_X + x * CELL_SIZE, GRID_OFFSET_Y + GRID_SIZE * CELL_SIZE), 2)

        for y in range(GRID_SIZE + 1):
            pygame.draw.line(screen, GRAY,
                             (GRID_OFFSET_X, GRID_OFFSET_Y + y * CELL_SIZE),
                             (GRID_OFFSET_X + GRID_SIZE * CELL_SIZE, GRID_OFFSET_Y + y * CELL_SIZE), 2)

        for row in self.grid:
            for jewel in row:
                if jewel:
                    jewel.draw(screen)

        for animation in self.animations:
            animation.draw(screen)


