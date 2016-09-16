from PyLaz.PyLaz import *
import signal
import os
import time

global cont
def receive_signal(signum,stack):
    global cont
    print("SIGINT")
    cont = False

cont = True

signal.signal(signal.SIGINT,receive_signal)

lazurite = PyLaz()

result = lazurite.init()

result = lazurite.begin(36,0xabcd,100,20)

while cont:
    result = lazurite.send(0xabcd,0x5fba,"hello")
    print (result)
    time.sleep(1)


result = lazurite.close()

result = lazurite.remove()


