from queue import Queue
from time import sleep
from .models import ThreadingStatus
from .sms import SMS
from src import db, init_app
import os
QueueList = dict()

app = init_app(os.getenv('APP_ENV'))

def sendSms(name: str, body: str, account_id: int, account_type: str, q: Queue):

    with app.app_context():
        
        sms = SMS(account_id=account_id, type=account_type)
        if sms.errors['error']:
            print(sms.errors['reason'])
            return False
        
        while not q.empty():
            record = q.get()
            q.task_done()
            success = 0
            failed = 0
            if sms.client.send(number=record, body=body):
                success = 1
            else:
                failed = 1
            if name in QueueList:
                QueueList[name]['current_process'] += 1
                QueueList[name]['success'] += success
                QueueList[name]['failed'] += failed
            sleep(1)

        print("Thread {} Completed !!!".format(name))
        if name in QueueList:
            thread = ThreadingStatus.query.filter(ThreadingStatus.name == name).first()
            if thread is not None:
                thread.is_active = False
                thread.completed = True
                thread.success_count = QueueList[name]['success']
                thread.failed_count = QueueList[name]['failed']
                db.session.commit()
            del QueueList[name]