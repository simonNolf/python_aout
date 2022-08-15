import pygame
import random

pygame.init()

LARGEUR, LONGUEUR = 700, 800

win = pygame.display.set_mode((LARGEUR, LONGUEUR))
pygame.display.set_caption("démineur")
couleur_fond = "white"
ROWS, COLS = 30, 30
MINES = 30


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


def draw(win):
    win.fill(couleur_fond)
    pygame.display.update()


def main():
    run = True
    champ = creationChampsMine(ROWS, COLS, MINES)
    print(champ)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(win)

    pygame.quit()


if __name__ == "__main__":
    main()
