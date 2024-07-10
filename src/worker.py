from queue import Queue
from threading import Event
from time import sleep

QueueList = dict()

def sendSms(name, q: Queue):
    while not q.empty():
        record = q.get()
        print("Current Task {}".format(record))
        q.task_done()
        if name in QueueList:
            QueueList[name]['current_process'] += 1
        sleep(1)
    print("Thread {} Completed !!!".format(name))
    if name in QueueList:
        QueueList[name]['is_active'] = False
        QueueList[name]['completed'] = True

thread_event = Event()