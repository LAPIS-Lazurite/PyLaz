# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

from PyLaz.PyLaz import *
import signal

global cont
def receive_signal(signum,stack):
    global cont
    print("SIGINT")
    cont = False

def test_success():
    assert True


cont = True

signal.signal(signal.SIGINT,receive_signal)

lazurite = PyLaz()

# lazurite.begin test
lazurite.init()

# address type scan
for atype in range(0,1):
    lazurite.begin(36,0xabcd,100,20)
    lazurite.rxEnable()
    lazurite.setAddrType(atype)
    atype = lazurite.getAddrType()
    payload = "AddressType=%d"%atype
    print(payload)
    lazurite.send(0xabcd,0x5f59,payload)
    time.sleep(3)
    data = lazurite.read()
    print(data)
    lazurite.close()

lazurite.remove()
