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

result = lazurite.open()
result = lazurite.begin(36,0xabcd,100,20)

result = lazurite.rxEnable()

while cont:
    result = lazurite.available()
    if result > 0:
        print(lazurite.read())
    
    time.sleep(0.01)


result = lazurite.rxDisable()
result = lazurite.close()

print("end")
