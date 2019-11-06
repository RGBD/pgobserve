from pgnotify import await_pg_notifications

for notification in await_pg_notifications('postgresql:///oleg', ['channel1']):
    print(notification.channel)
    print(notification.payload)
