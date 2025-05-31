import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
RED = (255, 69, 0)
YELLOW = (255, 215, 0)
GREEN = (50, 205, 50)
PURPLE = (138, 43, 226)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)

# Fonts
LARGE_FONT = pygame.font.Font(None, 48)
MEDIUM_FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)

class SpaceHangman:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Hangman")
        self.clock = pygame.time.Clock()
        
        # Space-themed word list
        self.words = [
            "GALAXY", "PLANET", "ASTEROID", "COMET", "NEBULA",
            "SUPERNOVA", "BLACKHOLE", "UNIVERSE", "SATELLITE",
            "METEOR", "ORBIT", "COSMOS", "STELLAR", "QUASAR",
            "PULSAR", "JUPITER", "SATURN", "MERCURY", "VENUS",
            "NEPTUNE", "URANUS", "PLUTO", "MARS", "EARTH"
        ]
        
        self.reset_game()
        self.stars = self.generate_stars()
        
    def generate_stars(self):
        stars = []
        for _ in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            brightness = random.randint(100, 255)
            size = random.randint(1, 3)
            stars.append((x, y, brightness, size))
        return stars
    
    def reset_game(self):
        self.word = random.choice(self.words)
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong = 6
        self.game_over = False
        self.won = False
        
    def draw_background(self):
        # Create a space gradient background
        for y in range(HEIGHT):
            color_ratio = y / HEIGHT
            r = int(25 * (1 - color_ratio))
            g = int(25 * (1 - color_ratio))
            b = int(50 + 100 * (1 - color_ratio))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))
        
        # Draw twinkling stars
        for star in self.stars:
            x, y, brightness, size = star
            # Create twinkling effect
            twinkle = math.sin(pygame.time.get_ticks() * 0.01 + x * 0.1) * 0.3 + 0.7
            alpha = int(brightness * twinkle)
            color = (alpha, alpha, alpha)
            pygame.draw.circle(self.screen, color, (x, y), size)
    
    def draw_spaceship_gallows(self):
        # Draw a futuristic spaceship/platform instead of traditional gallows
        base_x, base_y = 150, 500
        
        # Platform base
        pygame.draw.rect(self.screen, GRAY, (base_x - 50, base_y, 100, 20))
        pygame.draw.rect(self.screen, CYAN, (base_x - 50, base_y, 100, 5))
        
        # Vertical support beam (energy beam)
        for i in range(0, 200, 10):
            alpha = 255 - (i * 2)
            color = (0, alpha, 255) if alpha > 0 else CYAN
            pygame.draw.line(self.screen, color, (base_x, base_y - i), (base_x, base_y - i - 8), 3)
        
        # Horizontal beam
        pygame.draw.line(self.screen, CYAN, (base_x, base_y - 200), (base_x + 150, base_y - 200), 4)
        
        # Energy field generator
        pygame.draw.circle(self.screen, PURPLE, (base_x + 150, base_y - 200), 8)
        
        # Hanging energy field (noose equivalent)
        if self.wrong_guesses > 0:
            pygame.draw.line(self.screen, RED, (base_x + 150, base_y - 192), (base_x + 150, base_y - 150), 2)
    
    def draw_astronaut(self):
        # Draw astronaut parts based on wrong guesses
        x, y = 225, 350
        
        if self.wrong_guesses >= 1:  # Helmet
            pygame.draw.circle(self.screen, WHITE, (x, y), 25, 3)
            pygame.draw.circle(self.screen, CYAN, (x, y), 20, 2)
            # Visor reflection
            pygame.draw.arc(self.screen, BLUE, (x-15, y-15, 30, 30), 0, math.pi, 2)
        
        if self.wrong_guesses >= 2:  # Body
            pygame.draw.rect(self.screen, WHITE, (x-15, y+25, 30, 40), 0, 5)
            # Control panel
            pygame.draw.rect(self.screen, RED, (x-10, y+30, 8, 8))
            pygame.draw.rect(self.screen, GREEN, (x+2, y+30, 8, 8))
        
        if self.wrong_guesses >= 3:  # Left arm
            pygame.draw.line(self.screen, WHITE, (x-15, y+35), (x-35, y+50), 5)
        
        if self.wrong_guesses >= 4:  # Right arm
            pygame.draw.line(self.screen, WHITE, (x+15, y+35), (x+35, y+50), 5)
        
        if self.wrong_guesses >= 5:  # Left leg
            pygame.draw.line(self.screen, WHITE, (x-8, y+65), (x-20, y+90), 5)
        
        if self.wrong_guesses >= 6:  # Right leg
            pygame.draw.line(self.screen, WHITE, (x+8, y+65), (x+20, y+90), 5)
            # Add distress effects when complete
            for i in range(5):
                spark_x = x + random.randint(-30, 30)
                spark_y = y + random.randint(-20, 20)
                pygame.draw.circle(self.screen, RED, (spark_x, spark_y), 2)
    
    def draw_word(self):
        display_word = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                display_word += letter + " "
            else:
                display_word += "_ "
        
        # Create a glowing text effect
        text = LARGE_FONT.render(display_word, True, CYAN)
        glow_text = LARGE_FONT.render(display_word, True, WHITE)
        
        # Draw glow effect
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    self.screen.blit(glow_text, (WIDTH//2 - text.get_width()//2 + dx, 150 + dy))
        
        self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 150))
    
    def draw_guessed_letters(self):
        if self.guessed_letters:
            wrong_letters = [letter for letter in self.guessed_letters if letter not in self.word]
            if wrong_letters:
                text = MEDIUM_FONT.render("Wrong: " + " ".join(sorted(wrong_letters)), True, RED)
                self.screen.blit(text, (50, 600))
        
        # Show remaining guesses
        remaining = self.max_wrong - self.wrong_guesses
        color = RED if remaining <= 2 else YELLOW if remaining <= 4 else GREEN
        text = MEDIUM_FONT.render(f"Life Support: {remaining}", True, color)
        self.screen.blit(text, (WIDTH - 200, 600))
    
    def draw_instructions(self):
        instructions = [
            "Save the astronaut from the void of space!",
            "Type letters to guess the space-themed word",
            "Press 5 to restart, ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = SMALL_FONT.render(instruction, True, WHITE)
            self.screen.blit(text, (50, 50 + i * 25))
    
    def draw_game_over(self):
        if self.game_over:
            # Create semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            if self.won:
                message = "MISSION SUCCESSFUL!"
                color = GREEN
                sub_message = "The astronaut is safe!"
            else:
                message = "MISSION FAILED!"
                color = RED
                sub_message = f"The word was: {self.word}"
            
            # Main message
            text = LARGE_FONT.render(message, True, color)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            
            # Sub message
            sub_text = MEDIUM_FONT.render(sub_message, True, WHITE)
            self.screen.blit(sub_text, (WIDTH//2 - sub_text.get_width()//2, HEIGHT//2))
            
            # Restart instruction
            restart_text = MEDIUM_FONT.render("Press 5 to restart", True, YELLOW)
            self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    
    def handle_guess(self, letter):
        if letter.isalpha() and len(letter) == 1:
            letter = letter.upper()
            if letter not in self.guessed_letters:
                self.guessed_letters.add(letter)
                if letter not in self.word:
                    self.wrong_guesses += 1
                
                # Check win condition
                if all(letter in self.guessed_letters for letter in self.word):
                    self.won = True
                    self.game_over = True
                
                # Check lose condition
                if self.wrong_guesses >= self.max_wrong:
                    self.game_over = True
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_5:
                        self.reset_game()
                    elif not self.game_over:
                        self.handle_guess(event.unicode)
            
            # Draw everything
            self.draw_background()
            self.draw_instructions()
            self.draw_spaceship_gallows()
            self.draw_astronaut()
            self.draw_word()
            self.draw_guessed_letters()
            self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = SpaceHangman()
    game.run()