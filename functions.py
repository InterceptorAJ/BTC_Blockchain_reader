import urllib
from datetime import datetime
import psycopg2
import json
import sql_connection
import datetime
import urllib.request
from urllib.error import HTTPError
import time


def url_connection1(first_url):
    req = urllib.request.Request(
        url=r"https://blockchain.info/latestblock",
        headers={'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
    try:
        handler = urllib.request.urlopen(req)
    except HTTPError as e:
        content = e.read()
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


def insert_block(no_of_blocks, entry_block):
    global last_block
    latest_block = url_connection1("https://blockchain.info/latestblock")
    last_block = latest_block

    first_block = last_block - no_of_blocks
    arg1 = first_block-entry_block
    arg2 = last_block-entry_block
    print(arg1,arg2)

    try:
        conn = None
        # try:
        # connect to the PostgreSQL database
        conn = sql_connection.conn
        # create a new cursor
        cur = conn.cursor()

        for block in range(arg1, arg2):
            with urllib.request.urlopen(f'https://blockchain.info/rawblock/{block}') as url1:
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
                timestamp = datetime.datetime.fromtimestamp(time)
                date_time = (timestamp.strftime('%Y-%m-%d %H:%M:%S'))

                select = 'SELECT * FROM btc WHERE hash_no = %s'
                # print(cur.execute(select))
                cur.execute(select, (hash_no,))
                record = cur.fetchall()
                # insert a new values into the btc table
                if not record:
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
                                    date_time
                                    ) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """

                    # execute the INSERT statement
                    cur.execute(sql,
                                (hash_no, ver, prev_block, next_block, mrkl_root, time, bits, fee, nonce, n_tx, size,
                                 block_index, main_chain, height, date_time))

                    # commit the changes to the database
                    conn.commit()
                else:
                    pass

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

def check_real(count):
    try:
        conn = None
        # try:
        # connect to the PostgreSQL database
        conn = sql_connection.conn
        # create a new cursor
        cur = conn.cursor()

        for i in range(0,count):
            url1 = urllib.request.urlopen("https://blockchain.info/q/unconfirmedcount")
            url2 = urllib.request.urlopen("https://blockchain.info/q/eta")
            url3 = urllib.request.urlopen("https://blockchain.info/q/getdifficulty")
            url4 = urllib.request.urlopen("https://blockchain.info/q/probability")
            url5 = urllib.request.urlopen("https://blockchain.info/q/hashrate")
            url6 = urllib.request.urlopen("https://blockchain.info/q/hashestowin")
            pending_txs = url1.read().decode('utf-8')
            print(pending_txs)
            eta = url2.read().decode('utf-8')
            print(eta)
            difficulty = url3.read().decode('utf-8')
            print(difficulty)
            probability = url4.read().decode('utf-8')
            print(probability)
            hashrate = url5.read().decode('utf-8')
            print(hashrate)
            hashestowin = url6.read().decode('utf-8')
            print(hashestowin)
            time_txs = datetime.datetime.now().timestamp()
            print(time_txs)
            timestamp = datetime.datetime.fromtimestamp(time_txs)
            print(timestamp)
            date_time = (timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            print(date_time)

            sql = """INSERT INTO btc_real(
                            pending_txs,
                            eta,
                            difficulty,
                            probability,
                            hashrate,
                            hashestowin,
                            time_txs, 
                            date_time
                            ) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s); """

            # execute the INSERT statement
            cur.execute(sql,
                        (pending_txs,
                         eta,
                         difficulty,
                         probability,
                         hashrate,
                         hashestowin,
                         time_txs,
                         date_time))

            # commit the changes to the database
            conn.commit()
            time.sleep(60)

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

def check_market():
    # try:
        conn = None
        # try:
        # connect to the PostgreSQL database
        conn = sql_connection.conn
        # create a new cursor
        cur = conn.cursor()

        for i in range(0, 1):
            url1 = urllib.request.urlopen(f'https://api.blockchain.info/stats')
            url_pd = json.loads(url1.read().decode())

            market_price_usd = url_pd['market_price_usd']
            print(market_price_usd)
            hash_rate = url_pd['hash_rate']
            print(hash_rate)
            total_fees_btc = (url_pd['total_fees_btc']/100000000)
            print(total_fees_btc)
            n_btc_mined = (url_pd['n_btc_mined']/100000000)
            print(n_btc_mined)
            n_tx = url_pd['n_tx']
            print(n_tx)
            n_blocks_mined = url_pd['n_blocks_mined']
            print(n_blocks_mined)
            minutes_between_blocks = url_pd['minutes_between_blocks']
            print(minutes_between_blocks)
            totalbc = (url_pd['totalbc']/100000000)
            print(totalbc)
            n_blocks_total = url_pd['n_blocks_total']
            print(n_blocks_total)
            estimated_transaction_volume_usd = url_pd['estimated_transaction_volume_usd']
            print(estimated_transaction_volume_usd)
            blocks_size = url_pd['blocks_size']
            print(blocks_size)
            miners_revenue_usd = url_pd['miners_revenue_usd']
            print(miners_revenue_usd)
            nextretarget = url_pd['nextretarget']
            print(nextretarget)
            difficulty = url_pd['difficulty']
            print(difficulty)
            estimated_btc_sent = url_pd['estimated_btc_sent']
            print(estimated_btc_sent)
            miners_revenue_btc = url_pd['miners_revenue_btc']
            print(miners_revenue_btc)
            total_btc_sent = url_pd['total_btc_sent']
            print(total_btc_sent)
            trade_volume_btc = url_pd['trade_volume_btc']
            print(trade_volume_btc)
            trade_volume_usd = url_pd['trade_volume_usd']
            print(trade_volume_usd)
            time_stamp = int(url_pd['timestamp']/1000)
            print(time_stamp)
            timestamp = datetime.datetime.fromtimestamp(time_stamp)
            print(timestamp)
            date_time = (timestamp.strftime('%Y-%m-%d %H:%M:%S'))
            print(date_time)

            sql = """INSERT INTO btc_market(
                            market_price_usd,
                            hash_rate,
                            total_fees_btc,
                            n_btc_mined,
                            n_tx,
                            n_blocks_mined,
                            minutes_between_blocks,
                            totalbc,
                            n_blocks_total,
                            estimated_transaction_volume_usd,
                            blocks_size,
                            miners_revenue_usd,
                            nextretarget,
                            difficulty,
                            estimated_btc_sent,
                            miners_revenue_btc,
                            total_btc_sent,
                            trade_volume_btc,
                            trade_volume_usd,
                            time_stamp,
                            date_time
                            )
                            VALUES 
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); """






            # execute the INSERT statement
            cur.execute(sql,
                    (market_price_usd,
                    hash_rate,
                    total_fees_btc,
                    n_btc_mined,
                    n_tx,
                    n_blocks_mined,
                    minutes_between_blocks,
                    totalbc,
                    n_blocks_total,
                    estimated_transaction_volume_usd,
                    blocks_size,
                    miners_revenue_usd,
                    nextretarget,
                    difficulty,
                    estimated_btc_sent,
                    miners_revenue_btc,
                    total_btc_sent,
                    trade_volume_btc,
                    trade_volume_usd,
                    time_stamp,
                    date_time))

            # commit the changes to the database
            conn.commit()
            time.sleep(60)
        # close communication with the database
        cur.close()

    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)

    # finally:
    #     if conn is not None:
    #         conn.close()

        return True
