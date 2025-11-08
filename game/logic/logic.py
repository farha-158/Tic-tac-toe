# logic/logic.py
from .logicException import InvalidMoveError, TooManyPlayersError


class TicTacToeGame:
    def __init__(self):
        self.players = []  # [{username, sid, symbol}]
        self.board = [""] * 9
        self.turn = None

    def add_player(self, username, sid):
        if len(self.players) >= 2:
            raise TooManyPlayersError("Room is full. Please wait for the next round.")
        symbol = "X" if len(self.players) == 0 else "O"
        self.players.append({"username": username, "sid": sid, "symbol": symbol})
        return symbol

    def remove_player(self, sid):
        self.players = [p for p in self.players if p["sid"] != sid]
        self.reset_board()

    def make_move(self, sid, index, symbol):
        if index is None or not (0 <= index < 9):
            raise InvalidMoveError("Invalid move position.")
        if sid != self.turn:
            raise InvalidMoveError("It's not your turn!")
        if self.board[index]:
            raise InvalidMoveError("Cell already taken.")

        self.board[index] = symbol

        winner = self.check_winner()
        if winner:
            winner_name = next((p["username"] for p in self.players if p["symbol"] == winner), None)
            self.reset_board()
            return {"winner": winner_name}

        if "" not in self.board:
            self.reset_board()
            return {"winner": "Draw"}

        # تبديل الدور
        self.turn = [p["sid"] for p in self.players if p["sid"] != sid][0]
        next_turn_name = next(p["username"] for p in self.players if p["sid"] == self.turn)
        return {"turn": next_turn_name}

    def check_winner(self):
        combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for a, b, c in combos:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def reset_board(self):
        self.board = [""] * 9
        self.turn = None
