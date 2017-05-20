import sys
import threading
import time
from datetime import date, timedelta

from Editing.InferenceWriter import write_inferences
from InputValidation import *
from Scraping.ScrapingEngine import ScrapingEngine


def setupScrapeBeginDate(*args):
    daysParamString = "--days"

    global scrapeBeginDate

    argsList = list(*args)

    if (daysParamString in argsList):
        i = argsList.index(daysParamString)
        if (len(argsList) > i + 1) and isValidInteger(argsList[i + 1]):
            scrapeBeginDate = date.today() - timedelta(int(argsList[1]))
            return True
        else:
            print("Invalid argument")
            return False

    # No date parameter, continue
    else:
        scrapeBeginDate = yesterday
        return True


def autorun(*args):
    global currentTask
    global scrapeBeginDate

    currentTask = threading.Thread(target=loopTask, args=(killPill, *args))
    currentTask.setDaemon(True)
    currentTask.start()


def stop(*args):
    global currentTask

    if currentTask is None:
        print("Nothing to interrupt")
        return

    killPill.set()
    currentTask.join()
    currentTask = None
    killPill.clear()


def hello(*args):
    print("Hello, how may I help you ?")


def hi(*args):
    hello(*args)


def thanks(*args):
    if len(args) == 1 and args[0] == "--spanish":
        print("De nada !")
    else:
        print("You're welcome !")


def scrape(*args):
    if not setupScrapeBeginDate(args):
        return False

    else:
        se.run(scrapeBeginDate.strftime(TIME_FORMAT))

    return True


def clean(*args):
    se.clear()


def loopTask(stopEvent, *args):
    print("Starting up the daemon")
    while not stopEvent.wait(1):
        waitingTime = 0
        print("Scraping is about to take place")

        if stopEvent.wait(3):
            break

        if not scrape(*args):
            break

        print("Inference is about to take place")

        if stopEvent.wait(3):
            break

        infer(*args)

        print("Going for a coffee break, see you in 10 minutes. (^_^)o自")

        while not stopEvent.wait(1) and waitingTime < 600:
            waitingTime = waitingTime + 1

        clean()

    print("Daemon has stopped")


def dummyTask(stopEvent):
    i = 0
    while not stopEvent.wait(1):
        print(i)
        i = i + 1
        time.sleep(1)


def infer(*args):
    if not se.isReady():
        print("Please run wiki scraping first")
        return

    write_inferences(se.getResultSet())


def shutdown(*args):
    global currentTask
    print("Shutting down..")

    if currentTask is not None and currentTask.is_alive():
        stop()

    sys.exit(0)


def die(*args):
    print("\(ﾟДﾟ)/  ¬")

    if currentTask is not None and currentTask.is_alive():
        stop()

    print("-(x_x)-")
    time.sleep(1)
    sys.exit(0)


GREET = 'InferenceBot is at your service'
PROMPT = 'InferenceBot > '
TIME_BEGIN = "2000-01-01T00:00:00Z"
TIME_FORMAT = "%Y-%m-%dT00:00:00Z"
yesterday = date.today() - timedelta(1)
scrapeBeginDate = yesterday
currentTask = None
killPill = threading.Event()
command_list = [hello, hi, thanks, scrape, infer, autorun, stop, shutdown, die]
commands = {f.__name__: f for f in command_list}

se = ScrapingEngine()


def mainCLI():
    print(GREET)

    while True:
        command, *args = input(PROMPT).split(" ")
        command = command.lower()

        if command in commands:
            commands[command](*args)
        else:
            print("Command not known")


if __name__ == '__main__':
    mainCLI()
    # se.run()
    # write_inferences(se.getResultSet())
