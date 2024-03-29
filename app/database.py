import json
import sqlite3
from os import path

dir = str(path.dirname(__file__)) + '/'

class Database:
    def __init__(self, db_file: str):
        self.db = sqlite3.connect(dir + db_file)
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
              user_id INTEGER,
              gamemode TEXT,
              game TEXT )""") 

        self.db.commit()


    def close(self):
        self.db.close()
    
    def fetch_game(self, user_id, gamemode):
        print(user_id, gamemode)
        result = self.cur.execute("""
            SELECT game
            FROM   games
            WHERE  user_id = ? and gamemode = ?
        """, [user_id, gamemode]).fetchone()
        if(result == None):
            return None
        else: 
            return json.loads(result[0])

    def update_game(self, user_id, gamemode, game):
        if(self.fetch_game(user_id, gamemode) != None):
            self.cur.execute("""
                UPDATE games
                SET game = ?
                WHERE user_id = ? and gamemode = ?""", (game, user_id, gamemode))
        else:
            self.cur.execute("""
            INSERT INTO games(user_id, gamemode, game) VALUES(?, ?, ?)""", [user_id, gamemode, game])
        self.db.commit()


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


    def fetch_all_users(self):
        """
        Returns a list of all users and their relevant information
        as a list of dictionaries.
        Orders them by the number of wins.
        """

        self.cur.execute("""
            SELECT * FROM users
            ORDER BY wins DESC
        """)
        users = self.cur.fetchall()

        users_list = []
        for id, name, _pwd, img, wins in users:
            users_list.append({
                "id": id,
                "name": name,
                "avatar": img,
                "wins": wins,
            })

        return users_list


    def fetch_picture(self, user_id) -> str:
        """
        Returns the profile picture of the user with the given id.
        """
        self.cur.execute("SELECT profile_picture FROM users WHERE id = ?", (user_id,))
        img = index_nullable(self.cur.fetchone(), 0)

        return img

    def add_win(self, user_id) -> int:
        self.cur.execute("SELECT wins FROM users WHERE id = ?", (user_id,))
        wins = index_nullable(self.cur.fetchone(), 0)
        wins+= 1
        self.cur.execute("""
            UPDATE users
               SET wins = ?
             WHERE id = ?""", (wins, user_id))
        self.db.commit()
        return wins

    def fetch_wins(self, user_id) -> int:
        self.cur.execute("SELECT wins FROM users WHERE id = ?", (user_id,))
        wins = index_nullable(self.cur.fetchone(), 0)
        return wins

def index_nullable(nullable, index: int):
    if nullable is not None:
	    return nullable[index]
