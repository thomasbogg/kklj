import sqlite3

properties = [

    ## QUINTA DA BARRACUDA ##
    {'name': 'Quinta da Barracuda - A02',
    'bedrooms': 1,
    'owner': 'Nuno Pinto',
    'email': 'nunoanca@gmail.com'},

    {'name': 'Quinta da Barracuda - A03',
    'bedrooms': 1,
    'owner': 'Richard Day',
    'email': 'red17704@aol.com'},

    {'name': 'Quinta da Barracuda - A12',
    'bedrooms': 1,
    'owner': 'Karen Holtham',
    'email': 'kholtham@icloud.com'},

    {'name': 'Quinta da Barracuda - A13',
    'bedrooms': 1,
    'owner': 'Janice Daly',
    'email': 'janicedaly85@gmail.com'},

    {'name': 'Quinta da Barracuda - A15',
    'bedrooms': 1,
    'owner': 'Miguel Marques',
    'email': ' '},

    {'name': 'Quinta da Barracuda - A26',
    'bedrooms': 1,
    'owner': 'Olivier Lauraux',
    'email': 'olivier_lauraux@hotmail.com'},

    {'name': 'Quinta da Barracuda - B02',
    'bedrooms': 1,
    'owner': 'Maeve Costello',
    'email': 'costello.mm@gmail.com'},

    {'name': 'Quinta da Barracuda - B04',
    'bedrooms': 1,
    'owner': 'Catarina Amaral',
    'email': 'catarina.s.amaral@gmail.com'},

    {'name': 'Quinta da Barracuda - B05',
    'bedrooms': 1,
    'owner': 'Ines Filipa Carvalho',
    'email': 'ines.carvalho@siemens.com'},

    {'name': 'Quinta da Barracuda - B11',
    'bedrooms': 1,
    'owner': 'Isabelle Costa Oliveira',
    'email': 'isabelleco@me.com'},

    {'name': 'Quinta da Barracuda - B16',
    'bedrooms': 1,
    'owner': 'Evelyn Daly',
    'email': 'evelyn.daly@hotmail.com'},

    {'name': 'Quinta da Barracuda - B21',
    'bedrooms': 1,
    'owner': 'Mirelle Bianchetti',
    'email': 'mirelleluiza@gmail.com'},

    {'name': 'Quinta da Barracuda - B22',
    'bedrooms': 1,
    'owner': 'Maria Douglas',
    'email': 'maria@algarvebeachapartments.com'},

    {'name': 'Quinta da Barracuda - B24',
    'bedrooms': 1,
    'owner': 'Evelyn Malone',
    'email': 'evelyn.malone21@gmail.com'},

    {'name': 'Quinta da Barracuda - B25',
    'bedrooms': 1,
    'owner': 'Tommy Whelan',
    'email': 'twelectrical56@hotmail.com'},

    {'name': 'Quinta da Barracuda - B26',
    'bedrooms': 1,
    'owner': 'David Pais',
    'email': 'davidudate@gmail.com'},

    {'name': 'Quinta da Barracuda - B31',
    'bedrooms': 1,
    'owner': 'Michael Jordan',
    'email': 'michaeljbm@gmail.com'},

    {'name': 'Quinta da Barracuda - C01',
    'bedrooms': 1,
    'owner': 'Ines Filipa Carvalho',
    'email': 'ines.carvalho@siemens.com'},

    {'name': 'Quinta da Barracuda - C12',
    'bedrooms': 2,
    'owner': 'Maria Marta Correia',
    'email': 'maria.ratvajova@outlook.com'},

    {'name': 'Quinta da Barracuda - C14',
    'bedrooms': 1,
    'owner': 'Octavio',
    'email': 'octavio.zink@gmail.com'},

    {'name': 'Quinta da Barracuda - C31',
    'bedrooms': 1,
    'owner': 'Anne Burnett',
    'email': 'annehols@yahoo.co.uk'},

    {'name': 'Quinta da Barracuda - C33',
    'bedrooms': 3,
    'owner': 'Mieke Reece',
    'email': 'mieke.reece@gmail.com'},

    {'name': 'Quinta da Barracuda - C34',
    'bedrooms': 1,
    'owner': 'Vipin Seth',
    'email': 'vipins8@aol.com'},

    {'name': 'Quinta da Barracuda - D02',
    'bedrooms': 1,
    'owner': 'Salil Shah',
    'email': 'quintadabarracuda@gmail.com'},

    {'name': 'Quinta da Barracuda - D03',
    'bedrooms': 1,
    'owner': 'Ema Furtado',
    'email': 'ema.furtado@engie.com'},

    {'name': 'Quinta da Barracuda - D13',
    'bedrooms': 1,
    'owner': 'Chris Keogh',
    'email': 'cckeogh4@gmail.com'},

    {'name': 'Quinta da Barracuda - D15',
    'bedrooms': 1,
    'owner': 'Rosie Ambron',
    'email': 'rosieambron@gmail.com'},

    {'name': 'Quinta da Barracuda - D22',
    'bedrooms': 1,
    'owner': 'Maria Ratvajova',
    'email': 'maria.ratvajova@outlook.com'},

    {'name': 'Quinta da Barracuda - D23',
    'bedrooms': 1,
    'owner': 'Thomas Carey',
    'email': 't.carey140@gmail.com'},

    {'name': 'Quinta da Barracuda - D26',
    'bedrooms': 1,
    'owner': 'Gerry Neeson',
    'email': 'algarveapartments@thegeminigroup.co.uk'},

    {'name': 'Quinta da Barracuda - D31',
    'bedrooms': 1,
    'owner': 'Andre Marques',
    'email': 'andre.abreu.marques@sapo.pt'},


    ## CLUBE DO MONACO ##
    {'name': 'Clube do Monaco - 2',
    'bedrooms': 2,
    'owner': 'Somendra Khosla',
    'email': 'somendrakhosla@hotmail.com'},

    {'name': 'Clube do Monaco - 8',
    'bedrooms': 2,
    'owner': 'Somendra Khosla',
    'email': 'somendrakhosla@hotmail.com'},

    {'name': 'Clube do Monaco - AA',
    'bedrooms': 1,
    'owner': 'Somendra Khosla',
    'email': 'somendrakhosla@hotmail.com'},

    {'name': 'Clube do Monaco - AE',
    'bedrooms': 2,
    'owner': 'Somendra Khosla',
    'email': 'somendrakhosla@hotmail.com'},


    ## CERRO MAR ##
    {'name': 'Cerro Mar - 201',
    'bedrooms': 1,
    'owner': 'Patrick Seeber',
    'email': 'seeber555@btinternet.com'},

    {'name': 'Cerro Mar - 203',
    'bedrooms': 1,
    'owner': 'Patrick Seeber',
    'email': 'seeber555@btinternet.com'},

    {'name': 'Cerro Mar - 305',
    'bedrooms': 1,
    'owner': 'Catarina Amaral',
    'email': 'catarina.s.amaral@gmail.com'},

    {'name': 'Cerro Mar - 307',
    'bedrooms': 1,
    'owner': 'Katarina Glamoclija',
    'email': 'kaca.glam@gmail.com'},


    ## PARQUE DA CORCOVADA ##
    {'name': 'Parque da Corcovada - 43 G',
    'bedrooms': 1,
    'owner': 'Stephen O\'Brien',
    'email': 'obrien.stephen@gmail.com'},

    {'name': 'Parque da Corcovada - 43 2G',
    'bedrooms': 1,
    'owner': 'Stephen O\'Brien',
    'email': 'obrien.stephen@gmail.com'}

]

# establish connection to database and
conn = sqlite3.connect('KKLJ.db')
cur = conn.cursor()

# create tables
cur.executescript("""

CREATE TABLE IF NOT EXISTS Properties (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name        TEXT UNIQUE,
    bedrooms    INTEGER,
    owner       TEXT,
    email       TEXT
);

CREATE TABLE IF NOT EXISTS Guests (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name        TEXT,
    email       TEXT
);

CREATE TABLE IF NOT EXISTS Stay (
    id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    prop_id     INTEGER,
    guest_id    INTEGER,
    arrival     TEXT,
    departure   TEXT,
    party_size  TEXT,
    security    TEXT,
    owner       TEXT
);

CREATE TABLE IF NOT EXISTS Transport (
    stay_id     INTEGER UNIQUE,
    transport   TEXT,
    carhire    TEXT,
    eta         TEXT,
    f_in_no     TEXT,
    f_in_time   TEXT,
    f_out_no    TEXT,
    f_out_time  TEXT
);

CREATE TABLE IF NOT EXISTS Charges_Owner (
    stay_id     INTEGER,
    prop_id     INTEGER,
    clean       TEXT,
    meetgreet   TEXT,
    custom      TEXT,
    total       TEXT
);

CREATE TABLE IF NOT EXISTS Charges_Guest (
    stay_id         INTEGER,
    meet_greet      TEXT,
    transfer        TEXT,
    pack            TEXT,
    cot_chair       TEXT,
    custom          TEXT,
    total           TEXT
)
""")

for dict in properties:

    cur.execute('''
        INSERT INTO
        Properties (name, bedrooms, owner, email)
        VALUES (?,?,?,?)''',
        (dict['name'], dict['bedrooms'], dict['owner'], dict['email']))


cur.execute('SELECT name FROM Properties')
props = cur.fetchall()

print(props)

conn.commit()
conn.close()
