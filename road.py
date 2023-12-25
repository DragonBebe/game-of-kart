from trackblock import TrackBlock
class Road(TrackBlock):
    # Constructeur pour la classe Road.
    def __init__(self, x, y):
        # Appel du constructeur de la classe parent avec des paramètres spécifiques.
        # La couleur (0, 0, 0) correspond à la couleur noire pour la route.
        super().__init__(x, y, (0, 0, 0))

    # Méthode pour dessiner le bloc de route à l'écran.
    def draw(self, screen):
        # Appel de la méthode draw de la classe parent pour effectuer le dessin.
        super().draw(screen)