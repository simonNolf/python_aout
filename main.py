import pygame
import random

pygame.init()

LARGEUR, LONGUEUR = 700, 800

win = pygame.display.set_mode((LARGEUR, LONGUEUR))
pygame.display.set_caption("démineur")
couleur_fond = "white"
ROWS, COLS = 15,15
MINES = 30

TAILLE = LARGEUR / ROWS

NUM_FONT = pygame.font.SysFont("comicsans", 20)
NUM_COLORS = {1: "blue", 2: "green", 3: "red", 4: "purple", 5: "yellow", 6: "grey", 7: "brown", 8: "black"}

RECT_COLOR = "white"
RECT_CLIC_COLOR = (140, 140, 140)


def get_voisins(row, col, rows, cols):
    voisins = []

    if row > 0:
        voisins.append((row - 1, col))
    if row < rows - 1:
        voisins.append((row + 1, col))
    if col > 0:
        voisins.append((row, col - 1))
    if col < cols - 1:
        voisins.append((row, col + 1))

    if row > 0 and col > 0:
        voisins.append((row - 1, col - 1))
    if row < rows - 1 and col < cols - 1:
        voisins.append((row + 1, col + 1))
    if row < rows - 1 and col > 0:
        voisins.append((row + 1, col - 1))
    if row > 0 and col < cols - 1:
        voisins.append((row - 1, col + 1))

    return voisins


def creationChampsMine(rows, cols, MINES):
    champ = [[0 for _ in range(cols)] for _ in range(rows)]
    position_mines = set()

    while len(position_mines) < MINES:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        pos = row, col

        if (pos in position_mines):
            continue

        position_mines.add(pos)
        champ[row][col] = -1

    for mine in position_mines:
        voisins = get_voisins(*mine, rows, cols)
        for r, c in voisins:
            champ[r][c] += 1
    return champ


def draw(win, champ, champ_couvert):
    win.fill(couleur_fond)

    for i, row in enumerate(champ):
        y = TAILLE * i
        for j, value in enumerate(row):
            x = TAILLE * j

            couvert = champ_couvert[i][j] == 0

            if couvert:
                pygame.draw.rect(win, RECT_COLOR, (x, y, TAILLE, TAILLE))
                pygame.draw.rect(win, "black", (x, y, TAILLE, TAILLE),2)
                continue
            else:
                pygame.draw.rect(win, RECT_CLIC_COLOR, (x, y, TAILLE, TAILLE))
                pygame.draw.rect(win, "black", (x, y, TAILLE, TAILLE),2)

            if value > 0:
                text = NUM_FONT.render(str(value), 1, NUM_COLORS[value])
                win.blit(text, (x + (TAILLE / 2 - text.get_width() / 2), y + (TAILLE / 2 - text.get_height() / 2)))
    pygame.display.update()


def pos_grille(pos_souris):
    mx, my = pos_souris
    row = int(my // TAILLE)
    col = int(mx // TAILLE)

    return row, col


def main():
    run = True
    champ = creationChampsMine(ROWS, COLS, MINES)
    champ_couvert = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    print(champ)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = pos_grille(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue
                champ_couvert[row][col] = 1
        draw(win, champ, champ_couvert)

    pygame.quit()


if __name__ == "__main__":
    main()
