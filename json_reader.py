import functions

if functions.db_needs_update():
    print('Updating DB...')
    functions.insert_block()
    if function.insert_block():
        print('DB updated')
    else:
        print('Problem with DB update')
else:
    print('DB is up to date')
    exit()
