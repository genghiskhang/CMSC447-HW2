import sqlite3

conn = sqlite3.connect("hw2.db")
cur = conn.cursor()

# Table
cur.executescript("""
                DROP TABLE IF EXISTS users;
                CREATE TABLE users (
                  id TEXT NOT NULL PRIMARY KEY,
                  name TEXT DEFAULT NULL,
                  points INTEGER DEFAULT 0
                );
                CREATE INDEX id ON users(id);
                """)

# Test Data
cur.executescript("""
                DELETE FROM users;
                INSERT INTO users (
                  id,
                  name,
                  points
                )
                VALUES
                  ('387', 'Steve Smith', 80),
                  ('122', 'Jian Wong', 92),
                  ('213', 'Chris Peterson', 91),
                  ('524', 'Sai Patel', 94),
                  ('425', 'Andrew Whitebeard', 99),
                  ('626', 'Lynn Roberts', 90),
                  ('287', 'Robert Sanders', 75);
                """)