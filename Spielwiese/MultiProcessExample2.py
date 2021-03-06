'''
Created on 18 Jan 2017

@author: rudnikp
'''


from General.ErrorInCode import ErrorInCode
from datetime import datetime, timedelta    
from threading import current_thread   
from General.RunTimeController import RunTimeController
from Power.General.DatabasePreProcessingFunctions import _getSourceIDDemandActuals
from General.CustomThread import CustomThread        
from General.DBConnector import getValuesFromTable, insertCheckedValuesIntoTable, getColumnNames, runQuery
from General.Databases import getDatabase, SYNCED, UNSYNCED
#from General.DateConverter import formatDateTimeInLocalTimeToUTC,formatDateTimeInLocalTimeToUTCv2
from General.DateConverter import convertTimeZone
import xml.sax as sax
import sys
import pytz
import copy
import os


#from apscheduler.scheduler import Scheduler, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import  EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
import logging
import crontab
import threading
import concurrent.futures

from os import getpid
from multiprocessing import Process

from DownloaderAndImporter.Importer.EntsoeEUImporter2 import startImportEntsoeEU_Demand
from DownloaderAndImporter.Importer.SeffalikImporter_v2 import startImportSeffaflik
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import threading

def run_process_1(x):
    startImportEntsoeEU_Demand()
    print(getpid())
    
def run_process_2(x):
    startImportSeffaflik()
    print(getpid())

def run_process_3(x):
    print(getpid())


def run_processes():

    print ("starting p1")
    print ("starting p2")  
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:  
        f1 = executor.submit(run_process_1, 0)
        f2 = executor.submit(run_process_2, 1)
        print (f1.result())
        print (f2.result())



def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')

def run_processes_through_apscheduler():
    #config = {'apscheduler.misfire_grace_time': 45}
    #add listener to scheduler
    #sched.add_listener(my_listener, EVENT_JOB_ERROR)

    try:
        executors = {'default': ThreadPoolExecutor(20),'processpool': ProcessPoolExecutor(5)}
        #executors = {'default': ProcessPoolExecutor(2)}
        sched = BackgroundScheduler(executors=executors)
        sched.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        #sched.add_job(run_processes, trigger='cron', hour='14', minute='06')
        sched.add_job(run_processes)
        sched.start()
        ################# SPOT PRICE MODEL #######################
        ###### DE/AT #####
        #regular forecasts
        #sched.add_cron_job(run_processes,  hour='12', minute = '22') 
        
        print "Import Scheduler is running"
        
        input("Press enter to exit.")
        #print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        sched.shutdown()
    
    except Exception as exc:
        print "ERROR: " + str(exc.args)    



def run_processes_through_timer():
    run_at = datetime.now() + timedelta(minutes=1)
    delay = (run_at - datetime.now()).total_seconds()
    threading.Timer(delay, run_processes).start()
    print ("launched timer event in {s} second(s)".format(s=delay))


if __name__ == '__main__':
    #run_processes()
    run_processes_through_apscheduler()
    #config = {'apscheduler.misfire_grace_time': 45}
    #sched = Scheduler(config)
    #sched.start()
    #sched.print_jobs()
    
    
    
    
    
   

