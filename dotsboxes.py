import pygame
import random

class DotsAndBoxesAI:
    def __init__(self, rows=4, cols=4):
        self.rows = rows
        self.cols = cols
        
    def get_best_move(self, horizontal_lines, vertical_lines, boxes):
        """Simple AI that prioritizes completing boxes or safe moves"""
        # First, try to complete any boxes
        completing_moves = self.find_completing_moves(horizontal_lines, vertical_lines, boxes)
        if completing_moves:
            return random.choice(completing_moves)
        
        # Then, try to find safe moves (moves that don't give opponent a box)
        safe_moves = self.find_safe_moves(horizontal_lines, vertical_lines, boxes)
        if safe_moves:
            return random.choice(safe_moves)
        
        # Otherwise, make any available move
        all_moves = self.get_all_available_moves(horizontal_lines, vertical_lines)
        if all_moves:
            return random.choice(all_moves)
        
        return None
    
    def find_completing_moves(self, horizontal_lines, vertical_lines, boxes):
        """Find moves that complete a box"""
        completing_moves = []
        
        for row in range(self.rows):
            for col in range(self.cols):
                if boxes[row][col] == 0:  # Empty box
                    sides = self.count_box_sides(row, col, horizontal_lines, vertical_lines)
                    if sides == 3:  # One side missing
                        # Find the missing side
                        missing_move = self.find_missing_side(row, col, horizontal_lines, vertical_lines)
                        if missing_move:
                            completing_moves.append(missing_move)
        
        return completing_moves
    
    def find_safe_moves(self, horizontal_lines, vertical_lines, boxes):
        """Find moves that don't create a 3-sided box for opponent"""
        safe_moves = []
        all_moves = self.get_all_available_moves(horizontal_lines, vertical_lines)
        
        for move in all_moves:
            if self.is_safe_move(move, horizontal_lines, vertical_lines, boxes):
                safe_moves.append(move)
        
        return safe_moves
    
    def is_safe_move(self, move, horizontal_lines, vertical_lines, boxes):
        """Check if a move doesn't create a 3-sided box"""
        move_type, row, col = move
        
        # Temporarily make the move
        if move_type == 'horizontal':
            horizontal_lines[row][col] = True
        else:
            vertical_lines[row][col] = True
        
        # Check if this creates any 3-sided boxes
        creates_opportunity = False
        for box_row in range(self.rows):
            for box_col in range(self.cols):
                if boxes[box_row][box_col] == 0:
                    sides = self.count_box_sides(box_row, box_col, horizontal_lines, vertical_lines)
                    if sides == 3:
                        creates_opportunity = True
                        break
            if creates_opportunity:
                break
        
        # Undo the move
        if move_type == 'horizontal':
            horizontal_lines[row][col] = False
        else:
            vertical_lines[row][col] = False
        
        return not creates_opportunity
    
    def count_box_sides(self, row, col, horizontal_lines, vertical_lines):
        """Count how many sides of a box are drawn"""
        sides = 0
        
        # Top side
        if horizontal_lines[row][col]:
            sides += 1
        # Bottom side
        if horizontal_lines[row + 1][col]:
            sides += 1
        # Left side
        if vertical_lines[row][col]:
            sides += 1
        # Right side
        if vertical_lines[row][col + 1]:
            sides += 1
        
        return sides
    
    def find_missing_side(self, row, col, horizontal_lines, vertical_lines):
        """Find which side is missing from a 3-sided box"""
        if not horizontal_lines[row][col]:
            return ('horizontal', row, col)
        if not horizontal_lines[row + 1][col]:
            return ('horizontal', row + 1, col)
        if not vertical_lines[row][col]:
            return ('vertical', row, col)
        if not vertical_lines[row][col + 1]:
            return ('vertical', row, col + 1)
        return None
    
    def get_all_available_moves(self, horizontal_lines, vertical_lines):
        """Get all available moves"""
        moves = []
        
        # Horizontal lines
        for row in range(self.rows + 1):
            for col in range(self.cols):
                if not horizontal_lines[row][col]:
                    moves.append(('horizontal', row, col))
        
        # Vertical lines
        for row in range(self.rows):
            for col in range(self.cols + 1):
                if not vertical_lines[row][col]:
                    moves.append(('vertical', row, col))
        
        return moves

class DotsAndBoxesGame:
    def __init__(self, screen, colors):
        self.screen = screen
        self.colors = colors
        self.ai = DotsAndBoxesAI()
        self.reset_game()
    
    def reset_game(self):
        self.rows = 4
        self.cols = 4
        self.horizontal_lines = [[False for _ in range(self.cols)] for _ in range(self.rows + 1)]
        self.vertical_lines = [[False for _ in range(self.cols + 1)] for _ in range(self.rows)]
        self.boxes = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1  # 1 = human, 2 = AI
        self.scores = [0, 0]  # [human, AI]
        self.game_over = False
    
    def handle_click(self, pos):
        if hasattr(self, 'reset_button') and self.reset_button.collidepoint(pos):
            self.reset_game()
            return
        
        if self.game_over or self.current_player == 2:
            return
        
        if not hasattr(self, 'board_rect') or not self.board_rect.collidepoint(pos):
            return
        
        # Check horizontal lines
        for row in range(self.rows + 1):
            for col in range(self.cols):
                if not self.horizontal_lines[row][col]:
                    line_x1 = self.board_x + col * self.cell_size + 8
                    line_x2 = self.board_x + (col + 1) * self.cell_size - 8
                    line_y = self.board_y + row * self.cell_size
                    
                    line_rect = pygame.Rect(line_x1, line_y - 3, line_x2 - line_x1, 6)
                    
                    if line_rect.collidepoint(pos):
                        self.make_move('horizontal', row, col)
                        return
        
        # Check vertical lines
        for row in range(self.rows):
            for col in range(self.cols + 1):
                if not self.vertical_lines[row][col]:
                    line_x = self.board_x + col * self.cell_size
                    line_y1 = self.board_y + row * self.cell_size + 8
                    line_y2 = self.board_y + (row + 1) * self.cell_size - 8
                    
                    line_rect = pygame.Rect(line_x - 3, line_y1, 6, line_y2 - line_y1)
                    
                    if line_rect.collidepoint(pos):
                        self.make_move('vertical', row, col)
                        return
    
    def make_move(self, move_type, row, col):
        """Make a move in dots and boxes"""
        if move_type == 'horizontal':
            self.horizontal_lines[row][col] = True
        else:
            self.vertical_lines[row][col] = True
        
        # Check for completed boxes
        boxes_completed = self.check_completed_boxes()
        
        if boxes_completed > 0:
            self.scores[self.current_player - 1] += boxes_completed
            # Player gets another turn when completing boxes
        else:
            # Switch players
            self.current_player = 2 if self.current_player == 1 else 1
        
        # Check if game is over
        if self.is_game_over():
            self.game_over = True
    
    def check_completed_boxes(self):
        """Check for newly completed boxes and mark them"""
        completed = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                if self.boxes[row][col] == 0:  # Empty box
                    # Check if all four sides are drawn
                    if (self.horizontal_lines[row][col] and 
                        self.horizontal_lines[row + 1][col] and
                        self.vertical_lines[row][col] and 
                        self.vertical_lines[row][col + 1]):
                        
                        self.boxes[row][col] = self.current_player
                        completed += 1
        
        return completed
    
    def is_game_over(self):
        """Check if all boxes are completed"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.boxes[row][col] == 0:
                    return False
        return True
    
    def update(self):
        """Update dots and boxes AI logic"""
        if self.current_player == 2 and not self.game_over:
            # AI move
            best_move = self.ai.get_best_move(
                self.horizontal_lines, self.vertical_lines, self.boxes
            )
            
            if best_move:
                move_type, row, col = best_move
                self.make_move(move_type, row, col)
    
    def draw(self, mouse_pos, body_font, title_font, subheading_font, caption_font):
        # Title
        title_surface = title_font.render("Dots and Boxes", True, self.colors['text_white'])
        title_rect = title_surface.get_rect(centerx=self.screen.get_width() // 2, y=50)
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle with scores
        subtitle_surface = body_font.render(f"Strategic AI | Player: {self.scores[0]} | AI: {self.scores[1]}", True, self.colors['text_white'])
        subtitle_rect = subtitle_surface.get_rect(centerx=self.screen.get_width() // 2, y=90)
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Game board card with rounded corners
        board_card_size = 450
        board_card_x = (self.screen.get_width() - board_card_size) // 2
        board_card_y = 130
        board_card_rect = pygame.Rect(board_card_x, board_card_y, board_card_size, board_card_size)
        
        pygame.draw.rect(self.screen, self.colors['card_bg'], board_card_rect, border_radius=30)
        
        # Game board
        board_size = 360
        board_x = board_card_x + (board_card_size - board_size) // 2
        board_y = board_card_y + (board_card_size - board_size) // 2
        cell_size = board_size // self.cols
        dot_radius = 8
        line_thickness = 4
        
        # Draw boxes
        for row in range(self.rows):
            for col in range(self.cols):
                box_x = board_x + col * cell_size + dot_radius
                box_y = board_y + row * cell_size + dot_radius
                box_size = cell_size - 2 * dot_radius
                box_rect = pygame.Rect(box_x, box_y, box_size, box_size)
                
                if self.boxes[row][col] == 1:  # Human box
                # Light red with slight transparency
                 pygame.draw.rect(self.screen, (255, 150, 150, 150), box_rect, border_radius=8)
                 text = caption_font.render("P", True, (200, 0, 0))  # Dark red text for contrast
                 text_rect = text.get_rect(center=box_rect.center)
                 self.screen.blit(text, text_rect)
                elif self.boxes[row][col] == 2:  # AI box
    # Light blue with slight transparency
                 pygame.draw.rect(self.screen, (150, 150, 255, 150), box_rect, border_radius=8)
                 text = caption_font.render("AI", True, (0, 0, 200))  # Dark blue text for contrast
                 text_rect = text.get_rect(center=box_rect.center)
                 self.screen.blit(text, text_rect)
        # Draw dots
        for row in range(self.rows + 1):
            for col in range(self.cols + 1):
                dot_x = board_x + col * cell_size
                dot_y = board_y + row * cell_size
                pygame.draw.circle(self.screen, self.colors['text_primary'], (dot_x, dot_y), dot_radius)
        
        # Draw lines with rounded ends
        for row in range(self.rows + 1):
            for col in range(self.cols):
                line_x1 = board_x + col * cell_size + dot_radius
                line_x2 = board_x + (col + 1) * cell_size - dot_radius
                line_y = board_y + row * cell_size
                
                line_rect = pygame.Rect(line_x1, line_y - line_thickness // 2, 
                                      line_x2 - line_x1, line_thickness)
                
                is_hovered = line_rect.collidepoint(mouse_pos) and not self.horizontal_lines[row][col]
                
                if self.horizontal_lines[row][col]:
                    pygame.draw.line(self.screen, self.colors['accent_purple'], 
                                   (line_x1, line_y), (line_x2, line_y), line_thickness)
                    # Rounded ends
                    pygame.draw.circle(self.screen, self.colors['accent_purple'], (line_x1, line_y), line_thickness//2)
                    pygame.draw.circle(self.screen, self.colors['accent_purple'], (line_x2, line_y), line_thickness//2)
                elif is_hovered and not self.game_over and self.current_player == 1:
                    pygame.draw.line(self.screen, (200, 200, 200), 
                                   (line_x1, line_y), (line_x2, line_y), line_thickness)
        
        for row in range(self.rows):
            for col in range(self.cols + 1):
                line_x = board_x + col * cell_size
                line_y1 = board_y + row * cell_size + dot_radius
                line_y2 = board_y + (row + 1) * cell_size - dot_radius
                
                line_rect = pygame.Rect(line_x - line_thickness // 2, line_y1, 
                                      line_thickness, line_y2 - line_y1)
                
                is_hovered = line_rect.collidepoint(mouse_pos) and not self.vertical_lines[row][col]
                
                if self.vertical_lines[row][col]:
                    pygame.draw.line(self.screen, self.colors['accent_purple'], 
                                   (line_x, line_y1), (line_x, line_y2), line_thickness)
                    # Rounded ends
                    pygame.draw.circle(self.screen, self.colors['accent_purple'], (line_x, line_y1), line_thickness//2)
                    pygame.draw.circle(self.screen, self.colors['accent_purple'], (line_x, line_y2), line_thickness//2)
                elif is_hovered and not self.game_over and self.current_player == 1:
                    pygame.draw.line(self.screen, (200, 200, 200), 
                                   (line_x, line_y1), (line_x, line_y2), line_thickness)
        
        # Game status
        status_y = board_card_y + board_card_size + 30
        if self.game_over:
            if self.scores[0] > self.scores[1]:
                status = "Congratulations! You Win!"
                status_color = self.colors['success']
            elif self.scores[1] > self.scores[0]:
                status = "AI Wins! Great game!"
                status_color = self.colors['accent_blue']
            else:
                status = "It's a Draw! Well played!"
                status_color = self.colors['warning']
        else:
            if self.current_player == 2:
                status = "AI is planning the next move..."
                status_color = self.colors['accent_blue']
            else:
                status = "Your turn - Click a line to draw it"
                status_color = self.colors['text_white']
        
        status_surface = subheading_font.render(status, True, status_color)
        status_rect = status_surface.get_rect(centerx=self.screen.get_width() // 2, y=status_y)
        self.screen.blit(status_surface, status_rect)
        
        # Reset button with rounded corners
        reset_button = pygame.Rect(self.screen.get_width() // 2 - 60, status_y + 50, 120, 40)
        reset_hovered = reset_button.collidepoint(mouse_pos)
        
        reset_color = self.colors['button_hover'] if reset_hovered else self.colors['button_primary']
        pygame.draw.rect(self.screen, reset_color, reset_button, border_radius=25)
        
        reset_text = body_font.render("Reset", True, self.colors['text_white'])
        reset_text_rect = reset_text.get_rect(center=reset_button.center)
        self.screen.blit(reset_text, reset_text_rect)
        
        self.reset_button = reset_button
        self.board_rect = pygame.Rect(board_x - 20, board_y - 20, board_size + 40, board_size + 40)
        self.cell_size = cell_size
        self.board_x = board_x
        self.board_y = board_y

print("DotsAndBoxes module loaded successfully!")