from os import environ
import psycopg2

conn = psycopg2.connect(host='localhost',
                        database=environ['POSTGRES_DB'],
                        user=environ['USERNAME_DB'],
                        password=environ['PASSWORD_DB'])

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Inputs;')
cur.execute('CREATE TABLE Inputs (id serial PRIMARY KEY,'
            'data jsonb NOT NULL);'
            )

conn.commit()

cur.close()
conn.close()