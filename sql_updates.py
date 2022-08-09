import sqlite3

conn = sqlite3.connect('KKLJ.db')
cur = conn.cursor()

#update column 'meet_greet' in Charges_Guest to 'meetgreet'
cur.execute('ALTER TABLE Charges_Guest RENAME COLUMN meet_greet TO meetgreet')

conn.commit()
conn.close()
