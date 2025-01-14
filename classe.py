import random

class Navire:
    def __init__(self, nom, taille):
        self.nom = nom
        self.taille = taille
        self.positions = []  
        self.touches = []

    def est_coule(self):
        return len(self.touches) == self.taille


class Plateau:
    def __init__(self):
        self.grille = [[None for _ in range(10)] for _ in range(10)]
        self.navires = []

    def ajouter_navire(self, navire, positions):
        for x, y in positions:
            self.grille[x][y] = navire
        navire.positions = positions
        self.navires.append(navire)

    def tirer(self, x, y):
        if self.grille[x][y] is None:
            return "manqué"
        navire = self.grille[x][y]
        if (x, y) not in navire.touches:
            navire.touches.append((x, y))
        return "touché" if not navire.est_coule() else "coulé"

    def tous_les_navires_coules(self):
        return all(navire.est_coule() for navire in self.navires)


class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()

    def placer_navires(self):
        navires_info = [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer", 3),
            ("Destroyer", 3),
            ("Sous-marin", 2),
            ("Sous-marin", 2),
        ]
        for nom, taille in navires_info:
            while True:
                positions = self.generer_positions_aleatoires(taille)
                if self.verifier_positions(positions):
                    navire = Navire(nom, taille)
                    self.plateau.ajouter_navire(navire, positions)
                    break

    def generer_positions_aleatoires(self, taille):
        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            x = random.randint(0, 9)
            y = random.randint(0, 10 - taille)
            return [(x, y + i) for i in range(taille)]
        else:
            x = random.randint(0, 10 - taille)
            y = random.randint(0, 9)
            return [(x + i, y) for i in range(taille)]

    def verifier_positions(self, positions):
        for x, y in positions:
            if x < 0 or x >= 10 or y < 0 or y >= 10 or self.plateau.grille[x][y] is not None:
                return False
        return True