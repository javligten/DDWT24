import sqlite3

connection = sqlite3.connect('movies.db')
cursor = connection.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS movie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        year INTEGER NOT NULL,
        awards INTEGER NOT NULL
    );
''')


movies = [
    ('Black Panther: Wakanda Forever', 2022, 1),
    ('Everything Everywhere All at Once', 2022, 7),
    ('Avatar: The Way of Water', 2022, 1),
    ('Dune', 2021, 6),
    ('No Time to Die', 2021, 1)
]


cursor.executemany('INSERT INTO movie (name, year, awards) VALUES (?, ?, ?);', movies)
connection.commit()
connection.close()

print("Database created successfully.")
