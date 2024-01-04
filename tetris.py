import pygame
import random

# Inizializzazione Pygame
pygame.init()

# Costanti
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
FPS = 60
BLACK = (0, 0, 0)
FALL_SPEED = 0.5  # Puoi regolare questo valore per cambiare la velocità di discesa
POINTS_PER_LINE = 1  # Punteggio per ogni riga completata
WINNING_SCORE = 10  # Punteggio necessario per vincere

# Inizializzazione finestra di gioco
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# Definizione dei pezzi di Tetris
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

# Associa un colore univoco a ciascun tipo di pezzo
PIECE_COLORS = {
    0: (255, 0, 0),      # Rosso
    1: (0, 255, 0),      # Verde
    2: (0, 0, 255),      # Blu
    3: (255, 255, 0),    # Giallo
    4: (255, 165, 0),    # Arancione
    5: (128, 0, 128),    # Viola
    6: (0, 255, 255)     # Ciano
}

# Inizializzazione griglia di gioco
grid = [[0] * (WIDTH // GRID_SIZE) for _ in range(HEIGHT // GRID_SIZE)]

def draw_grid():
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != 0:
                color = PIECE_COLORS[grid[row][col] - 1]  # -1 per ottenere l'ID corretto
                pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_piece(piece, offset, piece_id):
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col] == 1:
                color = PIECE_COLORS[piece_id]
                pygame.draw.rect(screen, color, ((offset[0] + col) * GRID_SIZE, (offset[1] + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BLACK, ((offset[0] + col) * GRID_SIZE, (offset[1] + row) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def check_collision(piece, offset):
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col] == 1:
                if offset[1] + row >= len(grid) or offset[0] + col < 0 or offset[0] + col >= len(grid[0]) or grid[offset[1] + row][offset[0] + col] != 0:
                    return True
    return False

def merge_piece(piece, offset, piece_id):
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col] == 1:
                grid[offset[1] + row][offset[0] + col] = piece_id + 1  # +1 per ottenere l'ID corretto

def remove_completed_rows():
    completed_rows = [row for row in range(len(grid)) if all(grid[row])]
    for row in completed_rows:
        del grid[row]
        grid.insert(0, [0] * len(grid[0]))
    return len(completed_rows)

def rotate_piece(piece):
    return [[piece[j][i] for j in range(len(piece))] for i in range(len(piece[0]) - 1, -1, -1)]

def display_message(message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 255, 255))
    screen.blit(text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Mostra il messaggio per 2 secondi
    pygame.quit()
    quit()

def main():
    current_piece = random.choice(SHAPES)
    piece_id = SHAPES.index(current_piece)  # Ottieni l'ID del pezzo corrente
    piece_offset = [len(grid[0]) // 2 - len(current_piece[0]) // 2, 0]

    fall_time = 0
    score = 0

    while True:
        dt = clock.tick(FPS) / 1000  # Ottieni il tempo trascorso in secondi

        fall_time += dt

        if fall_time >= FALL_SPEED:
            fall_time = 0

            new_offset = [piece_offset[0], piece_offset[1] + 1]
            if not check_collision(current_piece, new_offset):
                piece_offset = new_offset
            else:
                merge_piece(current_piece, piece_offset, piece_id)
                lines_cleared = remove_completed_rows()
                score += lines_cleared * POINTS_PER_LINE

                if score >= WINNING_SCORE:
                    display_message("Hai vinto!")

                current_piece = random.choice(SHAPES)
                piece_id = SHAPES.index(current_piece)
                piece_offset = [len(grid[0]) // 2 - len(current_piece[0]) // 2, 0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_offset = [piece_offset[0] - 1, piece_offset[1]]
                    if not check_collision(current_piece, new_offset):
                        piece_offset = new_offset
                elif event.key == pygame.K_RIGHT:
                    new_offset = [piece_offset[0] + 1, piece_offset[1]]
                    if not check_collision(current_piece, new_offset):
                        piece_offset = new_offset
                elif event.key == pygame.K_DOWN:
                    new_offset = [piece_offset[0], piece_offset[1] + 1]
                    if not check_collision(current_piece, new_offset):
                        piece_offset = new_offset
                elif event.key == pygame.K_UP:
                    rotated_piece = rotate_piece(current_piece)
                    if not check_collision(rotated_piece, piece_offset):
                        current_piece = rotated_piece

        screen.fill(BLACK)
        draw_grid()
        draw_piece(current_piece, piece_offset, piece_id)

        # Mostra il punteggio
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Punteggio: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()
