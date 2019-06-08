import functions
from functions import check_market
from functions import check_real

# CASE 1
# SQL database populate with basic data
# if functions.insert_block(10,0):
#     print('DB updated')
# else:
#     print('Problem with DB update')

# CASE 2
#  run only one time per 24 hour. It will populate the trade btc data every 24 hours
# check_market()

# CASE 3
# it gains real time data about unspent transactions etc. It has for loop that iterates every 60 seconds. Argument is number of iterations
# check_real(numberofiterations)
