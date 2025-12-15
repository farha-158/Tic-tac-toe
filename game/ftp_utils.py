from ftplib import FTP
import os
from dotenv import load_dotenv


load_dotenv()
def save_game_result(player1, player2, winner):
    folder = "ftpFiles"  
    os.makedirs(folder, exist_ok=True)  

    filename = f"{player1}_vs_{player2}.txt"
    filepath = os.path.join(folder, filename)  

    with open(filepath, "w") as f:
        f.write(f"Player 1: {player1}\n")
        f.write(f"Player 2: {player2}\n")
        f.write(f"Winner: {winner}\n")
    return filepath

def upload_to_ftp(filename):
    ftp = FTP()
    ftp.connect("127.0.0.1", 21)
    ftp.login(os.getenv("FTP_NAME"), os.getenv("FTP_PASSWORD"))
    
    with open(filename, "rb") as file:
        ftp.storbinary(f"STOR {os.path.basename(filename)}", file)
    
    ftp.quit()
    print(f"{filename} uploaded successfully!")

