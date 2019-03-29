import psycopg2

conn = psycopg2.connect(
    database='your_pg_db',
    user='your_pg_user',
    password='your_pg_password',
    host='your_pg_host',
    port='your_pg_port'
    )
