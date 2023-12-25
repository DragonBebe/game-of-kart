import pygame
import math
from ai import AI

MAX_ANGLE_VELOCITY = 0.08
MAX_ACCELERATION = 0.25
FRICTION = 0.03  # Coefficient de frottement supposé, ajusté en fonction des conditions réelles
check_num = 0
CHECK_POINTS = ["C", "D", "E", "F"]
start_time = None
i = 0


class Kart():  # Vous pouvez ajouter des classes parentes
    """
    Classe implementant l'affichage et la physique du kart dans le jeu
    """

    def __init__(self, controller):
        self.__has_finished = False  # Indicateur pour la boucle while dans track.py
        self.controller = controller
        self.__position = [100, 100]  # Position initiale du kart
        self.__velocity = 0  # Vitesse initiale du kart
        self.__angle = 0  # Angle initial du kart
        self.__angle_velocity = 0  # Vitesse angulaire initiale du kart
        self.__acceleration = 0  # Accélération initiale du kart
        self.__check_p = [0, 0, 0, 0]  # Valeurs initiales pour les points de contrôle
        self.__next_checkpoint_id = 0
        self.__rebrithposition = [100, 100]
        self.__rebrithangle = 0
        self.__message_displayed = False
        self.__start_time = 0
        self.__game_start_time = pygame.time.get_ticks()
        # Définit l'attribut kart du contrôleur pour pointer vers l'instance actuelle de Kart
        # Cela permet à la classe AI d'accéder à l'instance de Kart via le contrôleur
        self.controller.kart = self

    # Utilise a AI
    @property
    def position(self):
        return self.__position

    # Utilise a AI
    @property
    def next_checkpoint_id(self):
        return self.__next_checkpoint_id

    # Utilise a AI
    @property
    def angle(self):
        return self.__angle

    # Utilise a Track
    @property
    def has_finished(self):
        return self.__has_finished

    def reset(self, initial_position, initial_orientation):
        self.__has_finished = False
        self.__position = initial_position
        self.__angle = initial_orientation
        self.__velocity = 0
        self.__angle_velocity = 0
        self.__acceleration = 0
        self.__check_p = [0, 0, 0, 0]  # Définir la valeur initiale du point de contrôle
        self.__next_checkpoint_id = 0

    def forward(self):
        # Ici on utilise += pour avoire la passibilite que si on appuei meme temps avance et recule, y'a pas de acceleration sur Kart
        self.__acceleration += MAX_ACCELERATION

    def backward(self):
        self.__acceleration += -MAX_ACCELERATION

    def turn_left(self):
        self.__angle_velocity -= MAX_ANGLE_VELOCITY

    def turn_right(self):
        self.__angle_velocity += MAX_ANGLE_VELOCITY

    def update_position(self, string, screen):
        x = int(self.__position[0] // 50)
        y = int(self.__position[1] // 50)
        rows = string.split('\n')
        if y > len(rows):
            y = len(rows)
        if y < 0:
            y = 0
        if x > len(rows[0]):
            x = len(rows[0])
        if x < 0:
            x = 0
        first_row = rows[y]
        actuel_str = first_row[x]

        #Détermination du hors limites
        if (self.__position[0] < 1 or self.__position[0] > 1285 or self.__position[1] < 1 or self.__position[1] > 785):
            self.__position = self.__rebrithposition * 1
            self.__velocity = 0  # Vitesse initiale du kart
            self.__angle = self.__rebrithangle
            self.__angle_velocity = 0  # Vitesse angulaire initiale du kart
            self.__acceleration = 0  # Accélération initiale du kart
            # self.draw(screen)

        #Gagne du jeu
        elif self.__check_p[3] == 1:
            font = pygame.font.Font(None, 270)  # Créer un objet de police
            text = font.render("Bravo", True, (255, 255, 255))  # Créer une surface de texte
            text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2 - 250))

            screen.fill((0, 0, 0))
            screen.blit(text, text_rect)  # Dessiner du texte à l'écran

            if self.__message_displayed == False:
                # Ce code est utilisé pour afficher bravo pendant 3 secondes après la fin du jeu puis terminer le jeu
                self.__message_displayed = True
                self.__start_time = pygame.time.get_ticks()
                # L'heure de début de l'enregistrement ne sera enregistrée qu'une seule fois
                # print(start_time)
            if self.__message_displayed == True:  # Après avoir affiché le texte, détectez la durée pendant laquelle le texte est affiché

                times = pygame.time.get_ticks()  # Ces trois lignes de code sont utilisées pour enregistrer le temps d'exécution du code.
                times = (times - self.__game_start_time) / 1000

                if pygame.time.get_ticks() - self.__start_time > 3000:
                    print(times)
                    self.__has_finished = True


        #Etat des routes
        elif actuel_str == "R":

            self.__acceleration = self.__acceleration - FRICTION * self.__velocity * math.cos(self.__angle_velocity)
            self.__velocity = self.__acceleration + self.__velocity * math.cos(self.__angle_velocity)

            # 根据速度和角度更新位置
            self.__position[0] += self.__velocity * math.cos(math.radians(self.__angle))
            self.__position[1] += self.__velocity * math.sin(math.radians(self.__angle))

            self.__angle += math.degrees(self.__angle_velocity)  # Mettre à jour l'angle en fonction de la vitesse angulaire actuelle
            self.__angle %= 360  # Gardez l'angle entre 0 et 360 degrés

            # Réinitialise l'accélération et la vitesse angulaire après chaque mise à jour afin qu'elles ne soient pas appliquées à nouveau lors du prochain appel.
            self.__acceleration = 0
            self.__angle_velocity = 0

            # Dessinez le nouvel emplacement de Kart

        #État de l'herbe
        elif actuel_str == "G":
            self.__acceleration = self.__acceleration - 0.2 * self.__velocity * math.cos(self.__angle_velocity)
            self.__velocity = self.__acceleration + self.__velocity * math.cos(self.__angle_velocity)
            self.__position[0] += self.__velocity * math.cos(math.radians(self.__angle))
            self.__position[1] += self.__velocity * math.sin(math.radians(self.__angle))
            self.__angle += math.degrees(self.__angle_velocity)
            self.__angle %= 360
            self.__acceleration = 0
            self.__angle_velocity = 0


        # Conditions magmatiques
        elif actuel_str == "L":
            self.__position = self.__rebrithposition * 1
            self.__velocity = 0
            self.__acceleration = 0
            self.__angle_velocity = 0

        # Etat de checkpoint
        elif actuel_str in ["C", "D", "E", "F"]:
            self.__acceleration = self.__acceleration - FRICTION * self.__velocity * math.cos(self.__angle_velocity)
            self.__velocity = self.__acceleration + self.__velocity * math.cos(self.__angle_velocity)
            # Mettre à jour la position en fonction de la vitesse et de l'angle
            self.__position[0] += self.__velocity * math.cos(math.radians(self.__angle))
            self.__position[1] += self.__velocity * math.sin(math.radians(self.__angle))
            self.__angle += math.degrees(self.__angle_velocity)
            self.__angle %= 360
            self.__acceleration = 0
            self.__angle_velocity = 0

            if actuel_str == "C":
                if self.__check_p[0] == 0:
                    self.__rebrithposition = self.__position * 1
                self.__check_p[0] = 1
                self.__next_checkpoint_id = 1
                self.__rebrithangle = self.__angle * 1

            if actuel_str == "D" and self.__check_p[0] == 1:  # Déterminer si le point de contrôle C a été réussi
                if self.__check_p[1] == 0:
                    self.__rebrithposition = self.__position * 1
                self.__check_p[1] = 1
                self.__next_checkpoint_id = 2
                self.__rebrithangle = self.__angle * 1

            if actuel_str == "E" and self.__check_p[1] == 1:  # Déterminer si le point de contrôle D a été réussi
                if self.__check_p[2] == 0:
                    self.__rebrithposition = self.__position * 1
                self.__check_p[2] = 1
                self.__next_checkpoint_id = 3
                self.__rebrithangle = self.__angle * 1

            if actuel_str == "F" and self.__check_p[2] == 1:  # Déterminer si le point de contrôle E a été franchi
                self.__check_p[3] = 1

        # Situation de la ceinture d'accélération
        elif actuel_str == "B":
            self.__acceleration = self.__acceleration - FRICTION * self.__velocity * math.cos(self.__angle_velocity)
            self.__velocity = 20

            # Mettre à jour la position en fonction de la vitesse et de l'angle
            self.__position[0] += self.__velocity * math.cos(math.radians(self.__angle))
            self.__position[1] += self.__velocity * math.sin(math.radians(self.__angle))

            # Mettre à jour l'angle en fonction de la vitesse angulaire actuelle
            self.__angle += math.degrees(self.__angle_velocity)
            # Gardez l'angle entre 0 et 360 degrés
            self.__angle %= 360

            # Réinitialise l'accélération et la vitesse angulaire après chaque mise à jour afin qu'elles ne soient pas appliquées à nouveau lors du prochain appel.
            self.__acceleration = 0
            self.__angle_velocity = 0

            # Dessinez le nouvel emplacement de Kart

        else:
            pass

    # Fonction de dessin
    def draw(self, screen):
        size1 = 20
        size2 = 10
        # Changez un triangle pour représenter la voiture. Le coin supérieur de la voiture est la direction dans laquelle nous nous dirigeons.
        top_point = (self.__position[0] + size1 * math.cos(math.radians(self.__angle)),
                     self.__position[1] + size1 * math.sin(math.radians(self.__angle)))
        left_point = (self.__position[0] + size2 * math.cos(math.radians(self.__angle + 120)),
                      self.__position[1] + size2 * math.sin(math.radians(self.__angle + 120)))
        right_point = (self.__position[0] + size2 * math.cos(math.radians(self.__angle + 240)),
                       self.__position[1] + size2 * math.sin(math.radians(self.__angle + 240)))
        pygame.draw.polygon(screen, (255, 255, 255), [top_point, left_point, right_point])

