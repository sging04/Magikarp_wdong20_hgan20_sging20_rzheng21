from database import Database

def rprint(success: bool, message: str):
    tag = "\033[92m[OK]\033[0m" if success else "\033[91m[FAIL]\033[0m"
    print(f"{tag} {message}")

db = Database(":memory:")

# Register tests
result = db.register_user("hello", "world")
rprint(result == True, "register_user returns True on new user registration")

result = db.register_user("hello", "world")
rprint(result == False, "register_user returns False on duplicate user registration")

result = db.register_user("hello", "man")
rprint(result == False, "register_user returns False on same name different password")

# Fetch user tests
db.register_user("hello2", "test")

result = db.fetch_user("hello", "world")
rprint(result == 1, "fetch_user returns the correct id when given the correct information")

result = db.fetch_user("hello2", "test")
rprint(result == 2, "fetch_user returns the correct id when given the correct information")

result = db.fetch_user("hello2", "bad")
rprint(result is None, "fetch_user returns None when given the incorrect information")

# Fetch username tests
result = db.fetch_username(1)
rprint(result == "hello", "fetch_username returns correct username when given valid id")

result = db.fetch_username(2)
rprint(result == "hello2", "fetch_username returns correct username when given valid id")

result = db.fetch_username(3)
rprint(result is None, "fetch_username returns None when given invalid id")

# Profile picture tests
result = db.set_picture(1, "test")
rprint(result == True, "set_picture returns True when given a valid user id")

result = db.set_picture(10, "test")
rprint(result == False, "set_picture returns False when given an invalid user id")

result = db.fetch_picture(1)
rprint(result == "test", "fetch_picture returns a picture when given a valid user id")

result = db.fetch_picture(2)
rprint(result == "", "fetch_picture returns a default picture when given the user id of a user that hasn't updated their profile picture")

result = db.fetch_picture(10)
rprint(result is None, "fetch_picture returns None when given an invalid user id")

db.close()