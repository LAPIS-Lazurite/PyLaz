from PyLaz.PyLaz import *
import signal
import os

cont = True
def receive_signal(signum,stack):
    cont = False

signal.signal(signal.SIGINT,receive_signal)

lazurite = PyLaz()

result = lazurite.open()

result = lazurite.begin(36,0xabcd,100,20)

while cont:
    result = lazurite.send(0xffff,0xffff,"hello")

result = lazurite.close()

result = lazurite.remove()


