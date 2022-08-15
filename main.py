import time
import pygame
import random
from queue import Queue

pygame.init()

LARGEUR, LONGUEUR = 700, 800

win = pygame.display.set_mode((LARGEUR, LONGUEUR))
pygame.display.set_caption("démineur")
couleur_fond = "white"
ROWS, COLS = 15, 15
MINES = 30

TAILLE = LARGEUR / ROWS

NUM_FONT = pygame.font.SysFont("comicsans", 20)
NUM_COLORS = {1: "blue", 2: "green", 3: "red", 4: "purple", 5: "yellow", 6: "grey", 7: "brown", 8: "black"}

RECT_COLOR = "white"
RECT_CLIC_COLOR = (140, 140, 140)
DRAP_COLOR = "green"
BOMBE_COLOR = "red"
PERDU = pygame.font.SysFont("comicsans", 50)
TEMPS = pygame.font.SysFont("comicsans", 50)


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
            if champ[r][c] != -1:
                champ[r][c] += 1
    return champ


def grille(win, champ, champ_couvert, temps):
    win.fill(couleur_fond)

    temps_text = TEMPS.render(f"Temps  passé : {round(temps)}", 1, "black")
    win.blit(temps_text, (10, LONGUEUR - temps_text.get_height()))

    for i, row in enumerate(champ):
        y = TAILLE * i

        for j, value in enumerate(row):
            x = TAILLE * j

            couvert = champ_couvert[i][j] == 0
            drapeau = champ_couvert[i][j] == -2
            bombe = champ_couvert[i][j] == -1

            if drapeau:
                pygame.draw.rect(win, DRAP_COLOR, (x, y, TAILLE, TAILLE))
                pygame.draw.rect(win, "black", (x, y, TAILLE, TAILLE), 2)
                continue

            if couvert:
                pygame.draw.rect(win, RECT_COLOR, (x, y, TAILLE, TAILLE))
                pygame.draw.rect(win, "black", (x, y, TAILLE, TAILLE), 2)
                continue

            else:
                pygame.draw.rect(win, RECT_CLIC_COLOR, (x, y, TAILLE, TAILLE))
                pygame.draw.rect(win, "black", (x, y, TAILLE, TAILLE), 2)

                if bombe:
                    print("coucou1")
                    pygame.draw.circle(win, BOMBE_COLOR, (x + TAILLE / 2, y + TAILLE / 2), TAILLE / 2 - 4)
                    print("coucou")


            if value > 0:
                text = NUM_FONT.render(str(value), 1, NUM_COLORS[value])
                win.blit(text, (x + (TAILLE / 2 - text.get_width() / 2), y + (TAILLE / 2 - text.get_height() / 2)))

    pygame.display.update()


def pos_grille(pos_souris):
    mx, my = pos_souris
    row = int(my // TAILLE)
    col = int(mx // TAILLE)

    return row, col


def pos_pas_couverte(row, col, champ_couvert, champ):
    q = Queue()
    q.put((row, col))
    visite = set()

    while not q.empty():
        actuel = q.get()

        voisins = get_voisins(*actuel, ROWS, COLS)
        for r, c in voisins:
            if (r, c) in visite:
                continue
            valeur = champ[r][c]
            if valeur == 0 and champ_couvert[r][c] != -2:
                q.put((r, c))

            if champ_couvert[r][c] != -2:
                champ_couvert[r][c] = 1

            visite.add((r, c))

def perdu(win, text):

    text = PERDU.render(text, 1, "black")
    win.blit(text, (LARGEUR / 2 - text.get_width() / 2, LONGUEUR / 2 - text.get_height() / 2))
    pygame.display.update()


def main():

    run = True
    champ = creationChampsMine(ROWS, COLS, MINES)
    champ_couvert = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    drapeau = MINES
    clic = 0
    perd = False
    temps_debut = 0
    temps = 0

    while run:
        if temps_debut > 0:
            temps = time.time() - temps_debut

        else:
            temps_debut = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = pos_grille(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue

                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0] and champ_couvert[row][col] != -2:
                    champ_couvert[row][col] = 1

                    if champ[row][col] == -1:
                        perd = True

                    if clic == 0 or champ[row][col] == 0:
                        pos_pas_couverte(row, col, champ_couvert, champ)
                        if clic == 0:
                            temps_debut = time.time()
                    clic += 1
                elif mouse_pressed[2]:
                    if champ_couvert[row][col] == -2:
                        champ_couvert[row][col] = 0
                        drapeau += 1
                    else:
                        drapeau -= 1
                        champ_couvert[row][col] = -2

        if perd:
            grille(win, champ, champ_couvert, temps)
            perdu(win, "Perdu, essaye encore...")
            pygame.time.delay(5000)
            champ = creationChampsMine(ROWS, COLS, MINES)
            champ_couvert = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            drapeau = MINES
            clic = 0
            perd = False

        grille(win, champ, champ_couvert, temps)

    pygame.quit()

if __name__ == "__main__":
    main()