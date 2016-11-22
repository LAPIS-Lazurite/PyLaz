#Lazurite Python Library "PyLaz"
Lazurite is IoT reference design with 920MHz SubGHz RF. It consists of low power micro controller board and Raspberry Pi based gateway.

[Lazurite](http://www.lapis-semi.com/lazurite-jp) development team supports Python Library for our RF on Raspberry Pi.

# Getting Started
1. install library
  easy install:
    ```
    sudo pip install PyLaz
    sudo pip3 install PyLaz
    ```
  manual install:
    ```
    git clone git://github.com/LAPIS-Lazurite/PyLaz
    cd PyLaz
    python setup.py install
    ```
2. download sample program
  Please git this repository.
  (ex) git clone git://github.com/LAPIS-Lazurite/PyLaz
3. execute sample program
   sample programs are stored in samples folder.
   rxsample.py :  simple version on command line program for receiving.
   txsample.py :  simple version on command line program for transferring.
   gateway.py :   GUI for setting RF parameters and log is displayed on GUI's text feild.

# Description
rxsample.py and txsample.py work on Python 2 and 3
gateway.py works on only Python3.


# Requirement
LazDriver must be worked on Raspberry Pi.

# API
## init()
## begin(ch,panid,rate,pwr)
## send(panid,rxaddr,payload)
## close()
## read()
## rxEnable()
## rxDisable()
## available()
## get_my_address()
## get_addr_type(type)
## set_addr_type(type)
## set_tx_retry(type)
## get_tx_retry(type)

## get_rx_time()
## get_rx_rssi()


