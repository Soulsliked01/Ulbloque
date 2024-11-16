"""
Nom: Perera Gonzalez
Prénom: Maxence
Matricule: 590023

"""


from sys import argv
from getkey import getkey

# corespond au .nombre de colones et lignes délimitant la carte du jeu
NBR_SIDE_LINES = NBR_SIDE_COLUMNS = 2

# corespond à la dernière ligne du fichier ne comprenant que le nombre de tours restants
MVMT_NBR = IDX_CORRECTOR = 1  # représente l'entier 1 qui est une ligne de fichier ne contenant que max_moves

# Ajout d'une variable espacement pour espacer la carte du coté gauche de la console
espacement = "   "

# et un index_corrector pour les boucles for et le systeme de coordonnées étant donné que la coord(0,0) corespond à "+"
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']

fond_blanc = "\u001b[47m"
# rouge 0       vert 1         jaune 2      bleu 3         magenta 4    cyan 5
couleur = ["\u001b[41m", "\u001b[42m", "\u001b[43m", "\u001b[44m", "\u001b[45m", "\u001b[46m"]
post_string_color = "\u001b[0m"

# source titre :  https://patorjk.com/software/taag/#p=display&h=0&v=0&f=Fire%20Font-k&t=ULBLOQUE
# source crédits : https://fancy-generator.com/fr
# Le titre n'est pas adaptable à la taille de la console il faudrait utiliser la librairies OS io resize par rapport à
# console
titre = """
                       ██▓▒­░ * 𝚖𝚊𝚍𝚎 𝚋𝚢 𝙼𝚊𝚡𝚜𝚘𝚞𝚕𝚜 * ░­▒▓██
 

      ___._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._._.___
    /./~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\.\ 
    ||                 (             (         )                                ||
    ||                 )\ )     (    )\ )   ( /(      (                         ||
    ||            (   (()/(   ( )\  (()/(   )\())   ( )\       (    (           ||
    ||            )\   /(_))  )((_)  /(_)) ((_)\    )((_)      )\   )\          ||
    ||         _ ((_) (_))   ((_)_  (_))     ((_)  ((_)_    _ ((_) ((_)         ||
    ||        | | | | | |     | _ ) | |     / _ \   / _ \  | | | | | __|        ||
    ||        | |_| | | |__   | _ \ | |__  | (_) | | (_) | | |_| | | _|         ||
    ||         \___/  |____|  |___/ |____|  \___/   \__\_\  \___/  |___|        ||
    \.\________________________________________________________________________/./
    
            Règles :  Sortir la voiture blanche par la sortie "-->"
                      Press "ESCAPE" to quit at any moment
            
            Comment ? 1 : Séléctionnez une voiture par sa lettre correspondante
                      2 : Déplacer la voiture avec :  UP  DOWN  RIGHT  LEFT
                      3 : Reseléctionnez une voiture
                          
                      
                 << Press any button to play the game >>
    
"""


"""
parse_game
La fonction parse_game analyse un fichier de jeu et retourne un dictionnaire game
représentant l’état initial du jeu de puzzle de voitures. 
Le chemin du fichier sera lu depuis la ligne de commande.

paramètres : — game_file_path : Chemin vers le fichier texte contenant la description du jeu.

Return : - > dict : dictionnaire game
"""


def parse_game(game_file_path: str) -> dict:
    game = {}
    # impossibilité de mettre try: except pour identifier si le fichier existe pas
    # Si la structure est utilisée les tests test_ulbloque.py me font échouer le test parse_game

    # try: !!
    with open(game_file_path, "r") as game_data:
        game_map = []
        for lines in game_data:
            game_map.append(lines.strip())
        # si malgré la 1ere vérif des arguments le chemin d'accès n'est pas bon empeche le crash
    # except FileNotFoundError: !!
    # print("File not found") !!
    # exit(0) !!

        # je suppose qu'il n'y a pas de changement dans l'ordre de données des fichiers donnés
        idx_first_column = 0  # évite un nombre magique dans la manip de la liste
        width = len(game_map[idx_first_column]) - NBR_SIDE_COLUMNS  # longueur bordure inférieure et supérieure
        height = len(game_map) - NBR_SIDE_LINES - MVMT_NBR
        game.update({"width": width, "height": height, "max_moves": int(game_map[-1])})

        cars = []
        found_cars = []
        for line in range(height + IDX_CORRECTOR):
            for char in range(width + IDX_CORRECTOR):
                # D'abord la boucle lenght car elle corespond à la longueur de la liste et la width à la longueur d'un
                # élément de celle-ci (qui est lui-même une liste
                car_letter = game_map[line][char]
                car_size = 0
                if car_letter in alphabet:
                    if car_letter not in found_cars:
                        car = [(char - IDX_CORRECTOR, line - IDX_CORRECTOR),
                               "orientation",
                               car_size,
                               game_map[line][char]]
                        # line = x et char = y
                        found_cars.append(car_letter)
                        idx_orientation = 1
                        idx_car_size = 2

                        # Sachant que la première partie de voiture sera toujours le morceau le plus en haut à gauche il
                        # suffit de vérifier pour le cas horizontal et vertical positif

                        if line + 1 < len(game_map) and game_map[line + 1][char] == car_letter:
                            car[idx_car_size] += 1
                            orientation = 'v'
                            car[idx_orientation] = orientation
                            new_line = line + 1
                            while new_line < len(game_map) and game_map[new_line][char] == car_letter:
                                car[idx_car_size] += 1
                                new_line += 1
                        elif char + 1 < len(game_map[line]) and game_map[line][char + 1] == car_letter:
                            car[idx_car_size] += 1
                            orientation = 'h'
                            car[idx_orientation] = orientation
                            new_char = char + 1
                            while new_char < len(game_map[line]) and game_map[line][new_char] == car_letter:
                                car[idx_car_size] += 1
                                new_char += 1

                        cars.append(car)

        # https://docs.python.org/3/howto/sorting.html
        # documentation python avec la recherche "python techniques de sort"
        # on fait une assignation qui recuillera la liste triée.
        # param de sorted(): list : list et key = lambda x : caractère ou entier à trier

        cars = sorted(cars, key=lambda x: x[3])
        for idx in range(len(cars)):
            del cars[idx][3]
        game["cars"] = cars
        return game


"""
get_game_st
 La fonction get_game_str renvoie le texte correspondant à l’affichage du plateau de
 jeu en utilisant les informations contenues dans le dictionnaire game. Elle
 montre les positions actuelles des voitures sur le plateau et le nombre de mouvements
 effectués.

 Paramètres
 — game : Dictionnaire contenant l’état actuel du jeu de puzzle de voitures (voir
 1.3.4).
 — current_move_number : Nombre actuel de mouvements effectués.
 Return :
 str : Texte correspondant à l’affichage du plateau de jeu
"""


def get_game_str(game: dict, current_move_number: int) -> str:
    # initialise une carte vide ( la sortie sera placée lors du placement de a
    inner_map = [["+"] + ["-"] * game["width"] + ["+"] + ["\n"]]
    for i in range(game["height"]):
        inner_map.append(["|"] + ['.'] * game["width"] + ["|"] + ["\n"])
    inner_map.append(["+"] + ["-"] * game["width"] + ["+\n"])
    cars = game["cars"]

    # placement de la voiture blanche et de la sortie en face
    coord_car = cars[0][0][0] + IDX_CORRECTOR, cars[0][0][1] + IDX_CORRECTOR
    code_blanc = fond_blanc + alphabet[0] + post_string_color
    inner_map[coord_car[1]][coord_car[0]] = code_blanc  # LES INDICE LE PREMIER == Y le 2EME == X
    inner_map = place_car(inner_map, coord_car, code_blanc, cars[0][2], cars[0][1])
    inner_map[coord_car[1]][-2] = "-->"
    count = 0
    for car in range(1, len(cars)):
        coord_car_n = cars[car][0][0] + IDX_CORRECTOR, cars[car][0][1] + IDX_CORRECTOR
        # opération pour permettre de redistribuer les couleurs si cars > 8
        code_color = couleur[count % len(couleur)] + alphabet[car] + post_string_color
        car_size = cars[car][2]
        car_orientation = cars[car][1]
        inner_map = place_car(inner_map, coord_car_n, code_color, car_size, car_orientation)
        count += 1
    # Création de la partie avec les mouvements restants
    outer_matrix = place_remaining_moves(str(current_move_number), str(game["max_moves"]))
    # transformation en string de la carte

    string_of_map = ''

    string_of_map = convert_to_str(inner_map, string_of_map, nbr_deplacment=6)

    string_of_map = convert_to_str(outer_matrix, string_of_map, nbr_deplacment=3)
    # La carte débutera au desus du premier caractère de MAX_MOVES
    return string_of_map


def move_car(game: dict, car_index: int, direction: str) -> bool:
    cars = game["cars"]
    car = cars[car_index]

    # on calcule toutes les coordonnées de la voiture déplacée
    moved_car = []
    for i in range(car[2]):
        if car[1] == "h":
            moved_car.append((car[0][0] + i, car[0][1]))
        else:
            moved_car.append((car[0][0], car[0][1] + i))

    cars_coord = recolt_coord(cars, car_index)

    # On va comparer la nouvelle position à toute celles de autres voitures
    return compare_cars(game, moved_car, car[1], car[2], direction, cars_coord, car_index)


def is_win(game: dict) -> bool:
    # tjrs horizon. taille map       taille voiture A
    exit_location = game["width"] - game["cars"][0][2]
    # je compare juste les x le y ne changeant jamais
    if game["cars"][0][0][0] is exit_location:
        return True
    else:
        return False


def play_game(game: dict) -> int:
    remaining_moves = game["max_moves"]
    if getkey() == "ESCAPE":
        return 2

    else:
        while not is_win(game):
            print(get_game_str(game, remaining_moves))
            print("Choisissez la voiture à déplacer")
            choose = getkey().upper()

            if remaining_moves == 0:
                return 1

            else:
                # Lire la touche pressée
                if choose == 'ESCAPE':
                    return 2

                elif choose.upper() in alphabet and alphabet.index(choose) < len(game["cars"]):
                    print(f"Vous avez séléctionné la voiture :  {choose}")
                    move = getkey()
                    if move_car(game, alphabet.index(choose), move):
                        print("le mouvement est effectué")
                        remaining_moves -= 1
                    else:
                        print("Le déplacement n'est pas valide")
        return 0


"""
convert_to_str
Cette fonction met dans un string les données présentes dans la matrice. Ce qui permet de print() le string
Fait pour que je puisse créer plusieurs "modules" venant autour de la carte

paramètres : - matrix : matrice des données
             - string : string qui contiendras les données de la matrice
             - nbr_deplacement : entier qui me permettra d'espacer le string de la bordure gauche de la console

return : string ainsi formé
"""


def convert_to_str(matrix: list, string: str, nbr_deplacment: int) -> str:
    for line in matrix:
        string += espacement * nbr_deplacment
        for character in line:
            string += character
    return string


"""
Place_car
Cette fonction va de pair avec get_game_str. 
Elle s'ocupe de placer les voitures à partir de la coordonnée de game["cars"]

paramètres : - game_map: la matrice de la carte du jeu (c'est une matrice pour une question de manip)
             - first_coord : le tuple représentant les coordonnées de la voiture dans l'objet "game"
             - color : code ascii pour colorer la voiture
             - car_size : taille de la voiture
             - Orientation: "h" ou "v" pour correctement placer les autres partie de la voiture
             
return : -> la liste game_map contenant la matrice du jeu 
BUT : factoriser le code (Ne place qu'une voiture)
"""


def place_car(game_map: list, first_coord: tuple, color: str, car_size: int, orientation: str) -> list:
    game_map[first_coord[1]][first_coord[0]] = color
    if orientation == "h":

        for i in range(1, car_size):
            nv_coord = first_coord[0] + i, first_coord[1]
            game_map[nv_coord[1]][nv_coord[0]] = color

    else:
        for i in range(1, car_size):
            nv_coord = first_coord[0], first_coord[1] + i
            game_map[nv_coord[1]][nv_coord[0]] = color

    return game_map


"""
# Update1: J'ai décidé de créer une fonction à part pour placer les if statements à la chaine 6 if consécutifs. Amélio ?
compare_cars
Compare la liste des coordonnées de la voiture séléctionnée avec les autres coordonnées des voitures sur la carte.
paramètres : - game: dictionnaire représentant l'avancement du jeu
             - moved_car_coord : coordonnées de la voiture en mouvement
             - car_orientation : orientation de la voiture déplacée
             - car_size : taille de la voiture déplacée
             - direction : Sans dans lequel est déplacée la voiture (ex: "DOWN")
             - other_cars : liste qui contient toutes les coordonnées des voitures exeptée celle déplacée
             - car_index : index de la voiture (0 = A, 1 = B, ...)
             
return : -> booléen qui indique si le mouvement est valide ou non
BUT: Séparer les différentes parties de la fonction move_car pour plus de lisibilité
"""


def compare_cars(game: dict, moved_car_coord: list, car_orientation: str,
                 car_size: int, direction: str, other_cars: list, car_index: int) -> bool:
    new_coord = []
    if car_orientation == "h":
        if direction == "RIGHT":
            for coord in range(len(moved_car_coord)):
                new_coord.append((moved_car_coord[coord][0] + 1, moved_car_coord[coord][1]))
            for element in new_coord:
                if not (0 <= new_coord[0][0] < game["width"] - car_size + 1 and element not in other_cars):
                    return False

            game["cars"][car_index][0] = new_coord[0]
            return True

        elif direction == "LEFT":
            for coord in range(len(moved_car_coord)):
                new_coord.append((moved_car_coord[coord][0] - 1, moved_car_coord[coord][1]))
            for element in new_coord:
                if not (0 <= new_coord[0][0] < game["width"] - car_size + 1 and element not in other_cars):
                    return False

            game["cars"][car_index][0] = new_coord[0]
            return True

        else:
            return False
    else:
        if direction == "UP":
            for coord in range(len(moved_car_coord)):
                new_coord.append((moved_car_coord[coord][0], moved_car_coord[coord][1] - 1))

            for element in new_coord:
                if not (0 <= new_coord[0][1] < game["height"] - car_size + 1 and element not in other_cars):
                    return False

            game["cars"][car_index][0] = new_coord[0]
            return True

        elif direction == "DOWN":
            for coord in range(len(moved_car_coord)):
                new_coord.append((moved_car_coord[coord][0], moved_car_coord[coord][1] + 1))
            for element in new_coord:
                if not (0 <= new_coord[0][1] < game["height"] - car_size + 1 and element not in other_cars):
                    return False

            game["cars"][car_index][0] = new_coord[0]
            return True
        else:
            return False


"""
place_remaining_moves
Cette fonction est en lien avec get_game_str. Je préfère rajouter cette partie à la matrice pour avoir un affichage
qui reste constant. Cette fonction indique aussi le nombre de mvmt restant et change de couleur en fonction du nbrs 
de mouvement restant. 

paramètres : - game_matrix : matrice contenant les caractères et voitures
             - remaining_moves : mouvements restants
             - max_moves : présent dans l'objet "game" --> nbr de mvmt maximum
             
return : /X/ rajoute à la fin de game_matrix l"espace pour le compteur
BUT: Plus de clareté
"""


def place_remaining_moves(remaining_moves: str, max_moves: str):

    # usage de chatGPT pour trouver les codes ascii, l'affichage est indépendant de la taille de la grille
    co_matrix = [["<|"] + ["======="] + ["MAX MOVES"] + ["======|>\n"],
                 [" |"] + ["__________"] + [max_moves] + ["__________|\n"],
                 [" |~~~~~~remaining~~~~~~~|\n"],
                 [" \________\ "] + ["\033[32m" + str(remaining_moves) + "\033[0m"] + [" /________/\n"]]

    # changement de la couleur du numéro en fonction du nombres de mouvements restants
    if 5 < int(remaining_moves) <= int(max_moves) // 2:
        co_matrix[-1] = [" \________\ "] + ["\033[33m" + str(remaining_moves) + "\033[0m"] + [" /________/\n"]
    elif 1 <= int(remaining_moves) <= 5:
        co_matrix[-1] = [" \________\ "] + ["\033[31m" + str(remaining_moves) + "\033[0m"] + [" /________/\n"]
    elif int(remaining_moves) == 0:
        co_matrix[-1] = ([" \________\ "] + ["\033[41m\033[30m" + ' ' + str(remaining_moves) + ' ' + "\033[0m"] +
                         [" /________/\n"])

    return co_matrix


"""
recolt_coord
Cette fonction récolte les données d'une unique voiture et calcule toutes ses coordonnées
Elle sera appelées dans move_car puis utilisée dans compare_car

paramètres : - cars : liste présente dans game["cars] contenant les voitures
             - car_index : index de la voiture (0 = A, 1 = B, ...)
             
return : liste qui contient toutes les coordonnées calculées de la voiture d'index car_index
BUT: Séparer les différentes parties de la fonction move_car pour plus de lisibilité
"""


def recolt_coord(cars: list, car_index: int) -> list:
    occupied_coords = []

    # Récupérez les coordonnées de toutes les autres voitures
    for i, car in enumerate(cars):
        if i != car_index:  # Ignorez la voiture en cours de mouvement
            car_coords = []
            for j in range(car[2]):  # car[2] est la taille de la voiture
                if car[1] == "h":  # orientation horizontale
                    car_coords.append((car[0][0] + j, car[0][1]))  # (x, y)µ
                else:  # orientation verticale
                    car_coords.append((car[0][0], car[0][1] + j))  # (x, y)
            occupied_coords.extend(car_coords)  # Ajoutez les coordonnées occupées
    return occupied_coords


if __name__ == '__main__':
    commande = argv
    if len(commande) > 2 or len(commande) == 1:
        print(f"La commande n'est pas correcte. Le nombre d'argument(s) est:  ({len(commande)}).\n")
        print("La commande demandée est: python3 ulbloque.py file_of_map.txt")
        exit(0)
    else:
        file_of_map = commande[1]
        # initialise la carte
        play_map = parse_game(file_of_map)
        print(titre)
        # lance le jeu
        res = play_game(play_map)
        if res == 0:
            print("\033[42m\033[37mVous avez gagné !\033[0m")
        elif res == 1:
            print("\033[31mVous avez perdu !\033[0m")
        else:
            print("Vous avez quitté le jeu")

