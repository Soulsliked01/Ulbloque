"""
Nom: Perera Gonzalez
Prénom: Maxence
Matricule: 590023

"""

from sys import argv
from getkey import getkey

# number borders (bottom, upper and sides
NBR_SIDE_LINES = NBR_SIDE_COLUMNS = 2

# last line of file == max_moves help later to only get other info. Sto
MOVE_NUMBER = IDX_CORRECTOR = 1

# used to assign a letter to a car and avoid having more than 26
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


def parse_game(game_file_path: str) -> dict:
    game = {}

    try:
        with open(game_file_path, "r") as game_data:
            game_map = []
            for lines in game_data:
                game_map.append(lines.strip())

    except FileNotFoundError:
        print("File not found")
        exit(1)
    except PermissionError:
        print("Permission denied")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")

    # I suppose no change in the files given
    idx_first_column = 0  # avoid magical number
    width = len(game_map[idx_first_column]) - NBR_SIDE_COLUMNS
    # height equals lenght of file minus number of upper and bottom border minus the line of max_moves
    height = len(game_map) - NBR_SIDE_LINES - MOVE_NUMBER
    game.update({"width": width, "height": height, "max_moves": int(game_map[-1])})

    cars = []
    found_cars = []
    # nested loop to find and mark the cars (IDX_CORRECTOR to access idx in list)
    for line in range(height + IDX_CORRECTOR):
        for char in range(width + IDX_CORRECTOR):
            car_letter = game_map[line][char]
            car_size = 0
            if car_letter in alphabet:
                if car_letter not in found_cars:
                    car = [(char - IDX_CORRECTOR, line - IDX_CORRECTOR), "orientation",
                           car_size, game_map[line][char]]
                    found_cars.append(car_letter)
                    orientation_idx = 1
                    car_size_idx = 2

                    # check the surondings of the new-found letter to expand the vertical car
                    if line + 1 < len(game_map) and game_map[line + 1][char] == car_letter:
                        car[car_size_idx] += 1
                        car[orientation_idx] = "v"
                        new_line = line + 1
                        while new_line < len(game_map) and game_map[new_line][char] == car_letter:
                            car[car_size_idx] += 1
                            new_line += 1

                    # check the surondings of the new-found letter to expand the horizontal car
                    elif char + 1 < len(game_map[line]) and game_map[line][char + 1] == car_letter:
                        car[car_size_idx] += 1
                        car[orientation_idx] = "h"
                        new_char = char + 1
                        while new_char < len(game_map[line]) and game_map[line][new_char] == car_letter:
                            car[car_size_idx] += 1
                            new_char += 1

                    cars.append(car)

    # Assignement of the values into a sorted list
    # param de sorted(): list : list and key = lambda x : idx of the carachter or integer to sort - Aide GPT

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
    white_bkg = "\u001b[47m"
    # red 0, green , yellow 2, blue 3, magenta 4, cyan 5
    colors = ["\u001b[41m", "\u001b[42m", "\u001b[43m", "\u001b[44m", "\u001b[45m", "\u001b[46m"]
    post_string_color = "\u001b[0m"
    # Initialize the inner map of the game (inclue only de cars and void characthers
    inner_map = [["+"] + ["-"] * game["width"] + ["+"] + ["\n"]]

    # Initialize borders of the map
    for i in range(game["height"]):
        inner_map.append(["|"] + ['.'] * game["width"] + ["|"] + ["\n"])
    inner_map.append(["+"] + ["-"] * game["width"] + ["+\n"])
    cars = game["cars"]

    # the exit is at the end of the list in front of the white car
    coord_car = cars[0][0][0] + IDX_CORRECTOR, cars[0][0][1] + IDX_CORRECTOR
    code_blanc = white_bkg + alphabet[0] + post_string_color
    inner_map[coord_car[1]][coord_car[0]] = code_blanc  # x and y are switched in a matrix
    inner_map = place_car(inner_map, coord_car, code_blanc, cars[0][2], cars[0][1])
    inner_map[coord_car[1]][-2] = "-->"

    count = 0
    for car in range(1, len(cars)):
        position_car_n = cars[car][0][0] + IDX_CORRECTOR, cars[car][0][1] + IDX_CORRECTOR
        # the operation "%" guarantee that if there are more than 7 cars the colors will loop.(car 8 will be red again)
        code_color = colors[count % len(colors)] + alphabet[car] + post_string_color
        car_size = cars[car][2]
        car_orientation = cars[car][1]
        inner_map = place_car(inner_map, position_car_n, code_color, car_size, car_orientation)
        count += 1

    outer_matrix = display_remaining_moves(str(current_move_number), str(game["max_moves"]))

    string_of_map = ''
    string_of_map = convert_to_str(inner_map, string_of_map)
    string_of_map = convert_to_str(outer_matrix, string_of_map)
    return string_of_map


def move_car(game: dict, car_index: int, direction: str) -> bool:
    cars = game["cars"]
    car = cars[car_index]

    # We calculate all the coordinates of the car
    coord_moved_car = []
    for i in range(car[2]):
        if car[1] == "h":
            coord_moved_car.append((car[0][0] + i, car[0][1]))
        else:
            coord_moved_car.append((car[0][0], car[0][1] + i))

    cars_coord = harvest_coordinates(cars, car_index)

    # On va comparer la nouvelle position à toutes celles d'autres voitures
    return check_car_overlap(game, coord_moved_car, direction, cars_coord, car_index)


def is_win(game: dict) -> bool:

    exit_location = game["width"] - game["cars"][0][2]
    # y will never change for the white car
    if game["cars"][0][0][0] is exit_location:
        return True
    else:
        return False


def play_game(game: dict) -> int:
    remaining_moves = game["max_moves"]
    selected_car_index = None

    while not is_win(game):
        print(get_game_str(game, remaining_moves))
        if remaining_moves == 0:
            return 1
        move = getkey().upper()
        # latence au niveau de getkey une fois ESCAPE pressée le programme se terminera dans tous les cas
        if move == 'ESCAPE':
            return 2

        if move in alphabet and alphabet.index(move) < len(game["cars"]):
            # Sélectionner une voiture
            selected_car_index = alphabet.index(move)
            print(f"Vous avez séléctionné la voiture {move}")
        elif selected_car_index is not None and move_car(game, selected_car_index, move):
            # Déplacer la voiture sélectionnée
            print("Le mouvement est effectué.")
            remaining_moves -= 1
        else:
            print("Le déplacement n'est pas valide")

    return 0


# matrix is the structure used to manipulate the map and empty string is used for the conversion
def convert_to_str(matrix: list, string: str = "") -> str:
    for line in matrix:
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
# Update2: Si je créé un dict qui contient les mouvements et coord, et si utilisation le jeu fonctionne 
mais je ne passe pas les tests 
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


def check_car_overlap(game: dict, moved_car_coord: list, direction: str, other_cars: list, car_index: int) -> bool:
    car_authorised_move = {
        "h": {"RIGHT": (1, 0), "LEFT": (-1, 0)},
        "v": {"UP": (0, -1), "DOWN": (0, 1)},
    }

    car_orientation = game["cars"][car_index][1]

    if direction not in car_authorised_move[car_orientation]:
        return False

    move_x, move_y = car_authorised_move[car_orientation][direction]
    updated_coord = []

    for old_x, old_y in moved_car_coord:
        new_x, new_y = old_x + move_x, old_y + move_y

        if not (0 <= new_x < game["width"] and 0 <= new_y < game["height"]):
            return False

        if (new_x, new_y) in other_cars:
            return False

        updated_coord.append((new_x, new_y))

    game["cars"][car_index][0] = updated_coord[0]
    return True


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


def display_remaining_moves(remaining_moves: str, max_moves: str):

    move_display = [["<|"] + ["======="] + ["MAX MOVES"] + ["======|>\n"], [" |"] + ["__________"] + [max_moves] +
                    ["__________|\n"], [" |~~~~~~remaining~~~~~~~|\n"], [" \________\ "] +
                    ["\033[32m" + str(remaining_moves) + "\033[0m"] + [" /________/\n"]]

    # affichage des nombres de différentes couleurs en fonction des mvmts restants
    if 5 < int(remaining_moves) <= int(max_moves) // 2:
        move_display[-1] = [" \________\ "] + ["\033[33m" + remaining_moves + "\033[0m"] + [" /________/\n"]
    elif 1 <= int(remaining_moves) <= 5:
        move_display[-1] = [" \________\ "] + ["\033[31m" + remaining_moves + "\033[0m"] + [" /________/\n"]
    elif int(remaining_moves) == 0:
        move_display[-1] = ([" \________\ "] + ["\033[41m\033[30m" + ' ' + remaining_moves + ' ' + "\033[0m"] +
                            [" /________/\n"])

    return move_display


def harvest_coordinates(cars: list, car_index: int) -> list:
    occupied_coords = []

    # Récupérez les coordonnées de toutes les autres voitures
    for i, car in enumerate(cars):
        if i != car_index:  # Ignore the moving car
            car_coords = []
            for j in range(car[2]):  # car[2]  == size of the car
                if car[1] == "h":
                    car_coords.append((car[0][0] + j, car[0][1]))
                else:
                    car_coords.append((car[0][0], car[0][1] + j))
            occupied_coords.extend(car_coords)
    return occupied_coords


if __name__ == '__main__':
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
    commande = argv
    if len(commande) > 2 or len(commande) == 1:
        print(f"La commande n'est pas correcte. Le nombre d'argument(s) est:  ({len(commande)}).\n")
        print("La commande demandée est: python3 ulbloque.py file_of_map.txt")
        exit(0)
    else:
        file_of_map = commande[1]
        play_map = parse_game(file_of_map)
        print(titre)
        if getkey():
            res = play_game(play_map)
            if res == 0:
                print("\033[42m\033[37mVous avez gagné !\033[0m")
            elif res == 1:
                print("\033[31mVous avez perdu !\033[0m")
            else:
                print("Vous avez quitté le jeu")
