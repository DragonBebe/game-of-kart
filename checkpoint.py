from trackblock import TrackBlock
class Checkpoint(TrackBlock):
    # Constructeur pour la classe Checkpoint.
    def __init__(self, x, y, checkpoint_id):
        # Appel du constructeur de la classe parent avec des paramètres spécifiques.
        # La couleur (128, 128, 128) correspond à la couleur grise pour le checkpoint.
        super().__init__(x, y, (128, 128, 128))  # checkpoint color
        # Enregistrement de l'ID du checkpoint.
        self.checkpoint_id = checkpoint_id
    # Méthode pour dessiner le checkpoint à l'écran.
    def draw(self, screen):
        # Appel de la méthode draw de la classe parent pour effectuer le dessin.
        super().draw(screen)