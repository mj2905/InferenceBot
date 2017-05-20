import sys
import threading
import time

from Editing.InferenceWriter import write_inferences
from Scraping.ScrapingEngine import ScrapingEngine


def main():
    se.run()
    write_inferences(se.getResultSet())


def autorun(*args):
    global currentTask
    currentTask = threading.Thread(target=loopTask, args=(killPill,))
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
    se.run()


def clean(*args):
    se.clear()


def loopTask(stopEvent):
    print("Starting up the daemon")
    while not stopEvent.wait(1):
        waitingTime = 0
        print("Scraping is about to take place")

        if stopEvent.wait(3):
            break

        scrape()

        print("Inference is about to take place")

        if stopEvent.wait(3):
            break

        infer()

        print("Going for a coffee break, see you in 10 minutes")

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


def mainTask(stopEvent):
    while not stopEvent.wait(1):
        print("Starting up")
        se.run()
        write_inferences(se.getResultSet())
        print("Coffee break, see you in 10 minutes.")
        time.sleep(60 * 10)

    print("Shutting down")


def infer():
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
    print("\(ﾟДﾟ)/")

    if currentTask is not None and currentTask.is_alive():
        stop()

    print("(x_x)")
    time.sleep(1)
    sys.exit(0)


GREET = 'InferenceBot is at your service'
PROMPT = 'InferenceBot > '
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
    main()
