from Magikarp_wdong20_hgan20_sging20_rzheng21.app.database import Database
from database import Database

db = Database("database.db")

print(db.fetch_game("0", "passnplay"))