import math
import pygame
import time
import heapq
from player import Player

MAX_ANGLE_VELOCITY = 0.05
BLOCK_SIZE = 50


"""
# Nous avons constaté que lorsque l'IA utilise la distance de Manhattan, 
  il peut atteindre le point final de manière plus stable, mais sa vitesse est relativement lente.
  
# Lorsque vous utilisez la distance euclidienne, 
  vous pouvez atteindre le point final plus rapidement, 
  mais lorsque la carte est plus complexe, elle touchera parfois le magma, 
  ce qui vous fera perdre du temps et ne parviendra même pas à atteindre le point final.
  
# Si nous constatons que nous ne pouvons pas atteindre le point final, 
  nous pouvons choisir de basculer entre la distance de Manhattan et la distance euclidienne

"""

class AI(Player):

    def __init__(self, game_map):
        self.kart = None
        self.__game_map = game_map.split("\n")
        self.__checkpoints = ['C', 'D', 'E', 'F']
        self.__flag = True
        self.__num_point = 0
        self.__path1 = (2, 2)

    def __get_neighbors(self, node):
        # liste de voisins lorsque nous utilisons la distance euclidienne
        # directions = [(0, -1), (0, 1), (-1, 0), (1, 0),(-1,-1),(-1,1),(1,-1),(1,1)]

        # liste des voisins lorsque nous utilisons la distance de Manhattan
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        neighbors = []
        x, y = node
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(self.__game_map[0]) and 0 <= ny < len(self.__game_map):
                neighbors.append((nx, ny))
        return neighbors

    def __heuristic(self, node, goal):
        # return math.sqrt((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) #Distance euclidienne
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])  # Distance de manhattan

    def __distance(self, current, neighbor):
        # Ce qui est défini ici, c'est le coût de chaque voisin
        # neighbor: les coordonnées d'un voisin
        # current: Les coordonnées du nœud en cours d'évaluation
        x, y = neighbor
        terrain_type = self.__game_map[y][x]
        # Définir le coût de chaque grille
        if terrain_type in ('R'):
            return 1
        elif terrain_type in ('B'):
            return 0.9
        elif terrain_type in ('G'):
            return 3
        elif terrain_type in ('L'):
            return float('inf')
        elif terrain_type in ('C', 'D', 'E', 'F'):
            return 1
        else:
            return float('inf')

    def __find_checkpoint(self, char):
        # Trouver les coordonnées du point de contrôle
        for y, row in enumerate(self.__game_map):
            for x, col in enumerate(row):
                if col == char:
                    return (x, y)
        return None

    def __search(self, start, goal):
        # Initialisation d'une liste vide pour servir d'ensemble ouvert (open_set).
        # Dans l'algorithme A*, cet ensemble est utilisé pour stocker les nœuds à évaluer.
        open_set = []

        # Ajout du point de départ à l'ensemble ouvert.
        # Ici, un tas (file de priorité) est utilisé pour stocker les nœuds,
        # ce qui permet de toujours extraire le nœud ayant le plus petit score f.
        heapq.heappush(open_set, (0, start))

        # Initialisation d'un dictionnaire (came_from) pour stocker le meilleur chemin vers chaque nœud.
        # Ce dictionnaire conserve le nœud précédent pour chaque nœud évalué.
        came_from = {}

        # Initialisation d'un dictionnaire pour les scores g (g_score),
        # qui enregistre la longueur du chemin le plus court de l'origine à chaque nœud.
        # Le score g du point de départ est fixé à 0.
        g_score = {start: 0}

        # Initialisation d'un dictionnaire pour les scores f (f_score),
        # qui enregistre les scores f de chaque nœud (le score g plus le coût heuristique vers le point d'arrivée).
        # Le score f du point de départ est son coût heuristique vers le point d'arrivée.
        f_score = {start: self.__heuristic(start, goal)}

        while open_set:  # Traitement de chaque nœud dans l'ensemble ouvert.
            # Sélection et suppression du nœud ayant le score f le plus bas dans l'ensemble ouvert.
            current = heapq.heappop(open_set)[1]

            if current == goal:  # Si le nœud courant est le nœud cible.
                path = []
                # Construction du chemin en remontant de la cible au départ à l'aide du dictionnaire came_from.
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]  # Retourne le chemin inversé (du départ à la cible).

            # Pour chaque voisin du nœud actuel, calculez le g-score depuis le point de départ en passant par le nœud actuel jusqu'à ce voisin.
            for neighbor in self.__get_neighbors(current):
                tentative_g_score = g_score[current] + self.__distance(current, neighbor)

                # Si le nouveau g-score est inférieur au g-score précédent du nœud voisin, mettez à jour came_from, g_score et f_score.
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.__heuristic(neighbor, goal)
                    # Si le nœud voisin n'est pas dans open_set, ajoutez-le
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # Si le chemin n'est pas trouvé

    def __calcul_trace(self):
        # Utilisez l'algorithme A* pour calculer le chemin optimal et renvoyez un tableau de coordonnées du chemin après intégration.

        start = (int(self.kart.position[0] // 50), int(self.kart.position[1] // 50))
        full_path = [start]
        # Initialiser le chemin complet, y compris le point de départ

        for checkpoint in self.__checkpoints:
            goal = self.__find_checkpoint(checkpoint)
            if goal:
                path = self.__search(start, goal)
                if path:
                    full_path += path[1:]
                    # Ajouter un chemin en supprimant le premier point du chemin (car c'est le point final du chemin précédent)
                    start = goal
                    # Mettre à jour le prochain point de départ

        return full_path

    def move(self,string):  # Contrôler le mouvement de la voiture
        time.sleep(0.01)
        if not self.kart:
            return {pygame.K_UP: False, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}
        if self.__flag:
            self.__path1 = self.__calcul_trace()
            self.__flag = True
        # Mettre à jour le point de contrôle que nous devons passer en fonction de next_checkpoint_id
        if self.kart.next_checkpoint_id == 0:
            self.__checkpoints = ['C', 'D', 'E', 'F']
        if self.kart.next_checkpoint_id == 1:
            self.__checkpoints = ['D', 'E', 'F']
        if self.kart.next_checkpoint_id == 2:
            self.__checkpoints = ['E', 'F']
        if self.kart.next_checkpoint_id == 3:
            self.__checkpoints = ['F']

        """
        Cette methode contient une implementation d'IA tres basique.
        L'IA identifie la position du prochain checkpoint et se dirige dans sa direction.

        :param string: La chaine de caractere decrivant le circuit
        :param screen: L'affichage du jeu
        :param position: La position [x, y] actuelle du kartq
        :param angle: L'angle actuel du kart
        :param velocity: La vitesse [vx, vy] actuelle du kart
        :param next_checkpoint_id: Un entier indiquant le prochain checkpoint a atteindre
        :returns: un tableau de 4 boolean decrivant quelles touches [UP, DOWN, LEFT, RIGHT] activer
        """

        # =================================================
        # D'abord trouver la position du checkpoint
        # =================================================

        # On utilise x et y pour decrire les coordonnees dans la chaine de caractere
        # x indique le numero de colonne
        # y indique le numero de ligne

        if self.__num_point < len(self.__path1):
            x, y = self.__path1[self.__num_point]

        else:
            x, y = self.__path1[-1]

        # print(f"next = {x},{y}")
        self.next_checkpoint_position = [x * BLOCK_SIZE + .5 * BLOCK_SIZE, y * BLOCK_SIZE + .5 * BLOCK_SIZE]
        if self.kart.position[0] // 50 == x and self.kart.position[1] // 50 == y:
            self.__num_point = 1

        # =================================================
        # Ensuite, trouver l'angle vers le checkpoint
        # =================================================

        relative_x = self.next_checkpoint_position[0] - self.kart.position[0]
        relative_y = self.next_checkpoint_position[1] - self.kart.position[1]

        # On utilise la fonction arctangente pour calculer l'angle du vecteur [relative_x, relative_y]
        next_checkpoint_angle = math.atan2(relative_y, relative_x)

        # L'angle relatif correspond a la rotation que doit faire le kart pour se trouver face au checkpoint
        # On applique l'operation (a + pi) % (2*pi) - pi pour obtenir un angle entre -pi et pi
        relative_angle = (next_checkpoint_angle - math.radians(self.kart.angle) + math.pi) % (2 * math.pi) - math.pi

        # =================================================
        # Enfin, commander le kart en fonction de l'angle
        # =================================================
        if relative_angle > MAX_ANGLE_VELOCITY:
            # On tourne a droite
            command = [False, False, False, True]
        elif relative_angle < -MAX_ANGLE_VELOCITY:
            # On tourne a gauche
            command = [False, False, True, False]
        else:
            # On avance
            command = [True, False, False, False]

        key_list = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        keys = {key: command[i] for i, key in enumerate(key_list)}
        return keys
    
    
    
"""
Notre classe AI utilise l'algorithme A* pour calculer le chemin le plus court pour une voiture de course sur la piste, du point de départ à chaque point de contrôle. Pour s'adapter à la 
disposition en grille de la piste, la fonction heuristique utilise la distance de Manhattan pour estimer la distance de la position actuelle au point de contrôle cible. Cela permet à l'IA 
de planifier efficacement les trajets, contournant les obstacles pour trouver des itinéraires efficaces sur la piste.
Nous avons également constaté que l'utilisation de la distance euclidienne comme fonction heuristique permet généralement à l'IA d'atteindre les objectifs plus rapidement. Cependant, cette 
méthode peut sous-estimer la longueur réelle du chemin vers la destination, en particulier sur des pistes complexes avec de nombreux obstacles. Cela peut conduire à des problèmes lorsque l'IA tente 
de suivre des itinéraires apparemment directs mais impraticables, tels que heurter des zones de lave adjacentes ou des frontières. En revanche, bien que la distance de Manhattan ne fournisse pas 
nécessairement l'itinéraire en ligne droite le plus court, elle offre généralement une estimation plus réaliste du chemin dans les pistes à disposition en grille, réduisant ainsi le risque de
collisions ou d'erreurs de parcours.
C'est pour ces raisons que nous avons finalement choisi la distance de Manhattan, et cette découverte souligne l'importance de choisir la bonne fonction heuristique en fonction du contexte d'application.

"""



