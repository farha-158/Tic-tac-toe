# events.py
from flask import request
from flask_socketio import emit
from .extensions import socketio
from .logic.logic import TicTacToeGame
from .logic.logicException import InvalidMoveError, TooManyPlayersError
from .logger import logger  
from .ftp_utils import upload_to_ftp, save_game_result 
from .localhost import send_local_email
from .email_utils_imap import fetch_inbox_emails
from .email_utils_pop3 import fetch_inbox_emails_pop3
from .real_email import send_real_email
from dotenv import load_dotenv
import os

load_dotenv()
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
            
            player1 = game.players[0]["username"]
            player2 = game.players[1]["username"]
            winner = result["winner"]

            filename = save_game_result(player1, player2, winner)

            upload_to_ftp(filename)

            body = f"The game between {player1} and {player2} has finished. Winner: {winner}!"

            # إرسال إيميل محلي
            send_local_email( os.getenv("EMAIL_TEST"),"Tic-Tac-Toe Result", body)
            send_local_email( os.getenv("EMAIL_pop3"),"Tic-Tac-Toe Result", body)
            send_real_email("Tic-Tac-Toe Result", body)

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

@socketio.on("fetch_imap_emails")
def fetch_imap_emails_event():
    try:
        emails = fetch_inbox_emails(os.getenv("EMAIL_TEST"), os.getenv("PASSWORD_TEST"))
        emit("emails_data", {"emails": emails})
    except Exception as e:
        emit("emails_data", {"emails": [], "error": str(e)})

@socketio.on("fetch_pop3_emails")
def fetch_pop3_emails_event():
    try:
        emails = fetch_inbox_emails_pop3(os.getenv("EMAIL_pop3"), os.getenv("PASSWORD_POP3"))  
        emit("emails_data", {"emails": emails})
        # emit("emails_data", {"emails": 'emails'})

    except Exception as e:
        emit("emails_data", {"emails": [], "error": str(e)})
