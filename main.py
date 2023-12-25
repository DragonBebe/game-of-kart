from track import Track
from ai import AI
from human import Human
from kart import Kart
# from test import *

# La chaine de caractere decrivant le terrain
string = """GGGGGGGGGGGGGGGGGGGGGGGGGG
GRRRRRRCRRRRRRRRRBRRRRRRRG
GRRRRRRCRRRRRRRRRBRRRRRRRG
GRRRRRRCRRRRRRRRRRRRRRRRRG
GRRRRRRCRRRRRRRRRRRRRRRRRG
GGGGGGGGGGGGGGGGGGGGGRRRRG
GGGGGGGGGGGGGGGGGGGGGRRRRG
GRRRRGGGGGGGGGGGGGGGGRRRRG
GFFRRGGGGGGGGGGGGGGGGRRRRG
GLRRRGGGGGGGGGGGGGGGGRRRRG
GRRRRGGGGGGGGGGGGGGGGDDDDG
GRRRRRERRRRRRRBRRRRRRRRLLG
GRRRRRERRRRRRRBRRRRRRRRRRG
GLRRRRERRRRRGGBRRRRRRRRRRG
GLLRRRERRRRRGGBRRRRRRRRRRG
GGGGGGGGGGGGGGGGGGGGGGGGGG"""

# La position et l'orientation initiale du kart
initial_position = [100, 100]
initial_angle = 0

# On peut lancer la controller, soit par Human(),soit par AI()

# controller = Human()
controller = AI(string)
"""
==================== ATTENTION =====================
Vous ne devez pas modifier ces quatre lignes de code 
====================================================
"""
kart = Kart(controller)
track = Track(string, initial_position, initial_angle)
track.add_kart(kart)
track.play()

