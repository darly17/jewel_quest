import pygame
import time
import random
from typing import List, Tuple, Optional
from .base import BackgroundState
from .menu_state import MenuState
from ..models.board import Board
from ..models.jewel_stats import JewelStats
from ..models.jewel_factory import JewelFactory

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 8
CELL_SIZE = 60
WHITE = (255, 255, 255)
TIME_ATTACK = "time"
SCORE_CHALLENGE = "score"

class LevelManager:
   
    def __init__(self, game, mode: str, level: int):
        self.game = game
        self.mode = mode
        self.level = level
        self.level_config = self.game.levels_config[level - 1]
        self.time_left = self.level_config['time_limit'] if mode == TIME_ATTACK else 0
        self.target_score = self.level_config['target_score']
        self.start_time = time.time()
        self.avoid_matches = True
    
    def update_time(self):
        if self.mode == TIME_ATTACK:
            elapsed = time.time() - self.start_time
            self.time_left = max(0, self.level_config['time_limit'] - int(elapsed))
            return self.time_left > 0
        return True
    
    def check_level_complete(self, score: int) -> bool:
        if self.mode == SCORE_CHALLENGE and score >= self.target_score:
            return True
        return False
    
    def load_board_config(self, board: Board):
       
        if not self.level_config.get('board'):
            return
        
        config_board = self.level_config['board']
        for y in range(min(len(config_board), board.height)):
            for x in range(min(len(config_board[y]), board.width)):
                jewel_type = config_board[y][x]
                if 0 <= jewel_type < len(self.game.jewels_config):
                    board.grid_manager.grid[y][x] = self.game.jewel_factory.create_jewel(jewel_type, x, y)
        
        self.fix_initial_matches(board)
    
    def fix_initial_matches(self, board: Board):
        
        matches = board.find_matches()
        attempts = 0
        max_attempts = 100

        while matches and attempts < max_attempts:
            for match in matches:
                for x, y in match:
                    bad_type = board.grid_manager.grid[y][x].type
                    possible_types = [t for t in range(self.game.jewel_factory.type_count) if t != bad_type]
                    new_type = random.choice(possible_types)
                    board.grid_manager.grid[y][x] = self.game.jewel_factory.create_jewel(new_type, x, y)

            matches = board.find_matches()
            attempts += 1

        if attempts >= max_attempts:
            print("Warning: Could not completely eliminate initial matches")

class GameUI:
    
    def __init__(self, game):
        self.game = game
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 36)
        self.font_small = pygame.font.SysFont('Arial', 24)
        self.timer_blink_state = False
        self.last_blink_time = time.time()
    
    def draw_game_info(self, screen: pygame.Surface, mode: str, score: int, time_left: int, target_score: int):
       
        score_text = self.font_medium.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        if mode == TIME_ATTACK:
            timer_color = WHITE
            if time_left <= 5:
                if self.timer_blink_state:
                    timer_color = (255, 50, 50)
                else:
                    timer_color = (255, 180, 180)
            
            time_text = self.font_medium.render(f"Time: {time_left}", True, timer_color)
            time_shadow = self.font_medium.render(f"Time: {time_left}", True, (0, 0, 0))
            screen.blit(time_shadow, (SCREEN_WIDTH - 150 + 2, 22))
            screen.blit(time_text, (SCREEN_WIDTH - 150, 20))
        else:
            target_text = self.font_small.render(f"Target: {target_score}", True, WHITE)
            screen.blit(target_text, (SCREEN_WIDTH - 150, 60))
    
    def draw_message(self, screen: pygame.Surface, title: str, subtitle: str):
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        title_text = self.font_medium.render(title, True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        subtitle_text = self.font_small.render(subtitle, True, WHITE)
        screen.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
    
    def draw_no_moves_message(self, screen: pygame.Surface):
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        message = self.font_large.render("No possible moves!", True, WHITE)
        restart = self.font_medium.render("Press R to restart", True, WHITE)
        
        screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
    
    def update_blink_state(self, time_left: int):
        
        if time_left <= 5:
            current_time = time.time()
            if current_time - self.last_blink_time > 0.25:
                self.timer_blink_state = not self.timer_blink_state
                self.last_blink_time = current_time
                if self.timer_blink_state:
                    self.game.audio.play_sound('select')
        else:
            self.timer_blink_state = False
 
class PlayingState(BackgroundState):
    def __init__(self, game, mode: str, level: int, score: int = 0):
        super().__init__(game, "game")
        self.mode = mode
        self.level = level
        self.score = score
        self.no_moves = False
        self.no_moves_message_time = 0
        self.game_over = False
        self.level_complete = False
        self.goal_achieved = False
        self.start_time = time.time()
        self.invalid_move_animation = False
        self.invalid_move_time = 0
        self.invalid_move_positions = []
        
        self.level_manager = LevelManager(game, mode, level)
        self.ui = GameUI(game)
        
       
        stats_x, stats_y = 10, SCREEN_HEIGHT - 300
        self.jewel_stats = JewelStats(self.game.jewels_config, stats_x, stats_y)
        
        global GRID_OFFSET_X, GRID_OFFSET_Y
        GRID_OFFSET_X = (SCREEN_WIDTH - GRID_SIZE * CELL_SIZE) // 2 + 30
        GRID_OFFSET_Y = 100 - 10
        
        self.board = Board(GRID_SIZE, GRID_SIZE, self.game.jewel_factory, self.game.audio)
        
        
        self.level_manager.load_board_config(self.board)
        if not self.level_manager.level_config.get('board'):
            self.board.fill_board(self.level_manager.avoid_matches)
        
        self.level_manager.fix_initial_matches(self.board)

    def reshuffle_board(self):
        
        jewels = [jewel for row in self.board.grid_manager.grid for jewel in row if jewel]
        random.shuffle(jewels)

        index = 0
        for y in range(self.board.height):
            for x in range(self.board.width):
                if index < len(jewels):
                    jewels[index].move_to(x, y)
                    self.board.grid_manager.grid[y][x] = jewels[index]
                    index += 1
                else:
                    self.board.grid_manager.grid[y][x] = None

        if not self.board.match_finder.has_possible_moves():
            self.board.fill_board(avoid_matches=True)

    def update(self, dt):
        if self.game_over or self.level_complete or self.goal_achieved:
            return

       
        if not self.board.match_finder.has_possible_moves():
            if not self.no_moves:
                self.no_moves = True
                self.no_moves_message_time = time.time()
                self.reshuffle_board()
            elif time.time() - self.no_moves_message_time > 2.0:
                self.no_moves = False

    
        if self.mode == TIME_ATTACK:
            if not self.level_manager.update_time():
                self.game_over = True
                if self.game.is_high_score(self.score):
                    from .name_input_state import NameInputState
                    self.game.set_state(NameInputState(self.game, self.mode, self.level, self.score,self.level_manager.time_left))
            
            self.ui.update_blink_state(self.level_manager.time_left)

     
        if self.mode == SCORE_CHALLENGE and self.score >= self.level_manager.target_score:
            self.level_complete = True
            self.goal_achieved = True

        
        self.board.update(dt)
        
        if not self.board.is_moving:
            matches = self.board.find_matches()
            if matches:
                points, collected_jewels = self.board.remove_matches(matches)
                self.score += points
                for jewel_type, count in collected_jewels.items():
                    for _ in range(count):
                        self.jewel_stats.add_jewel(jewel_type)
                self.board.grid_manager.collapse_columns()
                self.board.grid_manager.refill_board()
                if not any(jewel.animating for row in self.board.grid_manager.grid for jewel in row if jewel):
                    if self.score >= self.target_score and self.mode == SCORE_CHALLENGE:
                        self.level_complete = True
                    
    def draw(self, screen: pygame.Surface):
        self.draw_background(screen)
        
        self.ui.draw_game_info(
            screen, 
            self.mode, 
            self.score, 
            self.level_manager.time_left, 
            self.level_manager.target_score
        )
        
       
        self.board.draw(screen)
        self.jewel_stats.draw(screen)
        
       
        if self.invalid_move_animation:
            current_time = time.time()
            elapsed = current_time - self.invalid_move_time
            if elapsed < 0.5:
                alpha = int(255 * (1 - elapsed / 0.5))
                for pos in self.invalid_move_positions:
                    if pos:
                        x, y = pos
                        overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                        overlay.fill((255, 0, 0, alpha))
                        screen.blit(overlay, (GRID_OFFSET_X + x * CELL_SIZE +5, GRID_OFFSET_Y + y * CELL_SIZE +5))
            else:
                self.invalid_move_animation = False
        
       
        if self.game_over:
            self.ui.draw_message(screen, "Game Over!", "Press Enter to continue")
        elif self.level_complete:
            if time.time() - self.start_time >= 1.0:
                if self.level < len(self.game.levels_config):
                    self.ui.draw_message(screen, "Level Complete!", "Press Enter for next level")
                else:
                    self.ui.draw_message(screen, "Game Complete!", "Press Enter to continue")
        elif self.goal_achieved:
            self.ui.draw_message(screen, "Goal Achieved!", f"Score: {self.score}")
        
        if self.no_moves:
            self.ui.draw_no_moves_message(screen)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.set_state(MenuState(self.game))
                elif event.key == pygame.K_r and self.no_moves:
                    self.__init__(self.game, self.mode, self.level, 0)
                    return
                elif event.key == pygame.K_RETURN and (self.goal_achieved or self.level_complete or self.game_over):
                    if self.level < len(self.game.levels_config):
                        self.game.set_state(PlayingState(self.game, self.mode, self.level + 1, 0))
                    else:
                        self.game.set_state(MenuState(self.game))
            
            if not self.game_over and not self.level_complete and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                grid_x = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
                grid_y = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE
                
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    success, invalid_pos = self.board.select_jewel(grid_x, grid_y)
                    if not success and invalid_pos:
                        self.invalid_move_animation = True
                        self.invalid_move_time = time.time()
                        self.invalid_move_positions = [invalid_pos, (grid_x, grid_y)]                    
                        
                        
                        
                        
                        