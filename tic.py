import pygame
import random

class TicTacToeAI:
    def __init__(self):
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
    
    def minimax(self, board, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        winner = self.check_winner(board)
        
        if winner == 'O':  # AI wins
            return 10 - depth
        elif winner == 'X':  # Human wins
            return depth - 10
        elif self.is_board_full(board):  # Tie
            return 0
        
        if is_maximizing:  # AI's turn
            max_eval = float('-inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    eval_score = self.minimax(board, depth + 1, False, alpha, beta)
                    board[i] = ''
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval
        else:  # Human's turn
            min_eval = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    eval_score = self.minimax(board, depth + 1, True, alpha, beta)
                    board[i] = ''
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval
    
    def get_best_move(self, board):
        best_score = float('-inf')
        best_move = None
        
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                score = self.minimax(board, 0, False)
                board[i] = ''
                
                if score > best_score:
                    best_score = score
                    best_move = i
        
        return best_move
    
    def check_winner(self, board):
        for combo in self.winning_combinations:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] != ''):
                return board[combo[0]]
        return None
    
    def is_board_full(self, board):
        return '' not in board

class TicTacToeGame:
    def __init__(self, screen, colors):
        self.screen = screen
        self.colors = colors
        self.ai = TicTacToeAI()
        self.reset_game()
    
    def reset_game(self):
        self.board = [''] * 9
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def handle_click(self, pos):
        if hasattr(self, 'reset_button') and self.reset_button.collidepoint(pos):
            self.reset_game()
            return
        
        if (self.game_over or self.current_player == 'O' or 
            not hasattr(self, 'board_rect')):
            return
        
        if self.board_rect.collidepoint(pos):
            rel_x = pos[0] - self.board_rect.x
            rel_y = pos[1] - self.board_rect.y
            col = rel_x // self.cell_size
            row = rel_y // self.cell_size
            index = row * 3 + col
            
            if 0 <= index < 9 and self.board[index] == '':
                self.board[index] = 'X'
                
                # Check for win
                winner = self.ai.check_winner(self.board)
                if winner:
                    self.winner = winner
                    self.game_over = True
                elif self.ai.is_board_full(self.board):
                    self.game_over = True
                else:
                    self.current_player = 'O'
    
    def update(self):
        if (self.current_player == 'O' and not self.game_over):
            # AI move
            best_move = self.ai.get_best_move(self.board)
            if best_move is not None:
                self.board[best_move] = 'O'
                
                # Check for win
                winner = self.ai.check_winner(self.board)
                if winner:
                    self.winner = winner
                    self.game_over = True
                elif self.ai.is_board_full(self.board):
                    self.game_over = True
                else:
                    self.current_player = 'X'
    
    def draw(self, mouse_pos, body_font, title_font, subheading_font):
        # Title
        title_surface = title_font.render("Tic Tac Toe", True, self.colors['text_white'])
        title_rect = title_surface.get_rect(centerx=self.screen.get_width() // 2, y=50)
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_surface = body_font.render("Minimax Algorithm with Alpha-Beta Pruning", True, self.colors['text_white'])
        subtitle_rect = subtitle_surface.get_rect(centerx=self.screen.get_width() // 2, y=90)
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Game board card with rounded corners
        board_card_size = 400
        board_card_x = (self.screen.get_width() - board_card_size) // 2
        board_card_y = 150
        board_card_rect = pygame.Rect(board_card_x, board_card_y, board_card_size, board_card_size)
        
        # Draw rounded card
        pygame.draw.rect(self.screen, self.colors['card_bg'], board_card_rect, border_radius=30)
        
        # Game board
        board_size = 300
        board_x = board_card_x + (board_card_size - board_size) // 2
        board_y = board_card_y + (board_card_size - board_size) // 2
        cell_size = board_size // 3
        
        # Grid lines
        for i in range(1, 3):
            # Vertical lines
            x = board_x + i * cell_size
            pygame.draw.line(self.screen, self.colors['border_light'], (x, board_y), (x, board_y + board_size), 3)
            # Horizontal lines
            y = board_y + i * cell_size
            pygame.draw.line(self.screen, self.colors['border_light'], (board_x, y), (board_x + board_size, y), 3)
        
        # Draw X's and O's
        for i in range(9):
            row = i // 3
            col = i % 3
            x = board_x + col * cell_size + cell_size // 2
            y = board_y + row * cell_size + cell_size // 2
            
            cell_rect = pygame.Rect(board_x + col * cell_size, board_y + row * cell_size, cell_size, cell_size)
            is_hovered = cell_rect.collidepoint(mouse_pos) and self.board[i] == ''
            
            if is_hovered and not self.game_over and self.current_player == 'X':
                # Hover preview with rounded corners
                pygame.draw.rect(self.screen, (240, 240, 240), cell_rect, border_radius=15)
            
            if self.board[i] == 'X':
                # Draw X
                offset = 30
                pygame.draw.line(self.screen, self.colors['accent_red'], 
                               (x - offset, y - offset), (x + offset, y + offset), 6)
                pygame.draw.line(self.screen, self.colors['accent_red'], 
                               (x + offset, y - offset), (x - offset, y + offset), 6)
            elif self.board[i] == 'O':
                # Draw O
                pygame.draw.circle(self.screen, self.colors['accent_blue'], (x, y), 30, 6)
        
        # Game status
        status_y = board_card_y + board_card_size + 30
        if self.game_over:
            if self.winner:
                status = f"Game Over - {self.winner} Wins!"
                status_color = self.colors['success'] if self.winner == 'X' else self.colors['accent_blue']
            else:
                status = "Game Over - It's a Draw!"
                status_color = self.colors['warning']
        else:
            if self.current_player == 'O':
                status = "AI is thinking..."
                status_color = self.colors['accent_blue']
            else:
                status = "Your turn - Click a cell"
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
        self.board_rect = pygame.Rect(board_x, board_y, board_size, board_size)
        self.cell_size = cell_size

print("TicTacToe module loaded successfully!")