import pandas as pd
import urllib
from collections import Counter
import psycopg2
import json
import sql_connection
import datetime

def url_connection1(first_url):
    json_data = ''
    url_pd = ''

    # First connect to url to get latest block through JSON api
    with urllib.request.urlopen(first_url) as url:
        json_data = json.loads(url.read().decode())

    # Now we can check latest block index. Latest block index will help us get the previous already accomplished block
    block_index = json_data['block_index']
    prev_block_index = block_index - 1

    return prev_block_index

def url_connection2(second_url):

    # With previous block index we can get the previous block through JSON api
    with urllib.request.urlopen(second_url) as url1:
        url_pd = json.loads(url1.read().decode())

    return url_pd


# function that check if there is already (latest - 1) hash in DB. We take previous block because latest block is still
# processing.
def db_needs_update():

    # exec first func
    prev_block_index = url_connection1("https://blockchain.info/latestblock")

    #exec second func
    url_pd = url_connection2(f'https://blockchain.info/rawblock/{prev_block_index}')

    hash_no = url_pd['hash']

    # Create two variables out of the block so we can use it in the whole function
    db_update = False
    conn = None

    # Create error exception catcher
    try:

        # connect to the PostgreSQL database
        conn = sql_connection.conn

        # create a new cursor
        cur = conn.cursor()

        # execute the SELECT statement to check if our hash_no is already in database
        select = 'SELECT * FROM btc WHERE hash_no = %s'
        cur.execute(select, (hash_no,))

        # Main Function Duty - Check if record in DB are the same as previous block hash_no if not then we can update DB
        record = cur.fetchall()
        if not record:
            db_update = True
        else:
            db_update = False
        cur.close()

        # This will throw any exceptions during the connection to the DB
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

        # Final condition if connection to the database is not closed and db_update is False then we close connection
        # and exit
    finally:
        if conn is not None and db_update == False:
            conn.close()
            return db_update
        else:
            return db_update



# Function that insert new block info to our pgsql db
def insert_block():

    # First connect to url to get latest block through JSON api
    with urllib.request.urlopen("https://blockchain.info/latestblock") as url:
        json_data = json.loads(url.read().decode())

    block_index = json_data['block_index']
    prev_block_index = block_index - 1

    with urllib.request.urlopen(f'https://blockchain.info/rawblock/{prev_block_index}') as url1:
        url_pd = json.loads(url1.read().decode())

    hash_no = url_pd['hash']
    ver = url_pd['ver']
    prev_block = url_pd['prev_block']
    next_block = url_pd['next_block']
    mrkl_root = url_pd['mrkl_root']
    time = url_pd['time']
    bits = url_pd['bits']
    fee = url_pd['fee']
    nonce = url_pd['nonce']
    n_tx = url_pd['n_tx']
    size = url_pd['size']
    block_index = url_pd['block_index']
    main_chain = url_pd['main_chain']
    height = url_pd['height']
    tx_indexes = url_pd['tx']
    tx_count = 0
    for values in url_pd['tx']:
        tx_count += 1
    timestamp = datetime.datetime.fromtimestamp(time)
    date_time = (timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    try:
        # insert a new values into the btc table
        sql = """INSERT INTO btc(
        hash_no, 
        ver, 
        prev_block, 
        next_block, 
        mrkl_root, 
        time,
        bits, 
        fee, 
        nonce, 
        n_tx, 
        size, 
        block_index,
        main_chain, 
        height, 
        tx_count,
        date_time
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s); """

        conn = None
        # try:
        # connect to the PostgreSQL database
        conn = sql_connection.conn
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (hash_no, ver, prev_block, next_block, mrkl_root, time, bits, fee, nonce, n_tx, size,
                          block_index, main_chain, height, tx_count, date_time))
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
        else:
            pass

        return True
