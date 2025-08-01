import libsql

conn = libsql.connect("vector.db")

conn.execute(
    "CREATE TABLE movies (title TEXT, year INT, embedding F32_BLOB(3))")
conn.execute("CREATE INDEX movies_idx ON movies (libsql_vector_idx(embedding))")

conn.execute("""
  INSERT INTO movies (title, year, embedding) VALUES
    ('Napoleon', 2023, vector('[1,2,3]')),
    ('Black Hawk Down', 2001, vector('[10,11,12]')),
    ('Gladiator', 2000, vector('[7,8,9]')),
    ('Blade Runner', 1982, vector('[4,5,6]'));
""")

cur = conn.execute("""
  SELECT title, year
  FROM vector_top_k('movies_idx', '[4,5,6]', 3)
  JOIN movies ON movies.rowid = id
""")

print(cur.fetchall())
