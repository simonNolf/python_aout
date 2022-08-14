class Plateau():
    def __int__(self, taille):
        self.taille = taille
        self.setTableau()

    def setTableau(self):
        self.tableau = []
        for row in range(self.taille[0]):
            row = []
            for col in range(self.taille[1]):
                piece = None
                row.append(piece)
                self.plateau.append(row)

    def getTaille(self):
        return self.taille
