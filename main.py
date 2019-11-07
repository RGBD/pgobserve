from pgnotify import await_pg_notifications
import datetime

for notification in await_pg_notifications('postgresql:///oleg', ['channel1']):
    print("{}: {}".format(str(datetime.datetime.now()), notification.payload))
