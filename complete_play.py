import requests
import json


def play_lap(game_server_url: str, netid: str, player_key: str):
    # starting a fresh session with blank cookies:
    session = requests.Session()
    session.headers = {"Connection": "close"}

    # query the available game_types to find the LAP id:
    game_search = session.get(url=game_server_url + "game-types",
                              json={"netid": netid,
                                    "player_key": player_key})
    try:
        result = game_search.json()['result']
    except Exception as e:
        print('unexpected response:')
        print(game_search.content)
        print('\nfollowed by exception:' + str(e))
        return

    # searching for a game of LAP
    game_id = False
    for g in result:
        if ('LAP' in g['fullname'].upper()) and g['num_players'] == 2:
            game_id = g['id']

    # Now request a single match of that game type:
    request_match = session.post(url=game_server_url + "game-type/{}/request-match".format(game_id),
                                 json={"netid": netid,
                                       "player_key": player_key})

    print(request_match.text)
    match_id = request_match.json()['result']['match_id']

    if game_id:
        print('Found matching game-type: ', game_id)
    else:
        print('Game not available now.')
        exit()

#TODO: insert here - game play between two players on server

def input_validator(game_state):
    if (len(game_state) != 6):
        print('Incorrect Size ', len(game_state), " GS ", game_state)
        return False

    for clue in game_state:
        if (len(clue) != 6):
            print('F')
            return False
        else:
            print('T')
            return True


def fetch_clues(i, j, game_state):
    return game_state[i][j] + game_state[i][j + 1] + game_state[j + 1][i] + game_state[i + 1][j + 1]


def check_winner(request, game_state):
    return request == game_state


player_turn = 1

game_state11 = ["zzzzzx", "zzzxxx", "zxxxyx", "yyyyyx", "yyywww", "wwwwww"]
game_state22 = ['wwwxxz', 'wwxxxz', 'wwxxyz', 'wwxxyz', 'yyyyyz', 'yyzzzz']

# zzzzzx zzzxxx zxxxyx yyyyyx yyywww wwwwww
# wwwxxz wwxxxz wwxxyz wwxxyz yyyyyz yyzzzz

while True:
    game_state_0 = input(
        "Enter the Clues for Player 1 , Format - aaaaaa bbbbbb cccccc dddddd eeeeeee ffffff \n \n").split(" ")
    game_state_1 = input(
        "Enter the Clues for Player 2 , Format - aaaaaa bbbbbb cccccc dddddd eeeeeee ffffff \n \n").split(" ")

    if input_validator(game_state_0) and input_validator(game_state_1):
        break
    else:
        print("Either one of the game states is incorrect, Please enter them again \n \n ")

while True:
    if player_turn == 1:

        player_request0 = input(
            "Player {} Please enter the Clue in the format (0,0) or take a guess by entering the string with spaces \n \n ".format(
                player_turn))
        player_turn = 2
        if (len(player_request0.split(" ")) > 1):
            if check_winner(player_request0.split(" "), game_state_1):
                print("Player One Wins the Game! \n \n ")
                break
            else:
                print("You've guessed it incorrectly! \n \n ")
        else:
            while True:
                if (int(player_request0[1]) >= 0 and int(player_request0[1]) < 5 and int(
                        player_request0[3]) >= 0 and int(player_request0[3]) < 5):
                    print("Here's your clue - ",
                          fetch_clues(int(player_request0[1]), int(player_request0[3]), game_state_0))
                    break
                else:
                    player_request0 = print("Please enter the Clue in the format (0,0) \n \n ")
    if player_turn == 2:
        player_request1 = input(
            "Player {} Please enter the Clue in the format (0,0) or take a guess by entering the string with spaces\n \n ".format(
                player_turn))
        player_turn = 1
        if (len(player_request1.split(" ")) > 1):
            if check_winner(player_request1.split(" "), game_state_0):
                print("Player two Wins the Game! \n \n ")
                break
            else:
                print("You've guessed it incorrectly! \n \n ")
        else:
            while True:
                if (int(player_request1[1]) >= 0 and int(player_request1[1]) < 6 and int(
                        player_request1[3]) >= 0 and int(player_request1[3]) < 6):
                    print("Here's your clue - ",
                          fetch_clues(int(player_request1[1]), int(player_request1[3]), game_state_1))
                    break
                else:
                    player_request1 = print("Please enter the Clue in the format (0,0) \n \n ")
