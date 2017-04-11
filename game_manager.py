import logging
import game
import random

# Class that holds necessary information about a player
# id       : global indentifier for the device the player is linked to
# avatar   : index of the avatar that is assigned for this player
# nickname : user friendly name for this player
class Player(object):
    def __init__(self, user_id, avatar, nickname):
        self.user_id = user_id
        self.avatar = avatar
        self.nickname = nickname


# Keeps track of what games are going on and manages game ids
class GameManager(object):
    def __init__(self):
        # Initialize free_ids
        self._free_ids = range(10000)
        self._used_ids = []

        self._games = {}
        # Initialize container for players


    def createGame(self, errors, game_data, host):
        # Get an id for this game
        id_index = self._pickRandomId(errors)
        if id_index == None:
            return None

        # Free id found, convert to string
        game_id = str(self._free_ids[id_index]).zfill(4)

        # Move the id from free to used
        self._used_ids.append(self._free_ids[id_index])
        del self._free_ids[id_index]

        # Actually create the game
        new_game = game.Game(game_id, game_data['location'], game_data['waypoints'], game_data['radius'])

        # Add the first player in the lobby
        new_game.addPlayer(errors, Player(host['user_id'], 0, host['nickname']))

        # If nothing happened, go ahead and add the game, else destroy
        if len(errors) == 0:
            self._games[game_id] = new_game
            return new_game
        else:
            # Free the used id and return none
            self._free_ids.append(self._used_ids[-1])
            del self._used_ids[-1]
            return None


    # Returns a game with the provided id, if one exists
    def getGame(self, errors, game_id):
        if game_id in self._games:
            return self._games[game_id]
        else:
            errors.append("Game does not exist, id:" + game_id)
            return None


    # Randomly selects and returns an available id
    def _pickRandomId(self, errors):
        if len(self._free_ids) > 0:
            return int(random.random() * len(self._free_ids))
        else:
            errors.append("No more free ids, all are in use")
            return None
