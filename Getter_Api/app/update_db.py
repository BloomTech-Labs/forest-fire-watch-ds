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

# Import data
df = pd.read_csv('confirmed_fires_2014_456.csv')

# Send data to db
print('cleaning data')
dirty_rows = df.values

# Clean up rows
rows = []

for row in dirty_rows:
    rows.append(tuple(row))

print('adding data to DB')
# Loop over the array to write rows in the DB
for row in rows:
    insert = """
    INSERT INTO confirmed_fires
    (modis_id, latitude, longitude, brightness, scan, track,
     satellite, confidence, version, bright_t31, frp,
     daynight, month, week, doy, year,
     fire)
    VALUES 
    """ + str(row) + ';'
    
    pg_curs.execute(insert)

# Save and finish session
pg_curs.close()
pg_conn.commit()

print('all done!')
