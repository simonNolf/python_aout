import pygame
import os


class Jeu():
    def __init__(self, plateau, tailleEcran):
        self.plateau = plateau
        self.tailleEcran = tailleEcran
        self.taillePiece = self.tailleEcran[0] // self.plateau.getTaille()[1], self.tailleEcran[1] // self.plateau.getTaille()[0]
        self.chargementImage()
    def run(self):
        pygame.init()
        self.ecran = pygame.display.set_mode(self.tailleEcran)
        running = True
        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    running = False
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        hautGauche = (0, 0)
        for row in range(self.plateau.getTaille()[0]):
            for col in range(self.plateau.getTaille()[1]):
                image = self.images["bloc_vide"]
                self.ecran.blit(image, hautGauche)
                hautGauche = hautGauche[0] + self.taillePiece[0], hautGauche[1]
            hautGauche = 0, hautGauche[1] + self.taillePiece[1]

    def chargementImage(self):
        self.images = {}
        for fileName in os.listdir("images"):
            if (not fileName.endswith(".png")):
                continue
            image = pygame.image.load(r"images/" + fileName)
            image = pygame.transform.scale(image, self.taillePiece)
            self.images[fileName.split(".")[0]] = image
