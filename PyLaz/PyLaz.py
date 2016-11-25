import fcntl
import subprocess
import os
from struct import *
import time

class PyLaz:
    IOCTL_CMD=      0x0000
    IOCTL_SET_BEGIN=    IOCTL_CMD+0x11
    IOCTL_SET_RXON=     IOCTL_CMD+0x13
    IOCTL_SET_RXOFF=    IOCTL_CMD+0x15
    IOCTL_SET_CLOSE=            IOCTL_CMD+0x17
    IOCTL_GET_SEND_MODE=    IOCTL_CMD+0x18
    IOCTL_SET_SEND_MODE=    IOCTL_CMD+0x19
    IOCTL_PARAM=        0x1000
    IOCTL_GET_CH=       IOCTL_PARAM+0x02
    IOCTL_SET_CH=       IOCTL_PARAM+0x03
    IOCTL_GET_PWR=      IOCTL_PARAM+0x04
    IOCTL_SET_PWR=      IOCTL_PARAM+0x05
    IOCTL_GET_BPS=      IOCTL_PARAM+0x06
    IOCTL_SET_BPS=      IOCTL_PARAM+0x07
    IOCTL_GET_MY_PANID= IOCTL_PARAM+0x08
    IOCTL_SET_MY_PANID= IOCTL_PARAM+0x09
    IOCTL_GET_TX_PANID= IOCTL_PARAM+0x0a
    IOCTL_SET_TX_PANID= IOCTL_PARAM+0x0b
    IOCTL_GET_MY_ADDR0= IOCTL_PARAM+0x0c
    IOCTL_SET_MY_ADDR0= IOCTL_PARAM+0x0d
    IOCTL_GET_MY_ADDR1= IOCTL_PARAM+0x0e
    IOCTL_SET_MY_ADDR1= IOCTL_PARAM+0x0f
    IOCTL_GET_MY_ADDR2= IOCTL_PARAM+0x10
    IOCTL_SET_MY_ADDR2= IOCTL_PARAM+0x11
    IOCTL_GET_MY_ADDR3= IOCTL_PARAM+0x12
    IOCTL_SET_MY_ADDR3= IOCTL_PARAM+0x13
    IOCTL_GET_TX_ADDR0= IOCTL_PARAM+0x14
    IOCTL_SET_TX_ADDR0= IOCTL_PARAM+0x15
    IOCTL_GET_TX_ADDR1= IOCTL_PARAM+0x16
    IOCTL_SET_TX_ADDR1= IOCTL_PARAM+0x17
    IOCTL_GET_TX_ADDR2= IOCTL_PARAM+0x18
    IOCTL_SET_TX_ADDR2= IOCTL_PARAM+0x19
    IOCTL_GET_TX_ADDR3= IOCTL_PARAM+0x1a
    IOCTL_SET_TX_ADDR3= IOCTL_PARAM+0x1b
    IOCTL_GET_ADDR_TYPE=    IOCTL_PARAM+0x1c
    IOCTL_SET_ADDR_TYPE=    IOCTL_PARAM+0x1d
    IOCTL_GET_ADDR_SIZE=    IOCTL_PARAM+0x1e
    IOCTL_SET_ADDR_SIZE=    IOCTL_PARAM+0x1f
    IOCTL_GET_DRV_MODE= IOCTL_PARAM+0x20
    IOCTL_SET_DRV_MODE= IOCTL_PARAM+0x21
    IOCTL_GET_SENSE_TIME=   IOCTL_PARAM+0x22
    IOCTL_SET_SENSE_TIME=   IOCTL_PARAM+0x23
    IOCTL_GET_TX_RETRY= IOCTL_PARAM+0x24
    IOCTL_SET_TX_RETRY= IOCTL_PARAM+0x25
    IOCTL_GET_TX_INTERVAL=  IOCTL_PARAM+0x26
    IOCTL_SET_TX_INTERVAL=  IOCTL_PARAM+0x27
    IOCTL_GET_CCA_WAIT= IOCTL_PARAM+0x28
    IOCTL_SET_CCA_WAIT= IOCTL_PARAM+0x29
    IOCTL_GET_RX_SEC0=  IOCTL_PARAM+0x2A
    IOCTL_GET_RX_SEC1=  IOCTL_PARAM+0x2C
    IOCTL_GET_RX_NSEC0= IOCTL_PARAM+0x2E
    IOCTL_GET_RX_NSEC1= IOCTL_PARAM+0x30
    IOCTL_GET_RX_RSSI=  IOCTL_PARAM+0x32
    IOCTL_GET_TX_RSSI=  IOCTL_PARAM+0x34

    lzgw = 0
    lzgw_w = 0
    dev="/dev/lzgw"

    def init(self):
        '''
        cmd = "sudo rmmod lazdriver.ko"
        ret = subprocess.call(cmd,shell=True)
        '''
        cmd = "sudo insmod /home/pi/driver/LazDriver/lazdriver.ko"
        ret = subprocess.call(cmd,shell=True)

        cmd = "sudo chmod 0777 "+self.dev
        ret = subprocess.call(cmd,shell=True)

        self.lzgw_w = open(self.dev,"wb",buffering=0)
        self.lzgw = open(self.dev,"rb",buffering=0)

        return 0

    def begin(self,ch,panid,rate,pwr):
        result = self.set_ch(ch)
        if result != ch:
            return -1
        result = self.set_my_panid(panid)
        if result != panid:
            return -2
        result = self.set_bps(rate)
        if result != rate:
            return -3
        result = self.set_pwr(pwr)
        if result != pwr:
            return -4
        result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_BEGIN,0)
        if result != 0:
            return -5
        return 0

    def send(self,panid,rxaddr,payload,length):
        return send(self,panid,rxaddr,payload)

    def send(self,panid,rxaddr,payload):
        result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_TX_PANID,panid)
        if result != panid:
            return -1
        result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_TX_ADDR0,rxaddr)

        if result != rxaddr:
            return-2

        result = self.lzgw_w.write(payload.encode())

        return result

    def close(self):
        result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_CLOSE,0)
        return result

    def remove(self):
        ret = 0
        self.lzgw.close()
        self.lzgw_w.close()
        cmd = "sudo rmmod lazdriver"
        time.sleep(1)
        ret = subprocess.call(cmd,shell=True)

        return ret

    def read(self):
        size = self.available()
        if size > 0:
            raw = self.lzgw.read(size)
            return self.decMac(raw,size)
        else:
            data={}
            return data

    def rxEnable(self):
        result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_RXON,0)
        return result

    def rxDisable(self):
        result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_RXOFF,0)
        return result

    def available(self):
        ret = self.lzgw.read(2)
        if ret == b'':
            return 0
        size = unpack("H",ret)[0]
        return size

    def getMyAddress(self):
        return get_my_addr0()

    def decMac(self,raw,size):
        rcv = {"header":0, "rx_addr_type":-1, "rx_addr":-1, "rx_panid_comp":-1, "rx_panid":-1, "tx_addr_type":-1, "tx_addr":-1, "tx_panid_comp":-1, "tx_panid":-1, "frame_ver":-1, "ielist":-1, "seq_comp":-1, "ack_req":-1, "pending":-1, "sec_enb":-1, "frame_type":-1 ,"rx_sec":-1,"rx_nsec":-1,"rx_rssi":-1}
        offset = 0
        rcv['header']=unpack_from("H",raw,offset)[0]
        offset = 2
        rcv['rx_addr_type'] = (rcv['header'] >> 14)&0x0003
        rcv['frame_ver'] = (rcv['header'] >> 12)&0x0003
        rcv['tx_addr_type'] = (rcv['header'] >> 10)&0x0003
        rcv['ielist'] = (rcv['header'] >> 9)&0x0001
        rcv['seq_comp'] = (rcv['header'] >> 8)&0x0001
        rcv['panid_comp'] = (rcv['header'] >> 6)&0x0001
        rcv['ack_req'] = (rcv['header'] >> 5)&0x0001
        rcv['pending'] = (rcv['header'] >> 4)&0x0001
        rcv['sec_enb'] = (rcv['header'] >> 3)&0x0001
        rcv['frame_type'] = (rcv['header'] >> 0)&0x0007

        if rcv['rx_addr_type'] == 0:
            rcv['rx_addr_enb'] = 0
        else:
            rcv['rx_addr_enb'] = 1

        if rcv['tx_addr_type'] == 0:
            rcv['tx_addr_enb'] = 0
        else:
            rcv['tx_addr_enb'] = 1

        rcv['addr_type'] = rcv['rx_addr_enb']*4 + rcv['tx_addr_enb']*2 + rcv['panid_comp']

        if rcv['addr_type'] == 0:
            rcv['rx_panid_comp'] = 1
            rcv['tx_panid_comp'] = 1
        elif rcv['addr_type'] == 1:
            rcv['rx_panid_comp'] = 0
            rcv['tx_panid_comp'] = 1
        elif rcv['addr_type'] == 2:
            rcv['rx_panid_comp'] = 1
            rcv['tx_panid_comp'] = 0
        elif rcv['addr_type'] == 3:
            rcv['rx_panid_comp'] = 1
            rcv['tx_panid_comp'] = 1
        elif rcv['addr_type'] == 4:
            rcv['rx_panid_comp'] = 0
            rcv['tx_panid_comp'] = 1
        elif rcv['addr_type'] == 5:
            rcv['rx_panid_comp'] = 1
            rcv['tx_panid_comp'] = 1
        elif rcv['addr_type'] == 6:
            rcv['rx_panid_comp'] = 0
            rcv['tx_panid_comp'] = 1
        else:
            rcv['rx_panid_comp'] = 1
            rcv['tx_panid_comp'] = 1

        if rcv['seq_comp'] == 0:
            rcv['seq_num']=unpack_from("B",raw,offset)[0]
            offset = offset + 1

        if rcv['rx_panid_comp'] == 0:
            offset = offset + 2
            rcv['rx_panid'] =unpack_from("H",raw,offset)[0]

        if rcv['rx_addr_type'] == 1:
            rcv['rx_addr']=unpack_from("B",raw,offset)[0]
            offset = offset + 1
        if rcv['rx_addr_type'] == 2:
            rcv['rx_addr']=unpack_from("H",raw,offset)[0]
            offset = offset + 2
        if rcv['rx_addr_type'] == 3:
            rcv['rx_addr']= unpack_from("8B",raw,offset)[0]
            offset = offset + 8

        if rcv['tx_panid_comp'] == 0:
            rcv['tx_panid']=unpack_from("H",raw,offset)[0]
            offset = offset + 2

        if rcv['tx_addr_type'] == 1:
            rcv['tx_addr']=unpack_from("B",raw,offset)[0]
            offset = offset + 1
        if rcv['tx_addr_type'] == 2:
            rcv['tx_addr']=unpack_from("H",raw,offset)[0]
            offset = offset + 2
        if rcv['tx_addr_type'] == 3:
            rcv['tx_addr']=unpack_from("8B",raw,offset)[0]
            offset = offset + 8

        rcv['payload'] = unpack_from("%ds"%(size-offset),raw,offset)[0]


        sec = fcntl.ioctl(self.lzgw,self.IOCTL_GET_RX_SEC1)
        sec = sec * 65536 + fcntl.ioctl(self.lzgw,self.IOCTL_GET_RX_SEC0)
        nsec = fcntl.ioctl(self.lzgw,self.IOCTL_GET_RX_NSEC1)
        nsec = nsec *65536 + fcntl.ioctl(self.lzgw,self.IOCTL_GET_RX_NSEC0)
        rcv["rx_sec"] = sec
        rcv["rx_nsec"] = nsec
        rcv["rx_rssi"]= fcntl.ioctl(self.lzgw,self.IOCTL_GET_RX_RSSI)

        return rcv

    def getSendMode(self):
        self.get_send_mode()
        param = {}
        data = self.get_addr_type()
        param.update({"addr_type": data})
        data = self.get_sense_time()
        param.update({"sense_time": data})
        data = self.get_tx_retry()
        param.update({"tx_retry": data})
        data = self.get_tx_interval()
        param.update({"tx_interval": data})
        data = self.get_cca_wait()
        param.update({"cca_wait": data})
        data = self.get_my_addr0()
        param.update({"my_address": data})

        return param

    def setSendMode(self,param):
        self.get_send_mode()
        if "addr_type" in param:
            self.set_addr_type(param["addr_type"])
        if "sense_time" in param:
            self.set_addr_type(param["sense_time"])
        if "tx_retry" in param:
            self.set_tx_retry(param["tx_retry"])
        if "tx_interval" in param:
            self.set_tx_interval(param["tx_interval"])
        if "cca_wait" in param:
            self.set_cca_wait(param["cca_wait"])
        self.set_send_mode()
        return 0

    def getAddrType(self):
        if fcntl.ioctl(self.lzgw,self.IOCTL_GET_SEND_MODE) != 0:
            return -1
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_ADDR_TYPE)

    def setAddrType(self,addr_type):
        if fcntl.ioctl(self.lzgw,self.IOCTL_GET_SEND_MODE) != 0:
            return -1
        if fcntl.ioctl(self.lzgw,self.IOCTL_SET_ADDR_TYPE,addr_type) != addr_type:
            return -2
        if fcntl.ioctl(self.lzgw,self.IOCTL_SET_SEND_MODE) != 0:
            return -3
        return 0

    def getTxRetry(self):
        fcntl.ioctl(self.lzgw,self.IOCTL_GET_SEND_MODE)
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_TX_RETRY)

    def setTxRetry(self,tx_retry):
        if fcntl.ioctl(self.lzgw,self.IOCTL_GET_SEND_MODE) != 0:
            return -1
        if fcntl.ioctl(self.lzgw,self.IOCTL_SET_TX_RETRY,tx_retry) != tx_retry:
            return -2
        if fcntl.ioctl(self.lzgw,self.IOCTL_SET_SEND_MODE) != 0:
            return -3
        return 0

    def get_ch(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_CH,0)

    def set_ch(self,ch):
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_CH,ch)

    def get_my_panid(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_MY_PANID,0)

    def set_my_panid(self,panid):
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_MY_PANID,panid)

    def get_bps(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_BPS,0)

    def set_bps(self,bps):
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_BPS,bps)

    def get_pwr(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_PWR,0)

    def set_pwr(self,pwr):
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_PWR,pwr)

    def get_send_mode(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_SEND_MODE,0)

    def set_send_mode(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_SEND_MODE,0)

    def get_sense_time(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_SENSE_TIME,0)

    def set_sense_time(self,stime):
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_SENSE_TIME,stime)

    def get_tx_retry(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_TX_RETRY,0)

    def set_tx_retry(self,txretry):
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_TX_RETRY,txretry)

    def get_tx_interval(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_TX_INTERVAL,0)

    def set_tx_interval(self,txinterval):
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_TX_INTERVAL,txinterval)

    def get_cca_wait(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_CCA_WAIT,0)

    def set_cca_wait(self,ccawait):
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_CCA_WAIT,ccawait)

    def get_my_addr0(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_MY_ADDR0,0)

    def get_my_addr1(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_MY_ADDR1,0)

    def get_my_addr2(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_MY_ADDR2,0)

    def get_my_addr3(self):
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_MY_ADDR3,0)

    def get_addr_type(self): 
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_ADDR_TYPE,0)

    def set_addr_type(self,addr_type): 
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_ADDR_TYPE,addr_type)

    def get_tx_retry(self): 
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_TX_RETRY,0)

    def set_tx_retry(self,retry): 
        return fcntl.ioctl(self.lzgw,self.IOCTL_SET_TX_RETRY,retry)

    def get_rx_sec0(self): 
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_RX_NSEC0,0)

    def get_rx_sec1(self): 
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_RX_NSEC1,0)

    def get_rx_nsec0(self): 
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_RX_SEC0,0)

    def get_rx_nsec1(self): 
        return fcntl.ioctl(self.lzgw,self.IOCTL_GET_RX_SEC1,0)

