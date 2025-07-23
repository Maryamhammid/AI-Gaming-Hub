import pygame
import random

class ConnectFourAI:
    def __init__(self):
        self.rows = 6
        self.cols = 7
    
    def minimax(self, board, depth, alpha, beta, maximizing):
        winner = self.check_winner(board)
        if winner == 2:  # AI wins
            return 1000000
        elif winner == 1:  # Player wins
            return -1000000
        elif self.is_board_full(board):  # Tie
            return 0
        elif depth == 0:  # Reached max depth
            return self.evaluate_board(board)
        
        valid_moves = self.get_valid_moves(board)
        
        if maximizing:  # AI's turn
            value = float('-inf')
            for col in valid_moves:
                row = self.get_next_open_row(board, col)
                temp_board = [row[:] for row in board]
                self.drop_piece(temp_board, row, col, 2)
                
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, False)
                value = max(value, new_score)
                alpha = max(alpha, value)
                
                if alpha >= beta:
                    break
            return value
        else:  # Player's turn
            value = float('inf')
            for col in valid_moves:
                row = self.get_next_open_row(board, col)
                temp_board = [row[:] for row in board]
                self.drop_piece(temp_board, row, col, 1)
                
                new_score = self.minimax(temp_board, depth - 1, alpha, beta, True)
                value = min(value, new_score)
                beta = min(beta, value)
                
                if alpha >= beta:
                    break
            return value
    
    def get_best_move(self, board):
        valid_moves = self.get_valid_moves(board)
        if not valid_moves:
            return 3
        
        # Check for immediate winning moves
        for col in valid_moves:
            row = self.get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            self.drop_piece(temp_board, row, col, 2)
            if self.check_winner(temp_board) == 2:
                return col
        
        # Check for blocking moves
        for col in valid_moves:
            row = self.get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            self.drop_piece(temp_board, row, col, 1)
            if self.check_winner(temp_board) == 1:
                return col
        
        # Use minimax for best strategic move
        best_score = float('-inf')
        best_col = random.choice(valid_moves)
        
        for col in valid_moves:
            row = self.get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            self.drop_piece(temp_board, row, col, 2)
            
            score = self.minimax(temp_board, 4, float('-inf'), float('inf'), False)
            
            if score > best_score:
                best_score = score
                best_col = col
        
        return best_col
    
    def get_valid_moves(self, board):
        return [col for col in range(self.cols) if board[0][col] == 0]
    
    def get_next_open_row(self, board, col):
        for row in range(self.rows - 1, -1, -1):
            if board[row][col] == 0:
                return row
        return -1
    
    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece
    
    def check_winner(self, board):
        # Check horizontal
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if board[row][col] != 0 and board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]:
                    return board[row][col]
        
        # Check vertical
        for row in range(self.rows - 3):
            for col in range(self.cols):
                if board[row][col] != 0 and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                    return board[row][col]
        
        # Check diagonal (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if board[row][col] != 0 and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                    return board[row][col]
        
        # Check diagonal (negative slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if board[row][col] != 0 and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                    return board[row][col]
        
        return 0
    
    def is_board_full(self, board):
        return all(board[0][col] != 0 for col in range(self.cols))
    
    def evaluate_board(self, board):
        score = 0
        
        # Center column preference
        center_col = self.cols // 2
        center_count = sum(1 for row in range(self.rows) if board[row][center_col] == 2)
        score += center_count * 3
        
        # Evaluate windows of 4
        for row in range(self.rows):
            for col in range(self.cols - 3):
                window = [board[row][col+i] for i in range(4)]
                score += self.evaluate_window(window)
        
        return score
    
    def evaluate_window(self, window):
        score = 0
        ai_count = window.count(2)
        player_count = window.count(1)
        empty_count = window.count(0)
        
        if ai_count == 4:
            score += 100
        elif ai_count == 3 and empty_count == 1:
            score += 5
        elif ai_count == 2 and empty_count == 2:
            score += 2
        
        if player_count == 3 and empty_count == 1:
            score -= 4
        
        return score

class ConnectFourGame:
    def __init__(self, screen, colors):
        self.screen = screen
        self.colors = colors
        self.ai = ConnectFourAI()
        self.reset_game()
    
    def reset_game(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.current_player = 1
        self.game_over = False
        self.winner = None
    
    def handle_click(self, pos):
        if hasattr(self, 'reset_button') and self.reset_button.collidepoint(pos):
            self.reset_game()
            return
        
        if (self.game_over or self.current_player == 2 or 
            not hasattr(self, 'board_rect')):
            return
        
        if self.board_rect.collidepoint(pos):
            rel_x = pos[0] - self.board_rect.x
            col = rel_x // self.cell_size
            
            if 0 <= col < 7:
                # Find the lowest empty row
                for row in range(5, -1, -1):
                    if self.board[row][col] == 0:
                        self.board[row][col] = 1
                        
                        # Check for win
                        winner = self.ai.check_winner(self.board)
                        if winner:
                            self.winner = winner
                            self.game_over = True
                        elif self.ai.is_board_full(self.board):
                            self.game_over = True
                        else:
                            self.current_player = 2
                        break
    
    def update(self):
        if (self.current_player == 2 and not self.game_over):
            # AI move
            best_col = self.ai.get_best_move(self.board)
            
            # Find the lowest empty row in the chosen column
            for row in range(5, -1, -1):
                if self.board[row][best_col] == 0:
                    self.board[row][best_col] = 2
                    
                    # Check for win
                    winner = self.ai.check_winner(self.board)
                    if winner:
                        self.winner = winner
                        self.game_over = True
                    elif self.ai.is_board_full(self.board):
                        self.game_over = True
                    else:
                        self.current_player = 1
                    break
    
    def draw(self, mouse_pos, body_font, title_font, subheading_font):
        # Title
        title_surface = title_font.render("Connect Four", True, self.colors['text_white'])
        title_rect = title_surface.get_rect(centerx=self.screen.get_width() // 2, y=50)
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_surface = body_font.render("Minimax with Alpha-Beta Pruning", True, self.colors['text_white'])
        subtitle_rect = subtitle_surface.get_rect(centerx=self.screen.get_width() // 2, y=90)
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Game board card with rounded corners
        board_card_width = 450
        board_card_height = 400
        board_card_x = (self.screen.get_width() - board_card_width) // 2
        board_card_y = 150
        board_card_rect = pygame.Rect(board_card_x, board_card_y, board_card_width, board_card_height)
        
        pygame.draw.rect(self.screen, self.colors['card_bg'], board_card_rect, border_radius=30)
        
        # Game board
        board_width = 350
        board_height = 300
        board_x = board_card_x + (board_card_width - board_width) // 2
        board_y = board_card_y + (board_card_height - board_height) // 2
        cell_size = 50
        
        # Board background with rounded corners
        pygame.draw.rect(self.screen, self.colors['accent_blue'], 
                        pygame.Rect(board_x - 10, board_y - 10, board_width + 20, board_height + 20), 
                        border_radius=20)
        
        # Draw cells
        for row in range(6):
            for col in range(7):
                x = board_x + col * cell_size
                y = board_y + row * cell_size
                
                # Cell background
                pygame.draw.circle(self.screen, self.colors['card_bg'], 
                                 (x + cell_size // 2, y + cell_size // 2), 20)
                
                # Piece
                if self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, self.colors['accent_red'], 
                                     (x + cell_size // 2, y + cell_size // 2), 18)
                elif self.board[row][col] == 2:
                    pygame.draw.circle(self.screen, self.colors['accent_orange'], 
                                     (x + cell_size // 2, y + cell_size // 2), 18)
        
        # Column indicators
        for col in range(7):
            x = board_x + col * cell_size + cell_size // 2
            y = board_y - 30
            
            col_rect = pygame.Rect(board_x + col * cell_size, board_y - 50, cell_size, board_height + 50)
            is_hovered = col_rect.collidepoint(mouse_pos)
            
            if is_hovered and not self.game_over and self.current_player == 1:
                # Column highlight
                highlight_surface = pygame.Surface((cell_size, board_height + 50), pygame.SRCALPHA)
                highlight_surface.fill((255, 255, 255, 50))
                self.screen.blit(highlight_surface, (board_x + col * cell_size, board_y - 50))
            
            # Arrow
            arrow_color = self.colors['text_white'] if is_hovered else (200, 200, 200)
            pygame.draw.polygon(self.screen, arrow_color, 
                              [(x - 8, y), (x + 8, y), (x, y + 12)])
        
        # Game status
        status_y = board_card_y + board_card_height + 30
        if self.game_over:
            if self.winner == 1:
                status = "Congratulations! You Win!"
                status_color = self.colors['success']
            elif self.winner == 2:
                status = "AI Wins! Better luck next time."
                status_color = self.colors['accent_blue']
            else:
                status = "It's a Draw!"
                status_color = self.colors['warning']
        else:
            if self.current_player == 2:
                status = "AI is calculating the best move..."
                status_color = self.colors['accent_blue']
            else:
                status = "Your turn - Click a column to drop your piece"
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
        self.board_rect = pygame.Rect(board_x, board_y - 50, board_width, board_height + 50)
        self.cell_size = cell_size

print("ConnectFour module loaded successfully!")