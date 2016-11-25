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

# channel scan
for ch in range(24,61):
    if ch !=32:
        lazurite.begin(ch,0xabcd,100,20)
        assert lazurite.get_ch() == ch,"ch=%d error in begin"%ch
        assert lazurite.get_my_panid() == 0xabcd, "panid error in begin"
        assert lazurite.get_bps() == 100, "rate error in begin"
        assert lazurite.get_pwr() == 20, "pwr error in begin"

for ch in range(24,62):
    lazurite.begin(ch,0xabcd,50,20)
    assert lazurite.get_ch() == ch,"ch error in begin"
    assert lazurite.get_my_panid() == 0xabcd, "panid error in begin"
    assert lazurite.get_bps() == 50, "rate error in begin"
    assert lazurite.get_pwr() == 20, "pwr error in begin"

# rate scan
for rate in [50,100]:
    lazurite.begin(36,0xabcd,rate,20)
    assert lazurite.get_bps() == rate, "rate error in begin"

# pwr scan
for pwr in [1,20]:
    lazurite.begin(36,0xabcd,100,pwr)
    assert lazurite.get_pwr() == pwr, "rate error in begin"

# channel scan in error condition at 100kbps
for ch in [23,32,61]:
    try:
        lazurite.begin(ch,0xabcd,100,20)
    except:
        pass
        continue
    raise Exception("error")
# channel scan in error condition at 50kbps
for ch in [23,62]:
    try:
        lazurite.begin(ch,0xabcd,50,20)
    except:
        pass
        continue
    raise Exception("error")
# rate scan in error condition
for rate in [49,51,99,101]:
    try:
        lazurite.begin(36,0xabcd,rate,20)
    except:
        pass
        continue
    raise Exception("error")

# pwr scan in error condition
for pwr in [0,2,19,21]:
    try:
        lazurite.begin(36,0xabcd,100,pwr)
    except:
        pass
        continue
    raise Exception("error")

# check send mode
smode = lazurite.getSendMode()
print(smode)
assert smode["addr_type"]==6,"init value of addr type error"
assert smode["sense_time"]==20,"init value of sense time error"
assert smode["tx_retry"]==3,"init value of tx_retry error"
assert smode["tx_interval"]==500,"init value of tx_interval error"
assert smode["cca_wait"]==7,"init value of cca_wait error"

# address type scan
for atype in range(0,8):
    lazurite.begin(36,0xabcd,100,20)
    lazurite.rxEnable()
    lazurite.setAddrType(atype)
    lazurite.send(0xabcd,0x5f59,"hello")
    time.sleep(3)
    data = lazurite.read()
    print(data)
    lazurite.close()

lazurite.remove()
