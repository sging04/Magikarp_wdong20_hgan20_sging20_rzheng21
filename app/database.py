import sqlite3

class Database:
    def __init__(self, db_file: str):
        self.db = sqlite3.connect(db_file)
        self.cur = self.db.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY,
              username TEXT,
              password TEXT,
              profile_picture TEXT,
              wins INTEGER )""") #insert wins

        # TODO: Create database for saved games
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS games(
              game_id INTEGER PRIMARY KEY,
              player_one_id TEXT,
              player_two_id TEXT,
              player_one_won INTEGER
              game TEXT )""") 

        self.db.commit()


    def close(self):
        self.db.close()

    def add_game(self, player_one_id, player_two_id, player_one_won, game):
        self.cur.execute("""
            INSERT INTO games(
              player_one_id,
              player_two_id,
              player_one_won,
              game ) VALUES(?, ?, ?, ?)""", player_one_id, player_two_id, player_one_won, game)
        self.db.commit()
        return self.cur.lastrowid #game id
    
    def fetch_game(self, game_id):
        result = self.cur.execute("""
            SELECT game_id, player_one_id, player_two_id, player_one_won, game
            FROM   users
            WHERE  game_id = ?
        """, [game_id]).fetchone()
        return result 

    def update_game(self, game_id, game, player_one_won):
        self.cur.execute("""
            UPDATE games
               SET player_one_won = ?, game = ?
             WHERE game_id = ?""", (player_one_won, game, game_id))

    def delete_game(self, game_id):
        self.cur.execute("""
        DELETE FROM table
WHERE search_condition;
        """)

    def fetch_user(self, username: str, password: str) -> int:
        """
        Gets the id of the user with the given username/password combination from the database.
        Returns None if the combination is incorrect.
        """

        self.cur.execute("""
            SELECT id
            FROM   users
            WHERE  LOWER(username) = LOWER(?)
            AND    password = ?
        """, (username, password))

        # user_id is None if no matches were found
        user_id = self.cur.fetchone()

        return index_nullable(user_id, 0)


    def register_user(self, username: str, password: str, default_avatar: str = "") -> bool:
        """
        Tries to add the given username and password into the database.
        Returns False if the user already exists, True if it successfully added the user.
        """
        self.cur.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,))
        row = self.cur.fetchone()

        if row is not None: #make sure user doesn't already exist
            return False

        self.cur.execute("""
            INSERT INTO users(
              username,
              password,
              profile_picture,
              wins ) VALUES(?, ?, ?, ?)""", (username, password, default_avatar, 0))
        self.db.commit()
        return True


    def fetch_username(self, user_id: int) -> str:
        """
        Returns the username of the user with the given id.
        """
        self.cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        username = index_nullable(self.cur.fetchone(), 0)

        return username


    def set_picture(self, user_id: int, img: str) -> bool:
        """
        Updates the profile picture of the user with the given id.
        Returns if the user exists.
        """
        if self.fetch_picture(user_id) is None:
            return False

        self.cur.execute("""
            UPDATE users
               SET profile_picture = ?
             WHERE id = ?""", (img, user_id))

        self.db.commit()

        return True

    # def fetchAllUsers(self):
    #     self._cursor.execute(f'SELECT rowid,* FROM {self._name};')
    #     return self._cursor.fetchall()    # def fetchAllUsers(self):
    #     self._cursor.execute(f'SELECT rowid,* FROM {self._name};')
    #     return self._cursor.fetchall()


    def fetch_picture(self, user_id) -> str:
        """
        Returns the profile picture of the user with the given id.
        """
        self.cur.execute("SELECT profile_picture FROM users WHERE id = ?", (user_id,))
        img = index_nullable(self.cur.fetchone(), 0)

        return img

    def add_win(self, user_id) -> int:
        self.cur.execute("SELECT user FROM users WHERE id = ?", (user_id,))
        wins = index_nullable(self.cur.fetchone(), 0)
        wins+= 1;
        self.cur.execute("""
            UPDATE users
               SET wins = ?
             WHERE id = ?""", (wins, user_id))
        self.db.commit()
        return wins

    def fetch_wins(self, user_id) -> int:
        self.cur.execute("SELECT user FROM users WHERE id = ?", (user_id,))
        wins = index_nullable(self.cur.fetchone(), 0)
        return wins

def index_nullable(nullable, index: int):
    if nullable is not None:
	    return nullable[index]
