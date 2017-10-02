import datetime
import time
now_time = datetime.datetime.now() # Поточна дата
number = int(time.strftime('%W'))
if (number%2 > 0):
  week = '1'
else:
  week = '2'
day = '%d' %now_time.isoweekday()

