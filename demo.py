from modules.unifoundseat.api import unifoundUser
from datetime import date, datetime,timedelta

user=unifoundUser("222019")
user.dowebLogin()
tomorrow = datetime.now()+timedelta(days=2)
datefrom = datetime(year=tomorrow.year,
                    month=tomorrow.month, day=tomorrow.day, hour=8)
# 8:00 - 13:00
print(user.dowebReseve('7A402-4F-016',datefrom,datefrom+timedelta(hours=5)))
# 13:00 - 18:00
print(user.dowebReseve('7A402-4F-016',datefrom+timedelta(hours=5),datefrom+timedelta(hours=10)))
# 18:00 - 23:00
print(user.dowebReseve('7A402-4F-016',datefrom+timedelta(hours=10),datefrom+timedelta(hours=14)))