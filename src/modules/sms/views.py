from . import sms
from flask import render_template, redirect, url_for, flash, jsonify
from src.worker import sendSms, QueueList
from queue import Queue
from threading import Thread
import threading
from src.models import Contacts
from random import randrange

@sms.get('/current_process')
def currentprocess():
    for t in threading.enumerate():
        if t.name in QueueList:
            print(t.name)
    return "oke"

@sms.get('/thread/<string:name>')
def getthreadprocess(name):
    if name in QueueList:
        return jsonify(QueueList[name])

@sms.get('/add_process')
def addprocess():
    getAll = Contacts.query.all()
    q = Queue(maxsize=len(getAll))
    q.qsize()
    for data in getAll:
        q.put(data.phonenumber)
    thread_name = 'SENDSMS' + str(randrange(00000,99999))
    QueueList[thread_name] = {
        'is_active' : True,
        'completed' : False,
        'thread_name' : thread_name,
        'size' : len(getAll),
        'current_process' : 0
    }
    worker = Thread(target=sendSms, args=(thread_name, q))
    worker.daemon = True
    worker.name = thread_name
    worker.start()
    return thread_name