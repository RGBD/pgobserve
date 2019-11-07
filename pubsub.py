import pgpubsub
import time
import pdb

pubsub = pgpubsub.connect(user='oleg', database='oleg')

pubsub.listen('channel1')

while True:
    event = pubsub.get_event()
    if event:
        print(event.payload)
    time.sleep(1)
