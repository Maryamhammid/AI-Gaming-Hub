
import pygame
import random
import json
import os


class Game2048AI:
    def __init__(self):
        self.depth = 3
    
    def expectimax(self, grid, depth, is_chance_node):
        if depth == 0:
            return self.evaluate_grid(grid)
        
        if is_chance_node:
            empty_cells = self.get_empty_cells(grid)
            if not empty_cells:
                return self.evaluate_grid(grid)
            
            expected_score = 0
            for row, col in empty_cells:
                for value, prob in [(2, 0.9), (4, 0.1)]:
                    new_grid = [row[:] for row in grid]
                    new_grid[row][col] = value
                    score = self.expectimax(new_grid, depth - 1, False)
                    expected_score += prob * score / len(empty_cells)
            
            return expected_score
        else:
            max_score = 0
            for move in ['left', 'right', 'up', 'down']:
                new_grid, moved = self.simulate_move(grid, move)
                if moved:
                    score = self.expectimax(new_grid, depth - 1, True)
                    max_score = max(max_score, score)
            
            return max_score
    
    def get_best_move(self, grid):
        best_score = -1
        best_move = None
        
        for move in ['left', 'right', 'up', 'down']:
            new_grid, moved = self.simulate_move(grid, move)
            if moved:
                score = self.expectimax(new_grid, self.depth, True)
                if score > best_score:
                    best_score = score
                    best_move = move
        
        return best_move
    
    def simulate_move(self, grid, direction):
        new_grid = [row[:] for row in grid]
        moved = False
        
        if direction == 'left':
            moved = self.move_left(new_grid)
        elif direction == 'right':
            moved = self.move_right(new_grid)
        elif direction == 'up':
            moved = self.move_up(new_grid)
        elif direction == 'down':
            moved = self.move_down(new_grid)
        
        return new_grid, moved
    
    def move_left(self, grid):
        moved = False
        for row in range(4):
            compressed = [val for val in grid[row] if val != 0]
            merged = []
            i = 0
            while i < len(compressed):
                if i < len(compressed) - 1 and compressed[i] == compressed[i + 1]:
                    merged.append(compressed[i] * 2)
                    i += 2
                else:
                    merged.append(compressed[i])
                    i += 1
            
            merged.extend([0] * (4 - len(merged)))
            
            if merged != grid[row]:
                moved = True
                grid[row] = merged
        
        return moved
    
    def move_right(self, grid):
        for row in grid:
            row.reverse()
        moved = self.move_left(grid)
        for row in grid:
            row.reverse()
        return moved
    
    def move_up(self, grid):
        self.transpose(grid)
        moved = self.move_left(grid)
        self.transpose(grid)
        return moved
    
    def move_down(self, grid):
        self.transpose(grid)
        moved = self.move_right(grid)
        self.transpose(grid)
        return moved
    
    def transpose(self, grid):
        for i in range(4):
            for j in range(i + 1, 4):
                grid[i][j], grid[j][i] = grid[j][i], grid[i][j]
    
    def get_empty_cells(self, grid):
        empty = []
        for row in range(4):
            for col in range(4):
                if grid[row][col] == 0:
                    empty.append((row, col))
        return empty
    
    def evaluate_grid(self, grid):
        score = 0
        
        # Empty cells bonus
        empty_cells = len(self.get_empty_cells(grid))
        score += empty_cells * 100
        
        # Max tile
        max_tile = max(max(row) for row in grid)
        score += max_tile * 2
        
        # Monotonicity
        score += self.monotonicity_score(grid) * 10
        
        return score
    
    def monotonicity_score(self, grid):
        score = 0
        
        # Check rows
        for row in grid:
            increasing = decreasing = 0
            for i in range(3):
                if row[i] <= row[i + 1]:
                    increasing += 1
                if row[i] >= row[i + 1]:
                    decreasing += 1
            score += max(increasing, decreasing)
        
        return score

class Game2048:
    def __init__(self, screen, colors):
        self.screen = screen
        self.colors = colors
        self.ai = Game2048AI()
        # self.reset_game()
        self.high_score = 0
        self.load_high_score()  # Load high score when game starts
        self.reset_game()
        # AI hint display variables
        self.show_hint = False
        self.hint_text = ""
        self.hint_timer = 0
        self.hint_duration = 180  # frames (3 seconds at 60 FPS)
    
    def load_high_score(self):
        """Load high score from a file"""
        try:
            if os.path.exists('2048_highscore.json'):
                with open('2048_highscore.json', 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
        except:
            # If there's any error, just keep high_score as 0
            self.high_score = 0

    def save_high_score(self):
        """Save high score to a file"""
        try:
            with open('highscore.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            # If saving fails, just ignore it
            pass



    def reset_game(self):
        self.grid = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.game_over = False
        self.show_hint = False
        self.hint_text = ""
        self.hint_timer = 0
        self.add_random_tile()
        self.add_random_tile()
    
    def add_random_tile(self):
        empty_cells = []
        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 0:
                    empty_cells.append((row, col))
        
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.grid[row][col] = 2 if random.random() < 0.9 else 4
    
    def move(self, direction):
        if self.game_over:
            return
        
        old_grid = [row[:] for row in self.grid]
        moved = False
        
        if direction == 'left':
            moved = self.move_left()
        elif direction == 'right':
            moved = self.move_right()
        elif direction == 'up':
            moved = self.move_up()
        elif direction == 'down':
            moved = self.move_down()
        
        if moved:
            self.add_random_tile()
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()  # Save the new high score
            
        if self.is_game_over():
            self.game_over = True
        # Hide hint after making a move
        self.show_hint = False
    
    def move_left(self):
        moved = False
        for row in range(4):
            # Compress
            compressed = [val for val in self.grid[row] if val != 0]
            
            # Merge
            merged = []
            i = 0
            while i < len(compressed):
                if i < len(compressed) - 1 and compressed[i] == compressed[i + 1]:
                    merged_value = compressed[i] * 2
                    merged.append(merged_value)
                    self.score += merged_value
                    i += 2
                else:
                    merged.append(compressed[i])
                    i += 1
            
            # Pad with zeros
            merged.extend([0] * (4 - len(merged)))
            
            if merged != self.grid[row]:
                moved = True
                self.grid[row] = merged
        
        return moved
    
    def move_right(self):
        for row in self.grid:
            row.reverse()
        moved = self.move_left()
        for row in self.grid:
            row.reverse()
        return moved
    
    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved
    
    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved
    
    def transpose(self):
        for i in range(4):
            for j in range(i + 1, 4):
                self.grid[i][j], self.grid[j][i] = self.grid[j][i], self.grid[i][j]
    
    def is_game_over(self):
        # Check for empty cells
        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 0:
                    return False
        
        # Check for possible merges
        for row in range(4):
            for col in range(4):
                current = self.grid[row][col]
                if ((col < 3 and self.grid[row][col + 1] == current) or
                    (row < 3 and self.grid[row + 1][col] == current)):
                    return False
        
        return True
    
    def update(self):
        """Update hint timer"""
        if self.show_hint:
            self.hint_timer -= 1
            if self.hint_timer <= 0:
                self.show_hint = False
    
    def handle_click(self, pos):
        if hasattr(self, 'hint_button') and self.hint_button.collidepoint(pos):
            hint = self.ai.get_best_move(self.grid)
            if hint:
                # Display hint in game window
                direction_symbols = {
                    'left': '← LEFT',
                    'right': '→ RIGHT', 
                    'up': '↑ UP',
                    'down': '↓ DOWN'
                }
                self.hint_text = f"AI suggests: {direction_symbols.get(hint, hint.upper())}"
                self.show_hint = True
                self.hint_timer = self.hint_duration
            else:
                self.hint_text = "No moves available!"
                self.show_hint = True
                self.hint_timer = self.hint_duration
        
        if hasattr(self, 'reset_button') and self.reset_button.collidepoint(pos):
            self.reset_game()
    
    def handle_keydown(self, event):
        if event.key in [pygame.K_LEFT, pygame.K_a]:
            self.move('left')
        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
            self.move('right')
        elif event.key in [pygame.K_UP, pygame.K_w]:
            self.move('up')
        elif event.key in [pygame.K_DOWN, pygame.K_s]:
            self.move('down')
    
    def draw_hint_overlay(self, body_font):
        """Draw the AI hint overlay on the game window"""
        if self.show_hint and self.hint_text:
            # Create semi-transparent overlay
            overlay_width = 400
            overlay_height = 80
            overlay_x = (self.screen.get_width() - overlay_width) // 2
            overlay_y = 120  # Position below the title
            
            # Create overlay surface with alpha
            overlay_surface = pygame.Surface((overlay_width, overlay_height), pygame.SRCALPHA)
            
            # Draw rounded background with fade effect based on timer
            alpha = min(255, max(50, int(255 * (self.hint_timer / 60))))  # Fade out in last second
            bg_color = (173, 216, 230, alpha)
            pygame.draw.rect(overlay_surface, bg_color, (0, 0, overlay_width, overlay_height), border_radius=20)
            
            # Draw border
            border_color = (*self.colors['text_white'], alpha)
            pygame.draw.rect(overlay_surface, border_color, (0, 0, overlay_width, overlay_height), width=2, border_radius=20)
            
            # Render hint text
            text_color = (*self.colors['text_white'], min(255, alpha))
            hint_surface = body_font.render(self.hint_text, True, self.colors['text_white'])
            text_rect = hint_surface.get_rect(center=(overlay_width // 2, overlay_height // 2))
            
            # Apply alpha to text surface
            hint_surface.set_alpha(alpha)
            overlay_surface.blit(hint_surface, text_rect)
            
            # Blit overlay to main screen
            self.screen.blit(overlay_surface, (overlay_x, overlay_y))
            
            # Add a subtle glow effect
            if self.hint_timer > 120:  # Only show glow for first 2 seconds
                glow_surface = pygame.Surface((overlay_width + 10, overlay_height + 10), pygame.SRCALPHA)
                glow_alpha = max(0, int(30 * (self.hint_timer - 120) / 60))
                pygame.draw.rect(glow_surface, (*self.colors['accent_blue'], glow_alpha), 
                               (0, 0, overlay_width + 10, overlay_height + 10), border_radius=25)
                self.screen.blit(glow_surface, (overlay_x - 5, overlay_y - 5))
                
                # Re-draw the main overlay on top
                self.screen.blit(overlay_surface, (overlay_x, overlay_y))
    
    def draw(self, mouse_pos, body_font, title_font, subheading_font):
        # Title
        title_surface = title_font.render("2048", True, self.colors['text_white'])
        title_rect = title_surface.get_rect(centerx=self.screen.get_width() // 2, y=50)
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle with score
        score_text = f"Score: {self.score} | High Score: {self.high_score}"
        subtitle_surface = body_font.render(f"Expectimax Algorithm | Score: {self.score}", True, self.colors['text_white'])
        subtitle_rect = subtitle_surface.get_rect(centerx=self.screen.get_width() // 2, y=90)
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw AI hint overlay (before game board so it appears behind)
        self.draw_hint_overlay(body_font)
        
        # Game board card with rounded corners
        board_card_size = 400
        board_card_x = (self.screen.get_width() - board_card_size) // 2
        board_card_y = 220  # Moved down to make room for hint overlay
        board_card_rect = pygame.Rect(board_card_x, board_card_y, board_card_size, board_card_size)
        
        pygame.draw.rect(self.screen, self.colors['card_bg'], board_card_rect, border_radius=30)
        
        # Game board
        board_size = 320
        board_x = board_card_x + (board_card_size - board_size) // 2
        board_y = board_card_y + (board_card_size - board_size) // 2
        cell_size = 80
        
        # Grid background with rounded corners
        pygame.draw.rect(self.screen, self.colors['border_light'], 
                        pygame.Rect(board_x - 5, board_y - 5, board_size + 10, board_size + 10), 
                        border_radius=15)
        
        # Draw cells
        for row in range(4):
            for col in range(4):
                x = board_x + col * cell_size
                y = board_y + row * cell_size
                
                value = self.grid[row][col]
                
                # Cell background with rounded corners
                cell_rect = pygame.Rect(x + 2, y + 2, cell_size - 4, cell_size - 4)
                if value == 0:
                    color = (205, 193, 180)
                else:
                    # Color based on value
                    if value <= 4:
                        color = (238, 228, 218)
                    elif value <= 16:
                        color = (237, 224, 200)
                    elif value <= 64:
                        color = (242, 177, 121)
                    elif value <= 256:
                        color = (245, 149, 99)
                    elif value <= 1024:
                        color = (246, 124, 95)
                    else:
                        color = (237, 207, 114)
                
                pygame.draw.rect(self.screen, color, cell_rect, border_radius=10)
                
                # Draw number
                if value > 0:
                    text_color = (119, 110, 101) if value <= 4 else (249, 246, 242)
                    font_size = 36 if value < 100 else 32 if value < 1000 else 28
                    font = pygame.font.Font(None, font_size)
                    text = font.render(str(value), True, text_color)
                    text_rect = text.get_rect(center=cell_rect.center)
                    self.screen.blit(text, text_rect)
        
        # Controls
        controls_y = board_card_y + board_card_size + 30
        controls_text = body_font.render("Use WASD or Arrow Keys to move", True, self.colors['text_white'])
        controls_rect = controls_text.get_rect(centerx=self.screen.get_width() // 2, y=controls_y)
        self.screen.blit(controls_text, controls_rect)
        
        # Buttons with rounded corners
        button_y = controls_y + 40
        hint_button = pygame.Rect(self.screen.get_width() // 2 - 110, button_y, 100, 40)
        hint_hovered = hint_button.collidepoint(mouse_pos)
        
        hint_color = self.colors['button_hover'] if hint_hovered else self.colors['success']
        pygame.draw.rect(self.screen, hint_color, hint_button, border_radius=25)
        
        hint_text = body_font.render("AI Hint", True, self.colors['text_white'])
        hint_text_rect = hint_text.get_rect(center=hint_button.center)
        self.screen.blit(hint_text, hint_text_rect)
        
        reset_button = pygame.Rect(self.screen.get_width() // 2 + 10, button_y, 100, 40)
        reset_hovered = reset_button.collidepoint(mouse_pos)
        
        reset_color = self.colors['button_hover'] if reset_hovered else self.colors['button_primary']
        pygame.draw.rect(self.screen, reset_color, reset_button, border_radius=25)
        
        reset_text = body_font.render("Reset", True, self.colors['text_white'])
        reset_text_rect = reset_text.get_rect(center=reset_button.center)
        self.screen.blit(reset_text, reset_text_rect)
        
        self.hint_button = hint_button
        self.reset_button = reset_button
        
        # Game over overlay
        if self.game_over:
            overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = title_font.render("Game Over!", True, self.colors['text_white'])
            game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(game_over_text, game_over_rect)

print("Game2048 module with visual AI hints loaded successfully!")