# events.py
from flask import request
from flask_socketio import emit
from .extensions import socketio
from .logic.logic import TicTacToeGame
from .logic.logicException import InvalidMoveError, TooManyPlayersError
from .logger import logger  

# 🧩 إنشاء اللعبة
game = TicTacToeGame()


@socketio.on("connect")
def handle_connect():
    logger.info("client_connect", player=request.sid, details="Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    try:
        game.remove_player(request.sid)
        logger.info("player_disconnect", player=request.sid, details="Player disconnected")

        if len(game.players) == 1:
            emit("game_update", {
                "board": game.board,
                "turn": None,
                "winner": game.players[0]['username'] 
            }, broadcast=True)

    except Exception as e:
        logger.error("disconnect_error", player=request.sid, details=str(e))


@socketio.on("user_join")
def handle_user_join(username):
    try:
        symbol = game.add_player(username, request.sid)
        logger.info("user_join", player=request.sid, details=f"{username} joined as {symbol}")

        if len(game.players) < 2:
            emit("waiting_for_user", to=request.sid)
        else:
            game.turn = game.players[0]["sid"]
            emit("ready_to_play", {"symbol": "X"}, to=game.players[0]["sid"])
            emit("ready_to_play", {"symbol": "O"}, to=game.players[1]["sid"])

            emit("game_update", {
                "board": game.board,
                "turn": game.players[0]["username"]
            }, broadcast=True)

    except TooManyPlayersError as e:
        emit("error_message", {"error": str(e)}, to=request.sid)
        logger.warning("too_many_players", player=request.sid, details=str(e))
    except Exception as e:
        emit("error_message", {"error": f"Unexpected error: {e}"}, to=request.sid)
        logger.error("unexpected_error_user_join", player=request.sid, details=str(e))


@socketio.on("player_move")
def handle_player_move(data):
    try:
        index = data.get("index")
        symbol = data.get("symbol")

        result = game.make_move(request.sid, index, symbol)

        if "winner" in result:
            emit("game_update", {
                "board": game.board,
                "turn": None,
                "winner": result["winner"]
            }, broadcast=True)
            logger.info("game_winner", player=result["winner"], details=f"Player {result['winner']} won")
        else:
            emit("game_update", {
                "board": game.board,
                "turn": result["turn"]
            }, broadcast=True)
            logger.info("player_move", player=request.sid, details=f"Player {symbol} moved to {index}")

    except InvalidMoveError as e:
        emit("error_message", {"error": str(e)}, to=request.sid)
        logger.warning("invalid_move", player=request.sid, details=str(e))
    except Exception as e:
        emit("error_message", {"error": f"Unexpected error: {e}"}, to=request.sid)
        logger.error("unexpected_error_player_move", player=request.sid, details=str(e))
