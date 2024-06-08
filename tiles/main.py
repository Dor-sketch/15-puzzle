import string
import pygame
import asyncio
import random
from tiles import State, AStar

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init(channels=2)

# Load and play music
pygame.mixer.music.load('rain.mp3')
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Constants
TILE_SIZE = 100
GRID_SIZE = 4
WINDOW_SIZE = TILE_SIZE * GRID_SIZE + 400  # Additional space for buttons
BUTTON_HEIGHT = 40

# Colors
BACKGROUND_COLOR = (0, 0, 0)  # Black
BUTTON_COLOR = (0, 50, 0)  # Dark Green
BUTTON_TEXT_COLOR = (0, 255, 0)  # Bright Green
BUTTON_COLOR_LIGHT = (0, 100, 0)  # Slightly lighter Dark Green
TILE_COLOR = (0, 10, 0)  # Dark Green
TILE_COLOR_LIGHT = (199, 255, 255)  # Bright Green
SHADOW_COLOR = (0, 0, 0, 50)  # Shadow color with some transparency
BLACK = (0, 0, 0)  # Black
MATRIX_GREEN = (0, 160, 0)  # Matrix Green
TEXT_COLOR = MATRIX_GREEN  # Matrix Green
GREEN = (0, 255, 0)  # Bright Green
TILES_TEXT_COLOR = GREEN  # Bright Green

# Fonts
font_path = "font.ttf"
FONT = pygame.font.Font(font_path, TILE_SIZE // 2)
MATRIX_FONT = pygame.font.Font(font_path, 20)
BUTTON_FONT = pygame.font.Font('Courier.ttf', 24)
INSTRUCTIONS_FONT = pygame.font.Font('Courier.ttf', 14)
MATRIX_GREEN = GREEN

# Initialize position and velocity
pos = [0, WINDOW_SIZE // 1.65]
vel = [random.choice([-1, 1]) * random.uniform(1.5, 2.5), random.choice([-1, 1])
       * random.uniform(1.5, 2.5)]  # Increase the range of random velocities

# Initialize screen
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("8-Puzzle Solver")
grid_width = GRID_SIZE * TILE_SIZE
grid_height = GRID_SIZE * TILE_SIZE
offset_x = (screen.get_width() - grid_width) // 2
offset_y = (screen.get_height() - grid_height) // 2 - 50

# Define buttons
buttons = [
    {"label": "Shuffle", "rect": pygame.Rect(
        10, WINDOW_SIZE - BUTTON_HEIGHT, 100, BUTTON_HEIGHT)},
    {"label": "Shuffle Factor", "rect": pygame.Rect(
        340, WINDOW_SIZE - BUTTON_HEIGHT, 100, BUTTON_HEIGHT)},
    {"label": "Solve", "rect": pygame.Rect(
        230, WINDOW_SIZE - BUTTON_HEIGHT, 100, BUTTON_HEIGHT)},
    {"label": "Reset", "rect": pygame.Rect(
        120, WINDOW_SIZE - BUTTON_HEIGHT, 100, BUTTON_HEIGHT)},
    {"label": "Help", "rect": pygame.Rect(
        450, WINDOW_SIZE - BUTTON_HEIGHT, 100, BUTTON_HEIGHT)},
    {"label": "Exit", "rect": pygame.Rect(
        450, WINDOW_SIZE - BUTTON_HEIGHT, 100, BUTTON_HEIGHT)},
]

# Create a lock
lock = asyncio.Lock()


display_instructions = True


async def draw_shadow(surface, rect, shadow_color):
    pygame.draw.rect(surface, shadow_color, rect, border_radius=10)


async def draw_shadow(surface, rect, color):
    shadow_rect = rect.copy()
    shadow_rect.move_ip(5, 5)  # Offset for shadow
    pygame.draw.rect(surface, color, shadow_rect, border_radius=10)

# Create a lookup table for the colors
color_table = {}


async def draw_gradient_rect(surface, rect, start_color, end_color):
    color_rect = pygame.Surface((rect.width, rect.height))

    for y in range(rect.height):
        # If the color is not in the table, calculate it
        if y not in color_table:
            color = (
                start_color[0] + (end_color[0] - start_color[0]
                                  ) * y // rect.height,
                start_color[1] + (end_color[1] - start_color[1]
                                  ) * y // rect.height,
                start_color[2] + (end_color[2] - start_color[2]
                                  ) * y // rect.height,
            )
            color_table[y] = color

        pygame.draw.line(color_rect, color_table[y], (0, y), (rect.width, y))

    surface.blit(color_rect, rect.topleft)


class MatrixRain:
    def __init__(self, x, y, color, speed, start_delay=0, font=MATRIX_FONT):
        self.x = x
        self.y = y - start_delay
        self.font = font
        self.color = color
        self.speed = speed
        self.trail = []
        self.reset_delay = 0
        self.max_trail_length = random.randint(
            5, screen.get_height() // self.font.get_height())

    async def fall(self, surface):
        if self.reset_delay > 0:
            self.reset_delay -= 1
            return
        self.y += self.speed
        katakana = 'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
        characters = string.ascii_letters + string.digits + \
            string.punctuation + ' ' + katakana
        text_surface = self.font.render(
            random.choice(characters), True, self.color)
        text_surface.convert_alpha()  # Create a surface that supports per-pixel alpha
        self.trail.append(text_surface)
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        for i, text in enumerate(self.trail[::-1]):
            # Calculate the alpha value based on the reversed position in the trail
            alpha = int(
                255 * (0.6 + 0.4 * ((len(self.trail) - i) / len(self.trail))))
            # Create a new surface with the same size as the text surface
            alpha_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
            # Fill the new surface with white color and the calculated alpha value
            alpha_surface.fill((255, 255, 255, alpha))
            # Blend the new surface onto the text surface
            text.blit(alpha_surface, (0, 0),
                      special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(text, (self.x, self.y - i * text.get_height()))
        if self.y > WINDOW_SIZE:
            self.y = 0
            self.trail = []
            self.reset_delay = random.randint(0, int(1 // self.speed + 0.1))


# Calculate the number of lines based on the window size and the width of a character
# Increase the divisor to reduce the number of lines
# Increase the divisor# Initialize Matrix rain
num_lines = min((WINDOW_SIZE // (MATRIX_FONT.size(' ')[0])), 60)
matrix_rain = []
# Initialize position and velocity


for x in range(num_lines):
    char_width = MATRIX_FONT.size(' ')[0] * 2
    # Distribute lines along the screen
    position_x = x * (screen.get_width() // num_lines)
    position_y = 0
    color = MATRIX_GREEN
    speed = random.uniform(2.5, 4.5)
    start_delay = random.randint(0, WINDOW_SIZE // 2)

    rain = MatrixRain(position_x, position_y, color, speed, start_delay)
    matrix_rain.append(rain)


async def play_sound():
    # Load the sound
    thunder_sound = pygame.mixer.Sound('my_thunder.mp3')
    thunder_sound.set_volume(0.5)
    # Get a free channel
    channel = pygame.mixer.find_channel()
    # Play the sound on the channel
    if channel:
        channel.play(thunder_sound)
winner_text_str = "Congratulations, you solved the puzzle!"
winner_text = BUTTON_FONT.render(winner_text_str, True, TILES_TEXT_COLOR)
visible_chars = [True] * len(winner_text_str)
winner_text_surface = BUTTON_FONT.render(winner_text_str, True, GREEN)


async def draw_winner_text(surface):
    # Update position
    pos[0] += vel[0]
    pos[1] += vel[1]

    # Reverse direction if the text hits the edge of the screen
    async with lock:
        if (pos[0] <= 0 and vel[0] < 0) or (pos[0] + winner_text.get_width() >= WINDOW_SIZE and vel[0] > 0):
            vel[0] = -vel[0]
        if (pos[1] <= 0 and vel[1] < 0) or (pos[1] + winner_text.get_height() >= WINDOW_SIZE and vel[1] > 0):
            vel[1] = -vel[1]

    # Create a semi-transparent surface
    trans_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE), pygame.SRCALPHA)

    # Draw a semi-transparent rectangle on the surface
    pygame.draw.rect(trans_surface, (50, 50, 50, 128), pygame.Rect(
        pos[0] - 10, pos[1] - 10, winner_text.get_width() + 20, winner_text.get_height() + 20))

    # Blit the semi-transparent surface onto the screen
    screen.blit(trans_surface, (0, 0))

    # Randomly hide a character
    visible_chars[random.randint(0, len(visible_chars) - 1)] = False
    if all(visible_chars) is False:
        visible_chars[random.randint(0, len(visible_chars) - 1)] = True

    # Blit the text onto the screen, but only the characters that are currently visible
    for i, char in enumerate(winner_text_str):
        if visible_chars[i]:
            char_width = BUTTON_FONT.size(char)[0]
            start_pos = BUTTON_FONT.size(winner_text_str[:i])[0]
            remaining_width = winner_text_surface.get_width() - start_pos
            char_surface = winner_text_surface.subsurface(pygame.Rect(
                start_pos, 0, min(char_width, remaining_width), BUTTON_FONT.get_height()))
            screen.blit(char_surface, (pos[0] + start_pos, pos[1]))


class PuzzleGUI:
    def __init__(self, state):
        self.display_instructions = False
        self.difficulty = 30
        self.initial_state = state
        self.state = state
        self.tiles = state.numbers
        self.solution_steps = []
        self.solution_index = 0
        self.hasPlayed = False

    def shuffle(self):
        self.hasPlayed = False
        num_moves = self.difficulty
        # turn back to solved state
        self.state = State([i for i in range(GRID_SIZE ** 2)])
        # Assuming the grid is square
        grid_width = int(len(self.state.numbers) ** 0.5)
        for _ in range(num_moves):
            blank_index = self.state.numbers.index(0)
            blank_x, blank_y = divmod(blank_index, grid_width)
            neighbors = [(nx, ny) for nx, ny in [(blank_x-1, blank_y), (blank_x+1, blank_y), (blank_x, blank_y-1), (blank_x, blank_y+1)]
                         if 0 <= nx < grid_width and 0 <= ny < grid_width]
            swap_x, swap_y = random.choice(neighbors)
            swap_index = swap_x * grid_width + swap_y
            self.state.numbers[blank_index], self.state.numbers[swap_index] = self.state.numbers[swap_index], self.state.numbers[blank_index]
        # Create a new State object
        self.initial_state = State(self.state.numbers[:])
        self.state = self.initial_state
        self.tiles = self.state.numbers

    def reset(self):
        self.state = self.initial_state
        self.tiles = self.state.numbers
        self.solution_steps = []
        self.solution_index = 0

    def get_blank_tile_rect(self):
        blank_x, blank_y = self.state.find_number_in_matrix(0)
        return pygame.Rect(blank_y * TILE_SIZE + offset_x, blank_x * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE)

    def get_neighbors_of_blank_tile(self):
        blank_x, blank_y = self.state.find_number_in_matrix(0)
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = blank_x + dx, blank_y + dy
            if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                neighbors.append((x, y))
        return neighbors

    def solve(self):
        self.solution_steps = AStar(self.state).search().get_path()
        self.solution_index = 0

    async def draw_instructions(self, screen):
        # Create a semi-transparent surface that covers the entire screen
        instructions_surface = pygame.Surface(
            screen.get_size(), pygame.SRCALPHA)
        # RGBA color, 200 for alpha means semi-transparent
        instructions_surface.fill((0, 0, 0, 180))

        # Define instructions
        instructions = {
            "Shuffle": "Click 'Shuffle' to randomly rearrange the tiles in the puzzle.",
            "Reset": "Click 'Reset' to return the puzzle to its original, solved state.",
            "Solve": "Click 'Solve' to automatically solve the puzzle. Watch as the tiles move into place!",
            "Shuffle Factor": "Click 'x' to adjust the difficulty of the puzzle. Higher values will result in a more challenging puzzle.",
            "Exit": "Click 'Exit' to close the game. Your progress will not be saved.",
            "Blank Tile": "Click a cell next to the blank tile to move it."}
        # Define line height
        LINE_HEIGHT = INSTRUCTIONS_FONT.get_height()
        # Calculate the space between instructions
        space_between_instructions = screen.get_width() // (len(buttons)-1)
        index = 0
        # Draw instruction above each button
        for button in buttons:
            button_rect = button["rect"]
            instruction_text = instructions.get(button["label"], "")
            if instruction_text:
                text_surface = INSTRUCTIONS_FONT.render(
                    instruction_text, True, BUTTON_TEXT_COLOR, wraplength=space_between_instructions-20)
                # Adjust the vertical position here
                text_rect = text_surface.get_rect(
                    left=(10 + space_between_instructions * index), top=button_rect.top - 170)
                instructions_surface.blit(text_surface, text_rect)
                index += 1
                # Draw a rectangle around the button
                # Adjust the color and thickness as needed
                pygame.draw.rect(instructions_surface,
                                 (255, 255, 255), button_rect, 2)
        # Draw instruction for the blank tile
        blank_tile_instruction = instructions.get("Blank Tile", "")
        if blank_tile_instruction:
            # You need to implement this function
            blank_tile_rect = self.get_blank_tile_rect()
            text_surface = INSTRUCTIONS_FONT.render(
                blank_tile_instruction, True, BUTTON_TEXT_COLOR, wraplength=screen.get_width() // 2)
            # draw center above the puzzle
            # Adjust the vertical position here
            text_rect = text_surface.get_rect(
                center=(screen.get_width() // 2, 130))
            instructions_surface.blit(text_surface, text_rect)
            # Draw a bold rectangle around the neighboring cells
            # You need to implement this function
            neighbors = self.get_neighbors_of_blank_tile()
            for neighbor in neighbors:
                # If neighbor is a tuple in the form (x, y)
                neighbor_rect = pygame.Rect(
                    neighbor[1] * TILE_SIZE + offset_x, neighbor[0] * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE)
                # Adjust the color and thickness as needed
                pygame.draw.rect(instructions_surface,
                                 (255, 255, 255), neighbor_rect, 2)

        # Blit the instructions surface onto the main screen
        screen.blit(instructions_surface, (0, 0))

    async def draw(self):
        screen.fill((33, 33, 33))  # Background color

        # Call draw_instructions to display instructions

        for falling_line in matrix_rain:
            await falling_line.fall(screen)  # Increase speed
        # Draw tiles with shadows and gradients
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile = self.tiles[i * GRID_SIZE + j]
                if tile == 0:
                    continue
                rect = pygame.Rect(j * TILE_SIZE + offset_x,
                                   i * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE)
                await draw_shadow(screen, rect, SHADOW_COLOR)
                await draw_gradient_rect(screen, rect, TILE_COLOR, TILE_COLOR_LIGHT)
                text = FONT.render(str(tile), True, TILES_TEXT_COLOR)
                screen.blit(
                    text,
                    (
                        rect.x + rect.width // 2 - text.get_width() // 2,
                        rect.y + rect.height // 2 - text.get_height() // 2,
                    ),
                )

        button_space = 10  # Space between buttons
        total_button_width = sum(
            button["rect"].width + button_space for button in buttons) - button_space
        start_x = (screen.get_width() - total_button_width) // 2

        for button in buttons:
            button_rect = button["rect"]
            button_rect.x = start_x
            button_rect.y = WINDOW_SIZE - button_rect.height - 10  # 10 pixels from the bottom
            await draw_shadow(screen, button_rect.move(5, 5), SHADOW_COLOR)
            await draw_gradient_rect(screen, button_rect, BUTTON_COLOR, BUTTON_COLOR_LIGHT)
            text = BUTTON_FONT.render(button["label"], True, BUTTON_TEXT_COLOR)
            if button["label"] == "Shuffle Factor":
                text = BUTTON_FONT.render(
                    f"x{self.difficulty}", True, BUTTON_TEXT_COLOR)
            screen.blit(
                text,
                (
                    button_rect.x + button_rect.width // 2 - text.get_width() // 2,
                    button_rect.y + button_rect.height // 2 - text.get_height() // 2,
                ),
            )
            start_x += button_rect.width + button_space  # Move to the next button position

        if self.state.numbers in [[i for i in range(GRID_SIZE ** 2)], [i for i in range(GRID_SIZE ** 2)][::-1]]:
            if self.hasPlayed == False:
                await play_sound()
                self.hasPlayed = True
            await draw_winner_text(screen)
        if self.display_instructions:
            await self.draw_instructions(screen)
        # Blit the objects surface onto the main screen
        screen.blit(screen, (0, 0))

        pygame.display.update()

    def handle_click(self, pos):
        if self.display_instructions:
            self.display_instructions = False
        x, y = pos
        if y < TILE_SIZE * GRID_SIZE + offset_y:  # Include offset_y in the condition
            # Subtract offsets before division
            tile_y, tile_x = (
                x - offset_x) // TILE_SIZE, (y - offset_y) // TILE_SIZE
            blank_x, blank_y = self.state.find_number_in_matrix(0)
            if (tile_x == blank_x and abs(tile_y - blank_y) == 1) or (tile_y == blank_y and abs(tile_x - blank_x) == 1):
                tile_index, blank_index = tile_x * GRID_SIZE + \
                    tile_y, blank_x * GRID_SIZE + blank_y
                new_numbers = self.state.numbers[:]
                new_numbers[tile_index], new_numbers[blank_index] = new_numbers[blank_index], new_numbers[tile_index]
                self.state = State(new_numbers)
                self.tiles = self.state.numbers
        else:
            for button in buttons:
                if button["rect"].collidepoint(pos):
                    if button["label"] == "Shuffle":
                        self.shuffle()
                    elif button["label"] == "Reset":
                        self.reset()
                    elif button["label"] == "Solve":
                        self.solve()
                    elif button["label"] == "Shuffle Factor":
                        self.difficulty = (self.difficulty + 1) % 60
                    elif button["label"] == "Help":
                        self.display_instructions = not self.display_instructions
                    elif button["label"] == "Exit":
                        pygame.quit()
                        exit()

    def step_solution(self):
        if self.solution_steps and self.solution_index < len(self.solution_steps):
            step = self.solution_steps[self.solution_index]
            blank_x, blank_y = self.state.find_number_in_matrix(0)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x, y = blank_x + dx, blank_y + dy
                if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
                    if self.state.matrix[x][y] == step:
                        new_numbers = self.state.numbers[:]
                        blank_index, new_index = blank_x * GRID_SIZE + blank_y, x * GRID_SIZE + y
                        new_numbers[blank_index], new_numbers[new_index] = new_numbers[new_index], new_numbers[blank_index]
                        self.state = State(new_numbers)
                        self.tiles = self.state.numbers
                        break
            self.solution_index += 1


async def main():
    puzzle = PuzzleGUI(State([i for i in range(GRID_SIZE ** 2)]))
    running = True
    clock = pygame.time.Clock()
    # shuffle the puzzle
    puzzle.shuffle()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                puzzle.handle_click(event.pos)
        await puzzle.draw()
        puzzle.step_solution()

        await asyncio.sleep(0)
        clock.tick(60)

    pygame.quit()


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
