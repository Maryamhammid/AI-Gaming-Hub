import pygame
import sys
from enum import Enum
from tic import TicTacToeGame
from four import ConnectFourGame
from g_2048 import Game2048
from dotsboxes import DotsAndBoxesGame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1550
SCREEN_HEIGHT = 800
FPS = 80

# Modern UI Colors with warm sunset gradient
COLORS = {
    # New warm sunset gradient background colors
    'gradient_top': (255, 154, 158),      # Soft coral pink
    'gradient_middle': (250, 208, 196),   # Warm peach
    'gradient_bottom': (255, 206, 84),    # Golden yellow
    
    # Card and UI colors
    'card_bg': (255, 255, 255),          # Pure white cards
    'card_shadow': (0, 0, 0, 25),        # Subtle shadow
    'card_hover': (255, 255, 255),       # White with slight glow
    'card_hover_glow': (255, 255, 255, 40), # Hover glow effect
    
    # Text colors
    'text_primary': (45, 55, 72),        # Dark gray for titles
    'text_secondary': (113, 128, 150),   # Medium gray for descriptions
    'text_white': (255, 255, 255),       # White text
    
    # Accent colors for icons and elements
    'accent_red': (239, 68, 68),         # Red for Connect 4
    'accent_blue': (59, 130, 246),       # Blue for 2048
    'accent_green': (16, 185, 129),      # Green/teal for dots
    'accent_purple': (139, 92, 246),     # Purple accent
    'accent_orange': (251, 146, 60),     # Orange for target
    'dots_player': (0, 120, 255),  # Player box color
    'dots_ai': (255, 70, 70),  
    # UI elements
    'button_primary': (139, 92, 246),    # Purple buttons
    'button_hover': (124, 58, 237),      # Darker purple on hover
    'border_light': (226, 232, 240),     # Light borders
    'success': (16, 185, 129),           # Success green
    'warning': (245, 158, 11),           # Warning amber
    'error': (239, 68, 68),              # Error red
}

class GameState(Enum):
    MENU = "menu"
    TIC_TAC_TOE = "tic_tac_toe"
    CONNECT_FOUR = "connect_four"
    GAME_2048 = "game_2048"
    DOTS_AND_BOXES = "dots_and_boxes"

class ModernAIGamesHub:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("AI Games Hub - Modern Rounded Interface")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_state = GameState.MENU
        
        # Mouse tracking for hover effects
        self.mouse_pos = (0, 0)
        
        # Animation for hover effects
        self.hover_scale = {}  # Track hover scale for each card
        
        # Modern fonts
        self.title_font = pygame.font.Font(None, 48)
        self.heading_font = pygame.font.Font(None, 36)
        self.subheading_font = pygame.font.Font(None, 28)
        self.body_font = pygame.font.Font(None, 24)
        self.caption_font = pygame.font.Font(None, 20)
        
        # Game instances
        self.tic_tac_toe = TicTacToeGame(self.screen, COLORS)
        self.connect_four = ConnectFourGame(self.screen, COLORS)
        self.game_2048 = Game2048(self.screen, COLORS)
        self.dots_and_boxes = DotsAndBoxesGame(self.screen, COLORS)
        
    def draw_gradient_background(self):
        """Draw the beautiful warm sunset gradient background"""
        for y in range(SCREEN_HEIGHT):
            # Calculate the gradient ratio
            ratio = y / SCREEN_HEIGHT
            
            # Interpolate between gradient colors for smooth sunset effect
            if ratio < 0.4:
                # Top to middle (coral to peach)
                local_ratio = ratio / 0.4
                r = int(COLORS['gradient_top'][0] * (1 - local_ratio) + COLORS['gradient_middle'][0] * local_ratio)
                g = int(COLORS['gradient_top'][1] * (1 - local_ratio) + COLORS['gradient_middle'][1] * local_ratio)
                b = int(COLORS['gradient_top'][2] * (1 - local_ratio) + COLORS['gradient_middle'][2] * local_ratio)
            else:
                # Middle to bottom (peach to golden)
                local_ratio = (ratio - 0.4) / 0.6
                r = int(COLORS['gradient_middle'][0] * (1 - local_ratio) + COLORS['gradient_bottom'][0] * local_ratio)
                g = int(COLORS['gradient_middle'][1] * (1 - local_ratio) + COLORS['gradient_bottom'][1] * local_ratio)
                b = int(COLORS['gradient_middle'][2] * (1 - local_ratio) + COLORS['gradient_bottom'][2] * local_ratio)
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    def draw_rounded_card_with_hover(self, rect, card_id, is_hovered=False):
        """Draw a rounded card with smooth hover animation"""
        # Initialize hover scale if not exists
        if card_id not in self.hover_scale:
            self.hover_scale[card_id] = 1.0
        
        # Smooth hover animation
        target_scale = 1.05 if is_hovered else 1.0
        self.hover_scale[card_id] += (target_scale - self.hover_scale[card_id]) * 0.15
        
        # Calculate scaled rect
        scale = self.hover_scale[card_id]
        scaled_width = int(rect.width * scale)
        scaled_height = int(rect.height * scale)
        scaled_x = rect.centerx - scaled_width // 2
        scaled_y = rect.centery - scaled_height // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Enhanced shadow with hover effect
        shadow_offset = 8 if is_hovered else 6
        shadow_alpha = 35 if is_hovered else 25
        shadow_rect = pygame.Rect(scaled_rect.x + shadow_offset, scaled_rect.y + shadow_offset, 
                                 scaled_rect.width, scaled_rect.height)
        shadow_surface = pygame.Surface((scaled_rect.width, scaled_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (*COLORS['card_shadow'][:3], shadow_alpha), 
                        (0, 0, scaled_rect.width, scaled_rect.height), border_radius=30)
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Hover glow effect
        if is_hovered:
            glow_rect = pygame.Rect(scaled_rect.x - 4, scaled_rect.y - 4, 
                                   scaled_rect.width + 8, scaled_rect.height + 8)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, COLORS['card_hover_glow'], 
                           (0, 0, glow_rect.width, glow_rect.height), border_radius=34)
            self.screen.blit(glow_surface, glow_rect)
        
        # Card background with very rounded corners
        pygame.draw.rect(self.screen, COLORS['card_hover'] if is_hovered else COLORS['card_bg'], 
                        scaled_rect, border_radius=30)
        
        return scaled_rect
    
    def draw_icon(self, center_pos, icon_type, size=60):
        """Draw game icons"""
        x, y = center_pos
        
        if icon_type == "target":  # Tic Tac Toe
            # Draw target/bullseye icon
            pygame.draw.circle(self.screen, COLORS['accent_orange'], (x, y), size//2, 6)
            pygame.draw.circle(self.screen, COLORS['accent_orange'], (x, y), size//3, 6)
            pygame.draw.circle(self.screen, COLORS['accent_orange'], (x, y), size//6)
            
        elif icon_type == "circle":  # Connect 4
            # Draw red circle
            pygame.draw.circle(self.screen, COLORS['accent_red'], (x, y), size//2)
            pygame.draw.circle(self.screen, (200, 50, 50), (x, y), size//2, 3)
            
        elif icon_type == "box":  # Dots and Boxes
            # Draw 3D box icon
            box_size = size // 2
            # Front face
            front_rect = pygame.Rect(x - box_size//2, y - box_size//4, box_size, box_size//2)
            pygame.draw.rect(self.screen, (205, 133, 63), front_rect)
            # Top face
            top_points = [
                (x - box_size//2, y - box_size//4),
                (x, y - box_size//2),
                (x + box_size//2, y - box_size//4),
                (x, y)
            ]
            pygame.draw.polygon(self.screen, (222, 184, 135), top_points)
            # Right face
            right_points = [
                (x + box_size//2, y - box_size//4),
                (x + box_size//2, y + box_size//4),
                (x, y + box_size//2),
                (x, y)
            ]
            pygame.draw.polygon(self.screen, (160, 82, 45), right_points)
            
        elif icon_type == "2048":  # 2048
            # Draw 2048 grid icon
            grid_size = size // 2
            cell_size = grid_size // 2 - 2
            
            # Background
            bg_rect = pygame.Rect(x - grid_size//2, y - grid_size//2, grid_size, grid_size)
            pygame.draw.rect(self.screen, COLORS['accent_blue'], bg_rect, border_radius=8)
            
            # Grid cells with numbers
            numbers = ['1', '2', '3', '4']
            for i in range(2):
                for j in range(2):
                    cell_x = x - grid_size//2 + j * (cell_size + 2) + 2
                    cell_y = y - grid_size//2 + i * (cell_size + 2) + 2
                    cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
                    pygame.draw.rect(self.screen, COLORS['card_bg'], cell_rect, border_radius=4)
                    
                    # Number
                    num_surface = self.caption_font.render(numbers[i*2 + j], True, COLORS['accent_blue'])
                    num_rect = num_surface.get_rect(center=cell_rect.center)
                    self.screen.blit(num_surface, num_rect)
    
    # def draw_dots_indicator(self, center_pos):
    #     """Draw three dots indicator"""
    #     x, y = center_pos
    #     dot_spacing = 8
    #     for i in range(3):
    #         dot_x = x - dot_spacing + i * dot_spacing
    #         pygame.draw.circle(self.screen, COLORS['accent_green'], (dot_x, y), 3)
    
    def draw_menu(self):
        self.draw_gradient_background()
        
        # Beautiful main title at the top
        title_y = 40
        title_text = "AI Gaming Hub"

        # Create a larger font for the main title
        main_title_font = pygame.font.Font(None, 72)

        # Draw title shadow for depth
        shadow_offset = 3
        title_shadow = main_title_font.render(title_text, True, (0, 0, 0, 100))
        shadow_rect = title_shadow.get_rect(centerx=SCREEN_WIDTH // 2 + shadow_offset, y=title_y + shadow_offset)
        self.screen.blit(title_shadow, shadow_rect)

        # Draw main title with beautiful white color
        title_surface = main_title_font.render(title_text, True, COLORS['text_white'])
        title_rect = title_surface.get_rect(centerx=SCREEN_WIDTH // 2, y=title_y)
        self.screen.blit(title_surface, title_rect)

        # Add a subtle glow effect around the title
        glow_surface = pygame.Surface((title_rect.width + 20, title_rect.height + 20), pygame.SRCALPHA)
        glow_rect = pygame.Rect(0, 0, title_rect.width + 20, title_rect.height + 20)
        pygame.draw.rect(glow_surface, (255, 255, 255, 30), glow_rect, border_radius=15)
        self.screen.blit(glow_surface, (title_rect.x - 10, title_rect.y - 10))

        # Re-draw the title on top of the glow
        self.screen.blit(title_surface, title_rect)
        
        # Header badge with rounded corners
        badge_text = "Featuring Advanced AI Algorithms"
        badge_surface = self.body_font.render(badge_text, True, COLORS['text_white'])
        badge_width = badge_surface.get_width() + 40
        badge_height = 40
        badge_x = (SCREEN_WIDTH - badge_width) // 2
        badge_y = 120
        
        badge_rect = pygame.Rect(badge_x, badge_y, badge_width, badge_height)
        # More rounded badge
        pygame.draw.rect(self.screen, (255, 255, 255, 60), badge_rect, border_radius=25)
        
        badge_text_rect = badge_surface.get_rect(center=badge_rect.center)
        self.screen.blit(badge_surface, badge_text_rect)
        
        # Game cards with enhanced spacing
        card_width = 260
        card_height = 200
        card_spacing = 50  # Increased spacing for better hover effect
        
        # Calculate grid positioning
        total_width = 2 * card_width + card_spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        start_y = 180
        
        games = [
            ("Tic Tac Toe", "Minimax Algorithm", "target"),
            ("Connect 4", "Minimax with Alpha-Beta Pruning", "circle"),
            ("Dots and Boxes", "Minimax with Heuristics", "box"),
            ("2048", "Expectimax Algorithm", "2048")
        ]
        
        self.menu_buttons = []
        
        for i, (title, algorithm, icon_type) in enumerate(games):
            row = i // 2
            col = i % 2
            
            x = start_x + col * (card_width + card_spacing)
            y = start_y + row * (card_height + card_spacing)
            
            card_rect = pygame.Rect(x, y, card_width, card_height)
            is_hovered = card_rect.collidepoint(self.mouse_pos)
            
            # Draw rounded card with hover effect
            card_id = f"menu_card_{i}"
            scaled_rect = self.draw_rounded_card_with_hover(card_rect, card_id, is_hovered)
            
            # Icon (adjust position based on scaling)
            icon_y = scaled_rect.y + 60
            self.draw_icon((scaled_rect.centerx, icon_y), icon_type)
            
            # Title
            title_surface = self.heading_font.render(title, True, COLORS['text_primary'])
            title_rect = title_surface.get_rect(centerx=scaled_rect.centerx, y=scaled_rect.y + 110)
            self.screen.blit(title_surface, title_rect)
            
            # Algorithm description
            algo_surface = self.caption_font.render(algorithm, True, COLORS['text_secondary'])
            algo_rect = algo_surface.get_rect(centerx=scaled_rect.centerx, y=scaled_rect.y + 140)
            self.screen.blit(algo_surface, algo_rect)
            
            # # Three dots indicator
            # self.draw_dots_indicator((scaled_rect.centerx, scaled_rect.y + 170))
            
            # Store original rect for click detection
            self.menu_buttons.append((card_rect, [GameState.TIC_TAC_TOE, GameState.CONNECT_FOUR, GameState.DOTS_AND_BOXES, GameState.GAME_2048][i]))
    
    def draw_back_button(self):
        """Draw modern back button with rounded corners"""
        back_rect = pygame.Rect(30, 30, 100, 40)
        is_hovered = back_rect.collidepoint(self.mouse_pos)
        
        # Button background with more rounded corners
        bg_color = COLORS['button_hover'] if is_hovered else COLORS['button_primary']
        pygame.draw.rect(self.screen, bg_color, back_rect, border_radius=25)
        
        # Button text
        back_text = self.body_font.render("← Back", True, COLORS['text_white'])
        back_text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, back_text_rect)
        
        self.back_button = back_rect
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = pygame.mouse.get_pos()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    
                    # Back button (available in all game states)
                    if (self.current_state != GameState.MENU and 
                        hasattr(self, 'back_button') and self.back_button.collidepoint(pos)):
                        self.current_state = GameState.MENU
                        return
                    
                    if self.current_state == GameState.MENU:
                        if hasattr(self, 'menu_buttons'):
                            for button_rect, state in self.menu_buttons:
                                if button_rect.collidepoint(pos):
                                    self.current_state = state
                                    break
                    
                    elif self.current_state == GameState.TIC_TAC_TOE:
                        self.tic_tac_toe.handle_click(pos)
                    
                    elif self.current_state == GameState.CONNECT_FOUR:
                        self.connect_four.handle_click(pos)
                    
                    elif self.current_state == GameState.GAME_2048:
                        self.game_2048.handle_click(pos)
                    
                    elif self.current_state == GameState.DOTS_AND_BOXES:
                        self.dots_and_boxes.handle_click(pos)
            
            elif event.type == pygame.KEYDOWN:
                if self.current_state == GameState.GAME_2048:
                    self.game_2048.handle_keydown(event)
    
    def update(self):
        if self.current_state == GameState.TIC_TAC_TOE:
            self.tic_tac_toe.update()
        elif self.current_state == GameState.CONNECT_FOUR:
            self.connect_four.update()
        elif self.current_state == GameState.DOTS_AND_BOXES:
            self.dots_and_boxes.update()
    
    def draw(self):
        if self.current_state == GameState.MENU:
            self.draw_menu()
        elif self.current_state == GameState.TIC_TAC_TOE:
            self.draw_gradient_background()
            self.draw_back_button()
            self.tic_tac_toe.draw(self.mouse_pos, self.body_font, self.title_font, self.subheading_font)
        elif self.current_state == GameState.CONNECT_FOUR:
            self.draw_gradient_background()
            self.draw_back_button()
            self.connect_four.draw(self.mouse_pos, self.body_font, self.title_font, self.subheading_font)
        elif self.current_state == GameState.GAME_2048:
            self.draw_gradient_background()
            self.draw_back_button()
            self.game_2048.draw(self.mouse_pos, self.body_font, self.title_font, self.subheading_font)
        elif self.current_state == GameState.DOTS_AND_BOXES:
            self.draw_gradient_background()
            self.draw_back_button()
            self.dots_and_boxes.draw(self.mouse_pos, self.body_font, self.title_font, self.subheading_font, self.caption_font)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        self.running = True
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ModernAIGamesHub()
    game.run()