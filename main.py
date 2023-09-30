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

from module import context
from module import minecraftServerWsConnect as mcwsc
from module import goCQWsConnect as cqwsc

context.flag_exit = False

context.main_exit_flag = False


def exit():
    context.flag_exit = True
    context.main_exit_flag = True
    sys.exit()

def term_sig_handler(signum, frame):
    context.flag_exit = True
    log.info('catched singal: %d' % signum)
    sys.exit()

@atexit.register
def atexit_fun():
    log.info('i am exit, stack track:')
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)


def scheduleRunner():
    while not context.flag_exit:
        schedule.run_pending()
        time.sleep(1)




if(__name__ == "__main__"):
    signal.signal(signal.SIGTERM, term_sig_handler)
    signal.signal(signal.SIGINT, term_sig_handler)
    while not context.main_exit_flag:
        try:
            log.info("Start the scheduleRunnerThread")
            context.flag_exit = False
            scheduleRunnerThread = Thread(target=scheduleRunner)
            scheduleRunnerThread.start()
            # log.info("Try to Connect the MinecraftServer")
            scheduleRunnerThread = Thread(target=scheduleRunner)
            scheduleRunnerThread.start()
            tasks = list() #? WorkingList
            tasks += (mcwsc.getWorkList())
            if(config.cqwsc_enable):
                tasks += (cqwsc.getWorkList())
            
            wait_coro = asyncio.wait(tasks)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(wait_coro)
            loop.close()
            
        except Exception as e:
            log.error(e)
            log.error("MainFunc ERROR")
            log.info("Stop the scheduleRunnerThread")
            context.flag_exit = True
            log.info(f"Wait {config.error_wait} Sec.")
            time.sleep(config.error_wait)
