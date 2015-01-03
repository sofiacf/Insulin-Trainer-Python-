# Date Stuff

# One hour = 3600 seconds
# One day = 3600 * 24 seconds (=86400 seconds)
# One week = 3600* 24 * 7 seconds (= 604800 seconds)

# if month == 1, 3, 5, 7, 8, 10, or 12:
# 	one month = 3600 * 24 * 31 seconds (= 2678400 seconds)
# elif month == 4, 6, 9, or 11:
# 	one month = 3600 * 24 * 30 seconds (= 2592000 seconds)
# elif month == 2:
# 	if (year - 2000) % 4 == 0:
# 		one month = 3600 * 24 * 29
# 	else:
# 		one month = 3600 * 24 * 28

# compute everything as seconds after January 1, 2000
from datetime import datetime
print(datetime.now())