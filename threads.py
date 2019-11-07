import threading
import time
import datetime

def loop_report_time():
    while True:
        print(str(datetime.datetime.now()))
        time.sleep(1)

thread = threading.Thread(target=loop_report_time)
thread.start()
