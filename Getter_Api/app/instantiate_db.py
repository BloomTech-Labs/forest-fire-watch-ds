# Sqlite3 imports
import psycopg2

# DS Logic imports
import pandas as pd

# Credentials
dbname = 'iagqhysc'
user = 'iagqhysc'
password = '' # Don't commit this!
host = 'salt.db.elephantsql.com'

# Establish connection
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                       password=password, host=host)

# Instantiate cursor
pg_curs = pg_conn.cursor()

# Create table statement
create_training_table = """
CREATE TABLE training (
id SERIAL PRIMARY KEY,
latitude FLOAT,
longitude FLOAT,
brightness FLOAT,
scan FLOAT,
track FLOAT,
satellite VARCHAR(7),
confidence INT,
version VARCHAR(7),
bright_t31 FLOAT,
frp FLOAT,
daynight VARCHAR(7),
month INT,
week INT,
temperature FLOAT,
humidity FLOAT,
windspeed FLOAT,
winddirection FLOAT,
timestamp VARCHAR(50),
fire INT
);
"""

# Drop table statement
drop_training_table = """
DROP TABLE training;
"""

# Execute table creation
print('dropping old db')
pg_curs.execute(drop_training_table)
print('creating db')
pg_curs.execute(create_training_table)

# Save and finish session
pg_curs.close()
pg_conn.commit()

print('all done!')
