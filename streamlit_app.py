from collections import namedtuple
import pandas as pd
import streamlit as st
import psycopg2
from sshtunnel import SSHTunnelForwarder


"""
# Witam!

Poniżej znajduję się aktualizowana co 1h informacja o poziomie wypełnienia ankiety.
"""

server = SSHTunnelForwarder(
    'pgsql1.small.pl',
    ssh_username="tessali",
    ssh_password="XLw0UPsp5WT)nTpK65Hc",
    remote_bind_address=('pgsql1.small.pl', 5432)
)


server.start()

#print(server.local_bind_port) 


# Connect to an existing database
conn = psycopg2.connect(host='127.0.0.1', user='p1054_test',
                              password='47QXQ00:F.rMX.952r12E@.LwdIHv2', 
                              dbname='p1054_test', port=server.local_bind_port)


cur = conn.cursor()

# Execute a command: this creates a new table
#cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

# Pass data to fill a query placeholders and let Psycopg perform
# the correct conversion (no more SQL injections!)
#cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

# Query the database and obtain data as Python objects
cur.execute("SELECT * FROM mytable;")
results = cur.fetchall()

# Make the changes to the database persistent
conn.commit()


columns = []

for column in cur.description:
    columns.append(column.name)

# Perform query.
#df = conn.query('SELECT * FROM baeldungauthor;', ttl="10m")


df = pd.DataFrame(results, columns=columns) 

print(df)


cur.close()
conn.close()
server.stop()



#st.dataframe(df)

for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")


#st.dataframe(df, hide_index=True)