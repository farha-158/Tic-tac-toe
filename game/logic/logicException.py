# logic/logicExceptions.py
class GameError(Exception):
    pass

class InvalidMoveError(GameError):
    pass

class TooManyPlayersError(GameError):
    pass
