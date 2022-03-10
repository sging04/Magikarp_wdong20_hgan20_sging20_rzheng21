import sqlite3

class Database:
    def __init__(self, db_file: str):
        self.db = sqlite3.connect(db_file)
        self.cur = self.db.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
              id INTEGER PRIMARY KEY,
              username TEXT,
              password TEXT)""")
        
        # TODO: Create database for saved games

        self.db.commit()


    def close(self):
        self.db.close()


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


    def register_user(self, username: str, password: str) -> bool:
        """
        Tries to add the given username and password into the database.
        Returns False if the user already exists, True if it successfully added the user.
        """
        self.cur.execute("SELECT * FROM users WHERE LOWER(username) = LOWER(?)", (username,))
        row = self.cur.fetchone()

        if row is not None:
            return False

        self.cur.execute("""INSERT INTO users(username,password) VALUES(?, ?)""",(username,password))
        self.db.commit()
        return True


    def fetch_username(self, user_id: int) -> str:
        """
        Returns the username of the user with the given id.
        """
        self.cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        username = index_nullable(self.cur.fetchone(), 0)

        return username


def index_nullable(nullable, index: int):
    if nullable is not None:
	    return nullable[index]
