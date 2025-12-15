// chatapp/static/js/main.js
const socket = io({ autoConnect: false });
let username = "";
let symbol = "";

const landing = document.getElementById("landing");
const waiting = document.getElementById("waiting");
const gameBox = document.getElementById("game");
const boardEl = document.getElementById("board");
const turnInfo = document.getElementById("turn-info");
const winnerMsg = document.getElementById("winner-message");

landing.addEventListener("submit", e => {
  e.preventDefault();
  username = document.getElementById("username").value.trim();
  if (!username) return;
  socket.connect();
  socket.emit("user_join", username);
  landing.style.display = "none";
});

socket.on("waiting_for_user", () => {
  waiting.style.display = "block";
  gameBox.style.display = "none";
});

socket.on("ready_to_play", data => {
  symbol = data.symbol;
  waiting.style.display = "none";
  gameBox.style.display = "block";
});

socket.on("game_update", data => {
  const { board, turn, winner } = data;
  boardEl.innerHTML = "";
  winnerMsg.style.display = "none";

  board.forEach((cell, i) => {
    const cellEl = document.createElement("div");
    cellEl.textContent = cell || "";
    if (cell) cellEl.classList.add("filled");

    cellEl.onclick = () => {
      // send move only if it's our turn and cell empty
      if (!cell && turn === username) {
        socket.emit("player_move", { index: i, symbol });
      }
    };

    boardEl.appendChild(cellEl);
  });

  if (winner) {
    if (winner === "Draw") {
      turnInfo.textContent = "It's a Draw!";
      winnerMsg.textContent = "🤝 Game ended in a draw.";
      boardEl.style.display='none'

    } else {
      const msg = (winner === username) ? "🎉 You Win!" : "😢 You Lose!";
      turnInfo.textContent = `Winner: ${winner}`;
       boardEl.style.display='none'

      winnerMsg.textContent = msg;

    }
    winnerMsg.style.display = "block";
  } else {
    turnInfo.textContent = `Turn: ${turn || "—"}`;
  }
});

socket.on("opponent_left", data => {
  alert(data.msg || "Opponent left.");
  // show waiting screen
  gameBox.style.display = "none";
  waiting.style.display = "block";
});

socket.on("error_message", data => {
  alert(`⚠️ ${data.error}`);
});


