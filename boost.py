from trackblock import TrackBlock
class Boost(TrackBlock):
    # Constructeur pour la classe Boost.
    def __init__(self, x, y):
        # Appel du constructeur de la classe parent avec des paramètres spécifiques.
        # La couleur (255, 255, 0) correspond à la couleur jaune pour l'effet de boost.
        super().__init__(x, y, (255, 255, 0))
# Méthode pour dessiner le bloc de boost à l'écran.
    def draw(self, screen):
        super().draw(screen)