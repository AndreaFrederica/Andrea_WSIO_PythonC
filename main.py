import config
from module import log
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
    log.info('catched singal: %d' % signum)
    sys.exit()
 
@atexit.register
def atexit_fun():
    log.info('i am exit, stack track:')
 
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)


def scheduleRunner():
    global flag_exit
    while not flag_exit:
        schedule.run_pending()
        time.sleep(1)


async def main():
    async with websockets.connect(server) as websocket:
        context.context = websocket
        while True:
            command = await websocket.recv()
            log.info(command)
            await register.taskRoute(command)


if(__name__ == "__main__"):
    signal.signal(signal.SIGTERM, term_sig_handler)
    signal.signal(signal.SIGINT, term_sig_handler)
    while True:
        try:
            log.info("Start the scheduleRunnerThread")
            flag_exit = False
            scheduleRunnerThread = Thread(target=scheduleRunner)
            scheduleRunnerThread.start()
            log.info("Try to Connect the MinecraftServer")
            loop = asyncio.new_event_loop()
            loop.run_until_complete(main())
        except:
            loop.close()
            log.error("MainFunc ERROR")
            log.info("Stop the scheduleRunnerThread")
            flag_exit = True
            log.info(f"Wait {config.error_wait} Sec.")
            time.sleep(config.error_wait)

