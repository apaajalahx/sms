from queue import Queue
from threading import Event
from time import sleep
from .models import ThreadingStatus


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
        from src import db, init_app
        import os
        app = init_app(os.getenv('APP_ENV'))
        with app.app_context():
            thread = ThreadingStatus.query.filter(ThreadingStatus.name == name).first()
            if thread is not None:
                thread.is_active = False
                thread.completed = True
                thread.success_count = QueueList[name]['success']
                thread.failed_count = QueueList[name]['failed']
                db.session.commit()
            del QueueList[name]

thread_event = Event()