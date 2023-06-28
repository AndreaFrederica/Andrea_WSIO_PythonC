import asyncio
import atexit
import signal
import sys
from threading import Thread
import traceback
import schedule
import websockets
import json
import time

# import apscheduler.schedulers.background as adv_background_schedulers

from module import register
from module import context

flag_exit = False

server = "ws://localhost:23080"



def term_sig_handler(signum, frame):
    global flag_exit
    flag_exit = True
    schedule.run_all()
    print ('catched singal: %d' % signum)
    sys.exit()
 
@atexit.register
def atexit_fun():
    print ('i am exit, stack track:')
 
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)


def scheduleRunner():
    global flag_exit
    while not flag_exit:
        schedule.run_pending()
        time.sleep(1)

scheduleRunnerThread = Thread(target=scheduleRunner)

async def main():
    
    signal.signal(signal.SIGTERM, term_sig_handler)
    signal.signal(signal.SIGINT, term_sig_handler)
    async with websockets.connect(server) as websocket:
        context.context = websocket
        scheduleRunnerThread.start()
        while True:
            command = await websocket.recv()
            print(command)
            await register.taskRoute(command)


asyncio.run(main())
