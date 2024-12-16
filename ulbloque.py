"""
------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
But :
Ulbloque simule un jeu de puzzle ou la voiture blanche doit sortir d'un parking parsé d'un fichier texte.
Cela mobilise les savoir de base de python sur les boucles, if statements, manipulations sur les dictionnaires, listes,
matrices, etc.
------------------------------------------------------------------------------------------------------------------------
source art : symbole et unicode → https://symbl.cc/fr/unicode-table/
source font generator → https://patorjk.com/software/taag/
------------------------------------------------------------------------------------------------------------------------
"""


from sys import argv
from getkey import getkey

# number borders (bottom, upper and sides)
NBR_SIDE_LINES = NBR_SIDE_COLUMNS = 2

# last line of file == max_moves help later to only get other information.
# IDX_CORRECTOR is to rectify the position in the matrix. In fact, the coordinates of A (0,2) are in the code (1, 3)
# That's because of the first line in the matrix which is "+------------+"
MOVE_NUMBER = IDX_CORRECTOR = 1

# used to assign a letter to a car and avoid having more than 26
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']


def is_win(game: dict) -> bool:

    exit_location = game["width"] - game["cars"][0][2]
    # y will never change for the white car because its horizontal
    if game["cars"][0][0][0] is exit_location:
        return True
    else:
        return False


"""
-----------------------------------------------------------------------------------------------------------------------

Needed functions to pass the tests
They work with the additional functions

-----------------------------------------------------------------------------------------------------------------------
"""


def parse_game(game_file_path: str) -> dict:
    game = {}
    # catch various possible errors and exit the code with value 1 to indicate the error
    game_map = read_game_file(game_file_path)
    # I suppose no change in the files given
    idx_first_column = 0  # avoid magical number
    width = len(game_map[idx_first_column]) - NBR_SIDE_COLUMNS
    # height equals length of file minus number of upper and bottom border minus the line of max_moves
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

                    # check the surroundings of the new-found letter to expand the vertical car
                    if line + 1 < len(game_map) and game_map[line + 1][char] == car_letter:
                        car[car_size_idx] += 1
                        car[orientation_idx] = "v"
                        new_line = line + 1
                        while new_line < len(game_map) and game_map[new_line][char] == car_letter:
                            car[car_size_idx] += 1
                            new_line += 1

                    # check the surroundings of the new-found letter to expand the horizontal car
                    elif char + 1 < len(game_map[line]) and game_map[line][char + 1] == car_letter:
                        car[car_size_idx] += 1
                        car[orientation_idx] = "h"
                        new_char = char + 1
                        while new_char < len(game_map[line]) and game_map[line][new_char] == car_letter:
                            car[car_size_idx] += 1
                            new_char += 1

                    cars.append(car)

    # Assignment of the values into a sorted list
    # param de sorted(): list : list and key = lambda x : idx of the character or integer to sort - Aide GPT
    cars = sorted(cars, key=lambda x: x[3])
    for idx in range(len(cars)):
        del cars[idx][3]
    game["cars"] = cars
    return game


def get_game_str(game: dict, current_move_number: int) -> str:
    white_bkg = "\u001b[47m "
    # red 0, green 1, yellow 2, blue 3, magenta 4, cyan 5
    colors = ["\u001b[41m ", "\u001b[42m ", "\u001b[43m ", "\u001b[44m ", "\u001b[45m ", "\u001b[46m "]
    post_string_color = " \u001b[0m"
    # Initialize the inner map of the game (inclue only de cars and void characters and not the borders)
    inner_map = [["\u250F"] + ["---"] * game["width"] + ["\u2513"] + ["\n"]]

    # Initialize borders of the map
    for i in range(game["height"]):
        inner_map.append(["\u2507"] + [' \U0001F784 '] * game["width"] + ["\u2507"] + ["\n"])
    inner_map.append(["\u2517"] + ["---"] * game["width"] + ["\u251B\n"])
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
    return check_car_overlap(game, coord_moved_car, direction, cars_coord, car_index)


def play_game(game: dict) -> int:
    move_counter = 0
    selected_car_index = None

    while not is_win(game):

        if move_counter == game["max_moves"]:
            return 1

        move = getkey().upper()
        # latence au niveau de getkey une fois ESCAPE pressée le programme se terminera dans tous les cas
        if move == 'ESCAPE':
            return 2
        # clear la console
        print("\033[H\033[2J", end="")
        if move in alphabet and alphabet.index(move) < len(game["cars"]):
            selected_car_index = alphabet.index(move)
            print(f"--- Vous avez sélectionné la voiture {move} ---\n")
            print(get_game_str(game, move_counter))

        elif selected_car_index is not None and move_car(game, selected_car_index, move):
            # Déplacer la voiture sélectionnée
            print("\U0001F338 --- Le mouvement est effectué --- \U0001F338\n")
            move_counter += 1
            print(get_game_str(game, move_counter))

        else:
            print("~~~ Le déplacement n'est pas valide ~~~\n")
            print(get_game_str(game, move_counter))

    return 0


"""
-----------------------------------------------------------------------------------------------------------------------

Additional functions

-----------------------------------------------------------------------------------------------------------------------
"""


def read_game_file(game_file_path: str) -> list[str]:
    try:
        with open(game_file_path, "r") as game_data:
            game_map = []
            for lines in game_data:
                game_map.append(lines.strip())

    except FileNotFoundError:
        print("File not found")
        exit(1)
    except IsADirectoryError:
        print(f"The file can not be run: {game_file_path} --> is a Directory")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)

    return game_map


# matrix is the structure used to manipulate the map and empty string is used for the conversion
def convert_to_str(matrix: list, string: str) -> str:
    for line in matrix:
        for character in line:
            string += character
    return string


# use the first coord of the car to set the remaining parts of it
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


def check_car_overlap(game: dict, moved_car_coord: list, direction: str, other_cars: list, car_index: int) -> bool:
    car_authorised_move = {
        "h": {"RIGHT": (1, 0), "LEFT": (-1, 0)},
        "v": {"UP": (0, -1), "DOWN": (0, 1)},
    }

    car_orientation = game["cars"][car_index][1]

    if direction not in car_authorised_move[car_orientation]:
        return False

    move_x, move_y = car_authorised_move[car_orientation][direction]
    # list of tuples corresponding each coordinate of the car
    updated_coord = []

    # we check if the coordinates + 1 instance do not overlap another car
    for curent_x, curent_y in moved_car_coord:
        future_x, future_y = curent_x + move_x, curent_y + move_y
        # set the limits of the matrix (map)
        if not (0 <= future_x < game["width"] and 0 <= future_y < game["height"]):
            return False

        if (future_x, future_y) in other_cars:
            return False

        updated_coord.append((future_x, future_y))
    # we are only allowed to modify the first tuple in the dictionary game
    game["cars"][car_index][0] = updated_coord[0]
    return True


def display_remaining_moves(current_moves: str, max_moves: str):
    # display is hardcoded because we cannot use OS module to calculate the length and width of the console
    move_display = [["<|"] + ["======="] + ["MAX MOVES"] + ["======|>\n"], [" |"] + ["__________"] + [max_moves] +
                    ["__________|\n"], [" |~~~~~~remaining~~~~~~~|\n"], [" \________\ "] +
                    ["\033[32m" + current_moves + "\033[0m"] + [" /________/\n"]]

    # display the remaining moves in different color depending on how close the moves are to 0
    if int(max_moves) // 2 <= int(current_moves) < int(max_moves):
        move_display[-1] = [" \________\ "] + ["\033[33m" + current_moves + "\033[0m"] + [" /________/\n"]

    elif int(current_moves) == int(max_moves):
        move_display[-1] = ([" \________\ "] + ["\033[41m\033[30m" + current_moves + "\033[0m"] +
                            [" /________/\n"])

    return move_display


def harvest_coordinates(cars: list, car_index: int) -> list:
    occupied_coordinates = []

    for idx, car in enumerate(cars):
        if idx != car_index:  # Ignore the moving car
            car_coordinates = []
            for j in range(car[2]):  # car[2]  == size of the car
                if car[1] == "h":
                    car_coordinates.append((car[0][0] + j, car[0][1]))
                else:
                    car_coordinates.append((car[0][0], car[0][1] + j))
            occupied_coordinates.extend(car_coordinates)
    return occupied_coordinates


if __name__ == '__main__':
    # recherche des caractères sur https://symbl.cc/fr/unicode-table/#runic
    # usage de l'IA pour trouver les caractères d'échappement correspondent
    # le reste est fait main

    # Chaine de caractère d'échappement trouvée sur :
    # https://stackoverflow.com/questions/517970/how-can-i-clear-the-interpreter-console/50560686#50560686
    # et indiquée par le discord pour rajouter de la clarté
    clear = "\033[H\033[2J"
    title = """
                            \u001b[36m██▓▒­░ * 𝚖𝚊𝚍𝚎 𝚋𝚢 𝙼𝚊𝚡𝚜𝚘𝚞𝚕𝚜 * ░­▒▓██


        
        ╭━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮ 
        |   ▓▓▓▒░░░ ᚠ ᚡ ᚢ ᚣ ᚤ ᚥ  ᚧ ᚨ ᚩ ᚪᚬ ᚶ ᚷ ᚸ ᚹ ᚺᚻ ᚼ  ᛀ ᛁ ᛂ ᛃ ᛆ ᛈ ᛉ  ᛊ ᛋ ░░░▒▓▓▓   |
        |  ▓▓▓▒░░░ _   _   _      _ _    _        _      _ _    _   _   ___  ░░▒▓▓▓  |
        | ▓▓▓▒░░░ | | | | | |    | _ )  | |     / _ \   / _ \  | | | | | __|  ░░▒▓▓▓ |
        | ▓▓▓▒░░░ | |_| | | |__  | _ \  | |__  | (_) | | (_) | | |_| | | _|   ░░▒▓▓▓ |
        |  ▓▓▓▒░░  \___/  |____| |___/  |____|  \___/   \__\_\  \___/  |___| ░░▒▓▓▓  |
        |   ▓▓▓▒░░░ ᚲ ᚳ ᚴ ᚵ ᚶ ᚷ ᚸ ᚹ ᚺ ᚻ ᚼ ᚽ ᛁ ᛂ ᛃᛍᛏ ᛐ ᛑ ᛒ ᛓ ᛔ ᛕ ᛖ   ᛫ ᛯᛲ ᛳ ░░░▒▓▓▓   |
        ╰━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╯

                Goal :  Help the white escape the parking by the exit : "-->"
                
                          Press "ESCAPE" to quit at any moment

                How ?     \U0001F7A0 : Select a car with their letter
                                          
                                                  
                          \U0001F7A0 : Move the car : UP DOWN LEFT RIGHT
                                            

                         << Press any button to play the game >>\u001b[0m  

    """
    win_message = """
\u001b[32m ██╗   ██╗ ██████╗ ██╗   ██╗     ██╗    ██╗ ██████╗ ███╗   ██╗  
 ╚██╗ ██╔╝██╔═══██╗██║   ██║     ██║    ██║██╔═══██╗████╗  ██║  
  ╚████╔╝ ██║   ██║██║   ██║     ██║ █╗ ██║██║   ██║██╔██╗ ██║  
   ╚██╔╝  ██║   ██║██║   ██║     ██║███╗██║██║   ██║██║╚██╗██║  
    ██║   ╚██████╔╝╚██████╔╝     ╚███╔███╔╝╚██████╔╝██║ ╚████║  
    ╚═╝    ╚═════╝  ╚═════╝       ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═══╝\u001b[0m                                                                                                
    """
    game_over = """
  \u001b[31m ██████╗  █████╗ ███╗   ███╗███████╗      ██████╗ ██╗   ██╗███████╗██████╗
  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝     ██╔═══██╗██║   ██║██╔════╝██╔══██╗
  ██║  ███╗███████║██╔████╔██║█████╗       ██║   ██║██║   ██║█████╗  ██████╔╝
  ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝       ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗     ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝      ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝\u001b[0m
   """
    quit_message = """
   \u001b[33m██████╗  █████╗ ███╗   ███╗███████╗    ██╗     ███████╗███████╗████████╗
  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██║     ██╔════╝██╔════╝╚══██╔══╝
  ██║  ███╗███████║██╔████╔██║█████╗      ██║     █████╗  █████╗     ██║   
  ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║     ██╔══╝  ██╔══╝     ██║   
  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ███████╗███████╗██║        ██║   
   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚══════╝╚══════╝╚═╝        ╚═╝ \u001b[0m  
    """
    # Assignation to a variable for more readability
    commande = argv
    if len(commande) > 2 or len(commande) == 1:
        print(f"Incorrect command : {commande}")
        print("Correct command : python3 ulbloque.py file_of_map.txt")
        # code de sortie 1 pour indiquer une erreur
        exit(1)
    else:
        file_of_map = commande[1]
        play_map = parse_game(file_of_map)
        print(title)
        if getkey() != "ESCAPE":
            print(clear, end="")
            print(get_game_str(play_map, 0))
            res = play_game(play_map)
            if res == 0:
                print(win_message)
            elif res == 1:
                print(game_over)
            else:
                print(quit_message)
        else:
            print(quit_message)
