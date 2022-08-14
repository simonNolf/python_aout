from jeu import Jeu
from plateau import Plateau

taille2 = (9, 9)
plateau = Plateau()
plateau.taille = taille2
tailleEcran = (600, 600)
jeu = Jeu(plateau, tailleEcran)
jeu.run()
