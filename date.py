import datetime

today = datetime.date.today()
today = today + datetime.timedelta(1)
print str(today).replace('-', '')
