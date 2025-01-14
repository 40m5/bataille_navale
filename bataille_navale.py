import tkinter as tk
from tkinter import messagebox
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
            if navire.est_coule():
                return "coulé"
            else:
                return "touché"
        return "déjà touché"

    def tous_les_navires_coules(self):
        return all(navire.est_coule() for navire in self.navires)


class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.plateau = Plateau()

    def placer_navires_aleatoirement(self):
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


class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("Jeu de la Bataille Navale")

        self.joueur = Joueur("Joueur")
        self.ordinateur = Joueur("Ordinateur")
        self.ordinateur.placer_navires_aleatoirement()

        self.orientation = "horizontal"
        self.placement_termine = False

        self.tour_joueur = True

        self.grille_joueur = [[None for _ in range(10)] for _ in range(10)]
        self.grille_ordinateur = [[None for _ in range(10)] for _ in range(10)]

        self.creer_interface()

    def creer_interface(self):
        
        frame_joueur = tk.Frame(self.master, borderwidth=2, relief="groove")
        frame_joueur.grid(row=0, column=0, padx=10, pady=10)
        tk.Label(frame_joueur, text="Votre plateau").grid(row=0, column=0, columnspan=10)
        for i in range(10):
            for j in range(10):
                btn = tk.Button(frame_joueur, width=2, height=1, bg="white",
                                command=lambda x=i, y=j: self.placer_navire(x, y))
                btn.grid(row=i + 1, column=j)
                self.grille_joueur[i][j] = btn

    
        frame_ordinateur = tk.Frame(self.master, borderwidth=2, relief="groove")
        frame_ordinateur.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(frame_ordinateur, text="Plateau de l'ordinateur").grid(row=0, column=0, columnspan=10)
        for i in range(10):
            for j in range(10):
                btn = tk.Button(frame_ordinateur, width=2, height=1, bg="white",
                                command=lambda x=i, y=j: self.tirer(x, y))
                btn.grid(row=i + 1, column=j)
                self.grille_ordinateur[i][j] = btn

        
        self.message = tk.Label(self.master, text="Placez vos navires", fg="blue")
        self.message.grid(row=1, column=0, columnspan=2)

        tk.Button(self.master, text="Horizontal", command=lambda: self.choisir_orientation("horizontal")) \
            .grid(row=2, column=0, padx=5, pady=5)
        tk.Button(self.master, text="Vertical", command=lambda: self.choisir_orientation("vertical")) \
            .grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.master, text="Nouvelle partie", command=self.recommencer_partie) \
            .grid(row=3, column=0, columnspan=2, pady=5)

    def choisir_orientation(self, orientation):
        self.orientation = orientation
        self.message.config(text=f"Orientation : {orientation}")

    def placer_navire(self, x, y):
        if self.placement_termine:
            return

        navires_info = [
            ("Porte-avions", 5),
            ("Croiseur", 4),
            ("Destroyer", 3),
            ("Destroyer", 3),
            ("Sous-marin", 2),
            ("Sous-marin", 2),
        ]

        if len(self.joueur.plateau.navires) < len(navires_info):
            nom, taille = navires_info[len(self.joueur.plateau.navires)]
            positions = self.generer_positions(x, y, taille, self.orientation)
            if self.joueur.verifier_positions(positions):
                navire = Navire(nom, taille)
                self.joueur.plateau.ajouter_navire(navire, positions)
                for px, py in positions:
                    self.grille_joueur[px][py].config(bg="gray")
                if len(self.joueur.plateau.navires) == len(navires_info):
                    self.placement_termine = True
                    self.message.config(text="Tous les navires sont placés. Commencez à tirer !")
            else:
                self.message.config(text="Placement invalide, essayez encore.")

    def generer_positions(self, x, y, taille, orientation):
        if orientation == "horizontal":
            return [(x, y + i) for i in range(taille)]
        else:
            return [(x + i, y) for i in range(taille)]

    def tirer(self, x, y):
        if not self.placement_termine or not self.tour_joueur:
            return

        resultat = self.ordinateur.plateau.tirer(x, y)
        if resultat == "touché":
            self.grille_ordinateur[x][y].config(bg="red")
        elif resultat == "coulé":
            self.grille_ordinateur[x][y].config(bg="black")
        else:
            self.grille_ordinateur[x][y].config(bg="blue")

        if self.ordinateur.plateau.tous_les_navires_coules():
            messagebox.showinfo("Victoire", "Vous avez gagné !")
            self.recommencer_partie()
            return

        self.tour_joueur = False
        self.message.config(text="Tour de l'ordinateur")
        self.master.after(1000, self.tour_ordinateur)

    def tour_ordinateur(self):
        while True:
            x, y = random.randint(0, 9), random.randint(0, 9)
            if self.joueur.plateau.grille[x][y] is None or self.joueur.plateau.grille[x][y] != "touché":
                break

        resultat = self.joueur.plateau.tirer(x, y)
        if resultat == "touché":
            self.grille_joueur[x][y].config(bg="red")
        elif resultat == "coulé":
            self.grille_joueur[x][y].config(bg="black")
        else:
            self.grille_joueur[x][y].config(bg="blue")

        if self.joueur.plateau.tous_les_navires_coules():
            messagebox.showinfo("Défaite", "Vous avez perdu !")
            self.recommencer_partie()
            return

        self.tour_joueur = True
        self.message.config(text="À votre tour")

    def recommencer_partie(self):
        self.master.destroy()
        root = tk.Tk()
        Interface(root)
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()


 
