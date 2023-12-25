from trackblock import TrackBlock
class Lava(TrackBlock):
    # Constructeur pour la classe Lava.
    def __init__(self, x, y):
        # Appel du constructeur de la classe parent avec des paramètres spécifiques.
        # La couleur (255, 0, 0) correspond à la couleur rouge pour la lave.
        super().__init__(x, y, (255, 0, 0))

    # Méthode pour dessiner le bloc de lave à l'écran.
    def draw(self, screen):
        # Appel de la méthode draw de la classe parent pour effectuer le dessin.
        super().draw(screen)
