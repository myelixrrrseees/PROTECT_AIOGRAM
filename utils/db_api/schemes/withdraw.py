


Withdraw = """CREATE TABLE IF NOT EXISTS Withdraw(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
amount INTEGER,
photo_name TEXT,
photo_id TEXT,
status TEXT
)"""


drop_Withdraw = """DROP TABLE Withdraw"""