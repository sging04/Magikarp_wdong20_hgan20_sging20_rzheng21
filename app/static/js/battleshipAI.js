const grid0 = document.getElementById("grid1");
const grid1 = document.getElementById("grid2");
const messageBox = document.getElementById("messageBox");
const restartGame = document.getElementById("restartGame");
const saveGame = document.getElementById("saveGame");
const moveForward = document.getElementById("moveForward");
const moveBackward = document.getElementById("moveBackward");

let doNotUpdateWin = false;

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
    this.renderBothBoards();
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
    if (currentlyViewing !== boardHistory.length - 1) return; //move gui
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
    if (currentlyViewing !== boardHistory.length - 1) return; //move gui
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

  mouseClickHandler(htmlElement) {
    const [, player, row, col] = htmlElement.id
      .split("_")
      .map((v) => Number.parseInt(v));
    //Board Move GUI
    if (currentlyViewing !== boardHistory.length - 1) {
      currentlyViewing = boardHistory.length - 1;
      let modifiedBoardBugFix = JSON.parse(
        JSON.stringify(boardHistory[currentlyViewing][1])
      );
      if (modifiedBoardBugFix.currentPlayer === 0)
        modifiedBoardBugFix.currentPlayer = 1;
      else if (modifiedBoardBugFix.currentPlayer === 1)
        modifiedBoardBugFix.currentPlayer = 0;
      currentGame = SinglePlayerGame.loadGame(
        modifiedBoardBugFix,
        grid0,
        grid1
      );
      if (!currentGame.shootingPhase) {
        if (modifiedBoardBugFix.currentPlayer === 0)
          modifiedBoardBugFix.currentPlayer = 1;
        else if (modifiedBoardBugFix.currentPlayer === 1)
          modifiedBoardBugFix.currentPlayer = 0;
      }
      currentGame.renderBothBoards();
      return;
    }
    //Can't make any board modifications if game is finished
    if (this.gameFinished) return;
    //If ship have all been placed (shooting phase) and the opponent player's board was clicked
    // Steps:
    // Player makes a move
    // setTimeout and then computer makes a move
    if (
      this.currentPlayer === 0 &&
      this.shootingPhase &&
      player === this.opponentPlayer
    ) {
      if (
        this.opponentPlayerBoard.array[row][col] === -1 ||
        this.opponentPlayerBoard.array[row][col].sunk === true
      )
        return;
      this.opponentPlayerBoard = this.opponentPlayerBoard.shootSquare(row, col);
      boardHistory.push([
        `${char[col].toUpperCase()}${row + 1}`,
        SinglePlayerGame.saveGame(currentGame),
        typeof this.opponentPlayerBoard.array[row][col] === "object" &&
          this.opponentPlayerBoard.array[row][col].sunk,
      ]);
      currentlyViewing = boardHistory.length - 1;

      this.currentPlayer = this.opponentPlayer;

      //Computer player makes a move
      setTimeout(() => {
        if (this.board0.allSunk || this.board1.allSunk) return;
        let good_squares = [];
        for (let row = 0; row < 10; row++) {
          for (let col = 0; col < 10; col++) {
            if (
              this.opponentPlayerBoard.array[row][col] === -1 ||
              this.opponentPlayerBoard.array[row][col].sunk === true
            )
              continue;
            else {
              good_squares.push([row, col]);
            }
          }
        }
        let [rowGuess, colGuess] =
          good_squares[Math.floor(Math.random() * good_squares.length)];
        this.opponentPlayerBoard = this.opponentPlayerBoard.shootSquare(
          rowGuess,
          colGuess
        );
        boardHistory.push([
          `${char[colGuess].toUpperCase()}${rowGuess + 1}`,
          SinglePlayerGame.saveGame(currentGame),
          typeof this.opponentPlayerBoard.array[rowGuess][colGuess] ===
            "object" && this.opponentPlayerBoard.array[rowGuess][colGuess].sunk,
        ]);
        currentlyViewing = boardHistory.length - 1;

        this.currentPlayer = this.opponentPlayer;
        this.renderBothBoards();
      }, 300);
    }
    //If player 0 clicked their own board and they still need to place all their ships

    if (
      this.currentPlayer === 0 &&
      player === this.currentPlayer &&
      !this.currentPlayerBoard.canGameStart
    ) {
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

      if (this.currentPlayerBoard.shipsToPlace.length === 0) {
        this.currentPlayer = this.opponentPlayer;
        boardHistory.push([
          `${char[col].toUpperCase()}${row + 1}`,
          SinglePlayerGame.saveGame(currentGame),
        ]);
        currentlyViewing = boardHistory.length - 1;
        while (this.currentPlayerBoard.shipsToPlace.length != 0) {
          let shipsLeft = this.currentPlayerBoard.shipsToPlace.slice(0);
          let shipLength = shipsLeft.shift();
          let goodSquares = [];
          let verticalOrHorizontal = Math.random() < 0.5;
          for (let row = 0; row < 10; row++) {
            for (let col = 0; col < 10; col++) {
              let viable_squares = this.currentPlayerBoard.checkShipPlacement(
                row,
                col,
                shipLength,
                verticalOrHorizontal
              );
              if (viable_squares.length != 0) goodSquares.push([row, col]);
            }
          }
          let [randomRow, randomCol] =
            goodSquares[Math.floor(Math.random() * goodSquares.length)];
          this.currentPlayerBoard.placeShip(
            randomRow,
            randomCol,
            shipLength,
            verticalOrHorizontal
          );
          boardHistory.push([
            `${char[randomCol].toUpperCase()}${randomRow + 1}`,
            SinglePlayerGame.saveGame(currentGame),
          ]);
          currentlyViewing = boardHistory.length - 1;
        }
        this.currentPlayer = this.opponentPlayer;
      } else {
        boardHistory.push([
          `${char[col].toUpperCase()}${row + 1}`,
          SinglePlayerGame.saveGame(currentGame),
        ]);
        currentlyViewing = boardHistory.length - 1;
      }
    }

    this.renderBothBoards();
  }
  renderBothBoards() {
    let latestGame = boardHistory[boardHistory.length - 1][1];
    let board0object = Board.load(latestGame.board0);
    let board1object = Board.load(latestGame.board1);
    let isGameFinished = board0object.allSunk || board1object.allSunk;

    if (board1object.allSunk) {
      if (doNotUpdateWin === false) {
        postData("/api/updateGame", {
          gamemode: "ai",
          game: boardHistory,
        });
        postData("/api/addWin").then((res) => {
          console.log(res);
        });
        doNotUpdateWin = true;
      }
    }

    if (isGameFinished) {
      this.renderBoard(0, grid0, this.board0, false);
      this.renderBoard(1, grid1, this.board1, false);
    } else {
      this.renderBoard(0, grid0, this.board0, false);
      this.renderBoard(1, grid1, this.board1, true);
    }
    if (this.shootingPhase) {
      if (this.currentPlayer === 0) messageBox.innerHTML = `Your turn`;
      if (
        this.currentPlayer === 0 &&
        currentlyViewing != boardHistory.length - 1
      ) {
        messageBox.innerHTML = `(Viewing) Your move`;
      }
      if (this.currentPlayer === 1) messageBox.innerHTML = `Computer's turn`;
      if (
        this.currentPlayer === 1 &&
        currentlyViewing != boardHistory.length - 1
      ) {
        messageBox.innerHTML = `(Viewing) Computer's move`;
      }
    } else {
      if (this.currentPlayer === 0)
        messageBox.innerHTML = `Please place your ships`;
      if (
        this.currentPlayer === 0 &&
        currentlyViewing != boardHistory.length - 1
      ) {
        messageBox.innerHTML = `(Viewing) Your ship placements`;
      }

      if (this.currentPlayer === 1)
        messageBox.innerHTML = `(Viewing) Computer ship placements`;
    }
    if (this.board1.allSunk) {
      messageBox.innerHTML = "You won!";
    }
    if (this.board0.allSunk) {
      messageBox.innerHTML = "Computer Won!";
    }

    //Player move gui
    let moves = document.getElementById("moves");
    while (moves.firstChild) moves.removeChild(moves.lastChild);

    for (let i = 0; i < boardHistory.length; i++) {
      const node = document.createElement("div");

      if (!isGameFinished && i >= 6 && i <= 10) {
        node.innerHTML = `${i + 1}. --`;
      } else {
        node.innerHTML = `${i + 1}. ${boardHistory[i][0]}`;
      }

      if (i === currentlyViewing && boardHistory[i][2])
        node.style = "background-color: yellow; color: red;";
      else if (boardHistory[i][2]) node.style = "color: red;";
      else if (i === currentlyViewing) node.style = "background-color: yellow";

      node.addEventListener("click", () => {
        currentlyViewing = i;
        let isShootingPhase = SinglePlayerGame.loadGame(
          JSON.parse(JSON.stringify(boardHistory[currentlyViewing][1])),
          grid0,
          grid1
        ).shootingPhase;
        if (currentlyViewing === boardHistory.length - 1 && isShootingPhase) {
          let modifiedBoardBugFix = JSON.parse(
            JSON.stringify(boardHistory[currentlyViewing][1])
          );
          if (modifiedBoardBugFix.currentPlayer === 0)
            modifiedBoardBugFix.currentPlayer = 1;
          else if (modifiedBoardBugFix.currentPlayer === 1)
            modifiedBoardBugFix.currentPlayer = 0;
          currentGame = SinglePlayerGame.loadGame(
            modifiedBoardBugFix,
            grid0,
            grid1
          );
          currentGame.renderBothBoards();
        } else {
          currentGame = SinglePlayerGame.loadGame(
            boardHistory[currentlyViewing][1],
            grid0,
            grid1
          );
          currentGame.renderBothBoards();
        }
        return;
      });
      moves.appendChild(node);
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
      }
    }
  }
  startGame() {
    this.renderBothBoards();
  }
  static saveGame(SinglePlayerGame) {
    return {
      board0: Board.save({ ...SinglePlayerGame.board0 }),
      board1: Board.save({ ...SinglePlayerGame.board1 }),
      currentPlayer: SinglePlayerGame.currentPlayer,
    };
  }
  static loadGame(o, grid1, grid2) {
    let board0 = Board.load(o.board0);
    let board1 = Board.load(o.board1);
    let newGame = new SinglePlayerGame(board0, board1, grid1, grid2);
    newGame.currentPlayer = o.currentPlayer;
    currentGame = newGame;
    newGame.renderBothBoards();
    return newGame;
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
  static load(o) {
    let newBoard = new Board();
    newBoard.array = JSON.parse(JSON.stringify(o.array));
    newBoard.shipsPlaced = JSON.parse(JSON.stringify(o.shipsPlaced));
    newBoard.shipsToPlace = JSON.parse(JSON.stringify(o.shipsToPlace));
    return newBoard;
  }
  static save(board) {
    return JSON.parse(JSON.stringify(board));
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

let boardHistory = [
  [
    "Start",
    SinglePlayerGame.saveGame(
      new SinglePlayerGame(new Board(), new Board(), grid0, grid1)
    ),
  ],
];
let currentlyViewing = 0;

let currentGame = new SinglePlayerGame(new Board(), new Board(), grid0, grid1);
document.addEventListener("keypress", (e) => {
  if (e.key === "r") {
    currentGame.vertical = !currentGame.vertical;
  }
});
currentGame.startGame();

postData("/api/fetchGame", {
  gamemode: "ai",
}).then((json) => {
  if (json.game === false) {
  } else {
    boardHistory = json.game;
    currentlyViewing = boardHistory.length - 1;

    let latestGame = boardHistory[boardHistory.length - 1][1];
    let board0object = Board.load(latestGame.board0);
    let board1object = Board.load(latestGame.board1);

    if (board1object.allSunk) {
      console.log("Stopping win update");
      doNotUpdateWin = true;
    }

    currentGame = SinglePlayerGame.loadGame(
      boardHistory[currentlyViewing][1],
      grid0,
      grid1
    );

    currentGame.renderBothBoards();

    if (currentGame.shootingPhase) {
      currentlyViewing = boardHistory.length - 1;
      let modifiedBoardBugFix = JSON.parse(
        JSON.stringify(boardHistory[currentlyViewing][1])
      );
      if (modifiedBoardBugFix.currentPlayer === 0)
        modifiedBoardBugFix.currentPlayer = 1;
      else if (modifiedBoardBugFix.currentPlayer === 1)
        modifiedBoardBugFix.currentPlayer = 0;
      currentGame = SinglePlayerGame.loadGame(
        modifiedBoardBugFix,
        grid0,
        grid1
      );
      currentGame.renderBothBoards();
    }
    return;
  }
});

restartGame.addEventListener("click", () => {
  boardHistory = [
    [
      "Start",
      SinglePlayerGame.saveGame(
        new SinglePlayerGame(new Board(), new Board(), grid0, grid1)
      ),
    ],
  ];
  currentlyViewing = 0;
  currentGame = new SinglePlayerGame(new Board(), new Board(), grid0, grid1);
  currentGame.startGame();
  postData("/api/updateGame", {
    gamemode: "ai",
    game: boardHistory,
  }).then((json) => {
    console.log(json);
  });
});

saveGame.addEventListener("click", () => {
  postData("/api/updateGame", {
    gamemode: "ai",
    game: boardHistory,
  })
    .then((json) => {
      window.location.href = "/";
    })
    .catch((json) => {
      console.log("error saving");
      window.location.href = "/";
    });
});

moveForward.addEventListener("click", () => {
  if (currentlyViewing === boardHistory.length - 1) return;
  currentlyViewing++;
  let isShootingPhase = SinglePlayerGame.loadGame(
    JSON.parse(JSON.stringify(boardHistory[currentlyViewing][1])),
    grid0,
    grid1
  ).shootingPhase;
  if (currentlyViewing === boardHistory.length - 1 && isShootingPhase) {
    let modifiedBoardBugFix = JSON.parse(
      JSON.stringify(boardHistory[currentlyViewing][1])
    );
    if (modifiedBoardBugFix.currentPlayer === 0)
      modifiedBoardBugFix.currentPlayer = 1;
    else if (modifiedBoardBugFix.currentPlayer === 1)
      modifiedBoardBugFix.currentPlayer = 0;
    currentGame = SinglePlayerGame.loadGame(modifiedBoardBugFix, grid0, grid1);
    currentGame.renderBothBoards();
  } else {
    currentGame = SinglePlayerGame.loadGame(
      boardHistory[currentlyViewing][1],
      grid0,
      grid1
    );
    currentGame.renderBothBoards();
  }
  currentGame.renderBothBoards();
});

moveBackward.addEventListener("click", () => {
  if (currentlyViewing === 0) return;
  currentlyViewing--;
  currentGame = SinglePlayerGame.loadGame(
    boardHistory[currentlyViewing][1],
    grid0,
    grid1
  );
  currentGame.renderBothBoards();
});

async function postData(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "post",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return response.json(); // parses JSON response into native JavaScript objects
}
