import sqlite3

connection = sqlite3.connect('instance/movies.db')
cursor = connection.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS movie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        year INTEGER NOT NULL,
        awards INTEGER NOT NULL,
        genre TEXT
    );
''')


movies = [
    ('Black Panther: Wakanda Forever', 2022, 1, 'Action'),
    ('Everything Everywhere All at Once', 2022, 7, 'Sci-Fi'),
    ('Avatar: The Way of Water', 2022, 1, 'Fantasy'),
    ('Dune', 2021, 6, 'Sci-Fi'),
    ('No Time to Die', 2021, 1, 'Action')
]


cursor.executemany('INSERT INTO movie (name, year, awards, genre) VALUES (?, ?, ?, ?);', movies)
connection.commit()
connection.close()

print("Database created successfully.")
