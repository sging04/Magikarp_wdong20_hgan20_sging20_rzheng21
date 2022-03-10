from database import Database

def rprint(success: bool, message: str):
    tag = "[OK]" if success else "[FAIL]"
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

db.close()