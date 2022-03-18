const grid0 = document.getElementById("grid1");
const grid1 = document.getElementById("grid2");

const playable_board_size = 10;
let id = 0;

const board_size = playable_board_size + 1;
const board_style = `grid: repeat(${board_size}, 1fr) / repeat(${board_size}, 1fr);`;
grid0.style = grid1.style = board_style;

const char = "abcdefghijklmnopqrstuvwxyz";

class SinglePlayerGame {
  constructor(board0, board1, grid0, grid1) {
    //corresponds to Battleship.players["ships"] on the backend
    this.board0 = board0;
    this.board1 = board1;
    // corresponds to Battleship.players["hits board"] on the backend
    this.grid0 = grid0;
    this.grid1 = grid1;
    // corresponds to Battleship.current_player
    this.currentPlayer = 0;
    this._vertical = false;
  }
  get vertical() {
    return this._vertical;
  }
  set vertical(newValue) {
    if (this.board0.canGameStart && this.board1.canGameStart) return;
    this.renderBoard(
      this.currentPlayer,
      this.currentPlayerGridElement,
      this.currentPlayerBoard
    );
    this._vertical = newValue;
    return newValue;
  }
  get shootingPhase() {
    return this.board0.canGameStart && this.board1.canGameStart;
  }
  get gameFinished() {
    return this.board0.allSunk || this.board1.allSunk;
  }
  get opponentPlayer() {
    return this.currentPlayer === 0 ? 1 : 0;
  }
  get currentPlayerBoard() {
    return this.currentPlayer === 0 ? this.board0 : this.board1;
  }
  set currentPlayerBoard(newBoard) {
    if (this.currentPlayer === 0) {
      this.board0 = newBoard;
    } else if (this.currentPlayer === 1) {
      this.board1 = newBoard;
    } else throw new Error();
  }
  set opponentPlayerBoard(newBoard) {
    if (this.currentPlayer === 1) {
      this.board0 = newBoard;
    } else if (this.currentPlayer === 0) {
      this.board1 = newBoard;
    } else throw new Error();
  }
  get opponentPlayerBoard() {
    return this.currentPlayer === 0 ? this.board1 : this.board0;
  }
  get currentPlayerGridElement() {
    return this.currentPlayer === 0 ? this.grid0 : this.grid1;
  }
  get opponentPlayerGridElement() {
    return this.currentPlayer === 0 ? this.grid1 : this.grid0;
  }
  getBoardElement(row, col, player) {
    return document.getElementById(`id_${player}_${row}_${col}`);
  }
  mouseEnterHandler(htmlElement) {
    const [, player, row, col] = htmlElement.id
      .split("_")
      .map((v) => Number.parseInt(v));
    if (player != this.currentPlayer) return;
    if (!this.currentPlayerBoard.canGameStart) {
      let shipsLeft = this.currentPlayerBoard.shipsToPlace.slice(0);
      let shipLength = shipsLeft.shift();
      let viable_squares = this.currentPlayerBoard.checkShipPlacement(
        row,
        col,
        shipLength,
        this.vertical
      );
      let badSquares = this.currentPlayerBoard.checkBadSquares(
        row,
        col,
        shipLength,
        this.vertical
      );
      for (let [row, col] of viable_squares) {
        this.getBoardElement(row, col, this.currentPlayer).style =
          "background-color: grey;";
      }
      for (let [row, col] of badSquares) {
        this.getBoardElement(row, col, this.currentPlayer).style =
          "background-color: red;";
      }
    }
  }
  mouseLeaveHandler(htmlElement) {
    const [, player, row, col] = htmlElement.id
      .split("_")
      .map((v) => Number.parseInt(v));
    if (player != this.currentPlayer) return;
    if (!this.currentPlayerBoard.canGameStart) {
      let shipsLeft = this.currentPlayerBoard.shipsToPlace.slice(0);
      let shipLength = shipsLeft.shift();
      let viable_squares = this.currentPlayerBoard.checkShipPlacement(
        row,
        col,
        shipLength,
        this.vertical
      );
      let badSquares = this.currentPlayerBoard.checkBadSquares(
        row,
        col,
        shipLength,
        this.vertical
      );
      for (let [row, col] of viable_squares) {
        this.getBoardElement(row, col, this.currentPlayer).style = "";
      }
      for (let [row, col] of badSquares) {
        this.getBoardElement(row, col, this.currentPlayer).style = "";
      }
    }
  }

  playerTurnFinishedHandler() {
    if (this.board0.canGameStart && this.board1.canGameStart) {
      this.renderBoard(
        this.currentPlayer,
        this.currentPlayerGridElement,
        this.currentPlayerBoard,
        true
      );
      this.currentPlayer = this.opponentPlayer;
      if (this.board1.allSunk) {
        console.log("Player 1 Wins!");
      }
      if (this.board0.allSunk) {
        console.log("Player 2 Wins!");
      }
    }
    if (this.board0.canGameStart && !this.board1.canGameStart) {
      this.renderBoard(
        this.currentPlayer,
        this.currentPlayerGridElement,
        this.currentPlayerBoard,
        true
      );
      this.currentPlayer = 1;
      this.renderBoard(
        this.currentPlayer,
        this.currentPlayerGridElement,
        this.currentPlayerBoard
      );
    }
  }
  mouseClickHandler(htmlElement) {
    const [, player, row, col] = htmlElement.id
      .split("_")
      .map((v) => Number.parseInt(v));
    if (this.gameFinished) return;
    if (this.shootingPhase) {
      if (player === this.opponentPlayer) {
        if (
          this.opponentPlayerBoard.array[row][col] === -1 ||
          this.opponentPlayerBoard.array[row][col].sunk === true
        )
          return;
        this.opponentPlayerBoard = this.opponentPlayerBoard.shootSquare(
          row,
          col
        );
        this.renderBoard(
          this.opponentPlayer,
          this.opponentPlayerGridElement,
          this.opponentPlayerBoard,
          true
        );
        this.playerTurnFinishedHandler();
      }
    }
    if (!this.currentPlayerBoard.canGameStart) {
      let shipsLeft = this.currentPlayerBoard.shipsToPlace.slice(0);
      let shipLength = shipsLeft.shift();
      let viable_squares = this.currentPlayerBoard.checkShipPlacement(
        row,
        col,
        shipLength,
        this.vertical
      );
      if (viable_squares.length === 0) return;
      this.currentPlayerBoard.placeShip(row, col, shipLength, this.vertical);
      this.renderBoard(
        this.currentPlayer,
        this.currentPlayerGridElement,
        this.currentPlayerBoard
      );

      this.playerTurnFinishedHandler();
    }
  }
  renderBoard(player, gridElement, board, hideShips) {
    while (gridElement.firstChild)
      gridElement.removeChild(gridElement.lastChild); //Clear the board
    for (let i = 0; i < board_size; i++) {
      for (let j = 0; j < board_size; j++) {
        const node = document.createElement("div");
        node.className = "square";
        node.style =
          "display: flex; align-items: center; justify-content: center;";
        if (i === 0 && j === 0) {
        } else if (i === 0) {
          node.innerHTML = char.charAt(j - 1).toUpperCase();
        } else if (j === 0) {
          node.innerHTML = i;
        } else {
          node.id = `id_${player}_${i - 1}_${j - 1}`;
          const boardValue = board.getElement(i - 1, j - 1);
          if (boardValue === -1) {
            node.style = "background-color: darkblue;";
          }
          if (typeof boardValue === "object" && boardValue.sunk) {
            node.style = "background-color: red;";
          }
          if (typeof boardValue === "object" && !boardValue.sunk) {
            if (!hideShips) node.style = "background-color: purple;";
          }
          node.addEventListener("mouseleave", (e) => {
            this.mouseLeaveHandler(e.target, gridElement);
          });
          node.addEventListener("mouseenter", (e) => {
            this.mouseEnterHandler(e.target, gridElement);
          });
          node.addEventListener("click", (e) => {
            this.mouseClickHandler(e.target, gridElement);
          });
        }

        gridElement.appendChild(node);
        gridElement;
      }
    }
  }
  hoverGuide() {}
  startGame() {
    this.renderBoard(
      this.currentPlayer,
      this.currentPlayerGridElement,
      this.currentPlayerBoard
    );
  }
  saveGame() {
    return {
      board0: this.board0.save(),
      board1: this.board1.save(),
      currentPlayer: this.currentPlayer,
    };
  }
}

class Board {
  constructor() {
    //corresponds to Battleship.ship_sizes on the backend
    this.shipsToPlace = [5, 4, 3, 3, 2];
    //[{shipLength, uniqueShipId, row, col, vertical}, ...]
    this.shipsPlaced = [];

    this.array = Array.from({ length: playable_board_size }, () =>
      Array.from({ length: playable_board_size }, () => 0)
    );
  }
  get canGameStart() {
    return this.shipsToPlace.length === 0;
  }
  getElement(row, col) {
    //0 means empty
    //[sunk, shipLength, id] means a ship. Every part of that ship has the same id
    //-1 means miss
    return this.array[row][col];
  }
  checkShipPlacement(row, col, shipLength, vertical) {
    if (vertical) {
      const viable_squares = [];

      for (let i = 0; i < shipLength; i++) {
        const currentSquare = this.array[row + i]?.[col];
        if (currentSquare !== 0 || currentSquare === undefined) {
          return [];
        }
        viable_squares.push([row + i, col]);
      }
      return viable_squares;
    } else {
      const viable_squares = [];
      for (let i = 0; i < shipLength; i++) {
        const currentSquare = this.array[row]?.[col + i];
        if (currentSquare !== 0 || currentSquare === undefined) {
          return [];
        }
        viable_squares.push([row, col + i]);
      }
      return viable_squares;
    }
  }
  checkBadSquares(row, col, shipLength, vertical) {
    if (vertical) {
      const viable_squares = [];

      for (let i = 0; i < shipLength; i++) {
        const currentSquare = this.array[row + i]?.[col];
        if (currentSquare !== 0 || currentSquare === undefined) {
          return viable_squares;
        }
        viable_squares.push([row + i, col]);
      }
      return [];
    } else {
      const viable_squares = [];
      for (let i = 0; i < shipLength; i++) {
        const currentSquare = this.array[row]?.[col + i];
        if (currentSquare !== 0 || currentSquare === undefined) {
          return viable_squares;
        }
        viable_squares.push([row, col + i]);
      }
      return [];
    }
  }
  clone() {
    const board_copy = new Board();
    board_copy.array = JSON.parse(JSON.stringify(this.array));
    board_copy.shipsPlaced = JSON.parse(JSON.stringify(this.shipsPlaced));
    board_copy.shipsToPlace = JSON.parse(JSON.stringify(this.shipsToPlace));
    return board_copy;
  }
  load(o) {
    this.array = o.array;
    this.shipsPlaced = o.shipsPlaced;
    this.shipsToPlace = o.shipsToPlace;
    return this;
  }
  save() {
    return JSON.parse(JSON.stringify(this));
  }
  placeShip(row, col, shipLength, vertical) {
    if (this.shipsToPlace.length === 0)
      throw new Error("Board had no ships left to place!");
    if (!this.shipsToPlace.includes(shipLength))
      throw new Error(`Ship length of ${shipLength} not in Board's ship array`);
    const viable_squares = this.checkShipPlacement(
      row,
      col,
      shipLength,
      vertical
    );
    if (viable_squares.length === 0)
      throw new Error("Not a valid ship placement!");
    const uniqueShipId = id++;

    this.shipsPlaced.push({ shipLength, uniqueShipId, row, col, vertical });
    for (const square of viable_squares) {
      const [row, col] = square;
      this.array[row][col] = { sunk: false, shipLength, uniqueShipId };
    }
    this.shipsToPlace[this.shipsToPlace.findIndex((v) => v === shipLength)] =
      undefined;
    this.shipsToPlace = this.shipsToPlace.filter((v) => v !== undefined);
  }

  shootSquare(row, col) {
    const boardCopy = this.clone();
    let squareValue = boardCopy.array[row][col];
    if (squareValue === 0) {
      boardCopy.array[row][col] = -1;
    } else if (typeof squareValue === "object") {
      squareValue.sunk = true;
    }
    return boardCopy;
  }
  get allSunk() {
    if (!this.canGameStart) return false;
    for (let i = 0; i < this.array.length; i++) {
      for (let j = 0; j < this.array[0].length; j++) {
        if (typeof this.array[i][j] === "object" && !this.array[i][j].sunk)
          return false;
      }
    }
    return true;
  }
}

let currentGame = new SinglePlayerGame(new Board(), new Board(), grid0, grid1);
document.addEventListener("keypress", (e) => {
  if (e.key === "r") currentGame.vertical = !currentGame.vertical;
});
currentGame.startGame();
