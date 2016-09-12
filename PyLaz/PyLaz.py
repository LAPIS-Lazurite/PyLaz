import fcntl
import subprocess
from struct import *

class PyLaz:
	IOCTL_CMD=		0x0000
	IOCTL_SET_BEGIN=	IOCTL_CMD+0x11
	IOCTL_SET_RXON=		IOCTL_CMD+0x13
	IOCTL_SET_RXOFF=	IOCTL_CMD+0x15
	IOCTL_SET_CLOSE=	        IOCTL_CMD+0x17
	IOCTL_GET_SEND_MODE=	IOCTL_CMD+0x18
	IOCTL_SET_SEND_MODE=	IOCTL_CMD+0x19
	IOCTL_PARAM=		0x1000
	IOCTL_GET_CH=		IOCTL_PARAM+0x02
	IOCTL_SET_CH=		IOCTL_PARAM+0x03
	IOCTL_GET_PWR=		IOCTL_PARAM+0x04
	IOCTL_SET_PWR=		IOCTL_PARAM+0x05
	IOCTL_GET_BPS=		IOCTL_PARAM+0x06
	IOCTL_SET_BPS=		IOCTL_PARAM+0x07
	IOCTL_GET_MY_PANID=	IOCTL_PARAM+0x08
	IOCTL_SET_MY_PANID=	IOCTL_PARAM+0x09
	IOCTL_GET_TX_PANID=	IOCTL_PARAM+0x0a
	IOCTL_SET_TX_PANID=	IOCTL_PARAM+0x0b
	IOCTL_GET_MY_ADDR0=	IOCTL_PARAM+0x0c
	IOCTL_SET_MY_ADDR0=	IOCTL_PARAM+0x0d
	IOCTL_GET_MY_ADDR1=	IOCTL_PARAM+0x0e
	IOCTL_SET_MY_ADDR1=	IOCTL_PARAM+0x0f
	IOCTL_GET_MY_ADDR2=	IOCTL_PARAM+0x10
	IOCTL_SET_MY_ADDR2=	IOCTL_PARAM+0x11
	IOCTL_GET_MY_ADDR3=	IOCTL_PARAM+0x12
	IOCTL_SET_MY_ADDR3=	IOCTL_PARAM+0x13
	IOCTL_GET_TX_ADDR0=	IOCTL_PARAM+0x14
	IOCTL_SET_TX_ADDR0=	IOCTL_PARAM+0x15
	IOCTL_GET_TX_ADDR1=	IOCTL_PARAM+0x16
	IOCTL_SET_TX_ADDR1=	IOCTL_PARAM+0x17
	IOCTL_GET_TX_ADDR2=	IOCTL_PARAM+0x18
	IOCTL_SET_TX_ADDR2=	IOCTL_PARAM+0x19
	IOCTL_GET_TX_ADDR3=	IOCTL_PARAM+0x1a
	IOCTL_SET_TX_ADDR3=	IOCTL_PARAM+0x1b
	IOCTL_GET_ADDR_TYPE=	IOCTL_PARAM+0x1c
	IOCTL_SET_ADDR_TYPE=	IOCTL_PARAM+0x1d
	IOCTL_GET_ADDR_SIZE=	IOCTL_PARAM+0x1e
	IOCTL_SET_ADDR_SIZE=	IOCTL_PARAM+0x1f
	IOCTL_GET_DRV_MODE=	IOCTL_PARAM+0x20
	IOCTL_SET_DRV_MODE=	IOCTL_PARAM+0x21
	IOCTL_GET_SENSE_TIME=	IOCTL_PARAM+0x22
	IOCTL_SET_SENSE_TIME=	IOCTL_PARAM+0x23
	IOCTL_GET_TX_RETRY=	IOCTL_PARAM+0x24
	IOCTL_SET_TX_RETRY=	IOCTL_PARAM+0x25
	IOCTL_GET_TX_INTERVAL=	IOCTL_PARAM+0x26
	IOCTL_SET_TX_INTERVAL=	IOCTL_PARAM+0x27
	IOCTL_GET_CCA_WAIT=	IOCTL_PARAM+0x28
	IOCTL_SET_CCA_WAIT=	IOCTL_PARAM+0x29
	IOCTL_GET_RX_SEC0=	IOCTL_PARAM+0x2A
	IOCTL_GET_RX_SEC1=	IOCTL_PARAM+0x2C
	IOCTL_GET_RX_NSEC0=	IOCTL_PARAM+0x2E
	IOCTL_GET_RX_NSEC1=	IOCTL_PARAM+0x30
	IOCTL_GET_RX_RSSI=	IOCTL_PARAM+0x32
	IOCTL_GET_TX_RSSI=	IOCTL_PARAM+0x34

	lzgw = 0
	lzgw_w = 0
	dev="/dev/lzgw"

	def open(self):
		cmd = "sudo insmod /home/pi/driver/LazDriver/lazdriver.ko"
		ret = subprocess.call(cmd,shell=True)
		print("%s = %d"%(cmd,ret))

		cmd = "sudo chmod 0777 "+self.dev
		ret = subprocess.call(cmd,shell=True)
		print("%s = %d"%(cmd,ret))
		if ret != 0:
			return -2
		self.lzgw_w = open(self.dev,"wb",buffering=0)
		self.lzgw = open(self.dev,"rb")

		return 0

	def begin(self,ch,panid,rate,pwr):
		result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_CH,ch)
		if result != ch:
			return -1
		result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_MY_PANID,panid)
		if result != panid:
			return -2
		result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_BPS,rate)
		if result != rate:
			return -3
		result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_PWR,pwr)
		if result != pwr:
			return -4
		result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_BEGIN,0)
		if result != 0:
			return -5
		return 0

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
		self.lzgw.close()
		cmd = "sudo rmmod lazdriver"
		ret = subprocess.call(cmd,shell=True)
		return ret
	
	def read(self):
		size = self.lzgw.read(2)
		if size > 0
		raw = self.lzgw.read(size)
		return self.decMac(raw)

	def rxEnable(self):
		result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_RXON,0)
		return result
	def rxDisable(self):
		result = fcntl.ioctl(self.lzgw,self.IOCTL_SET_RXOFF,0)
		return result

	def decMac(self,raw):
		header=unpack_from("H",raw,0)[0]
		
		rx_addr_type = bin(header >> 14)&0x0003
		frame_ver = bin(header >> 12)&0x0003
		tx_addr_type = bin(header >> 10)&0x0003
		ielist = bin(header >> 9)&0x0001
		seq_comp = bin(header >> 8)&0x0001
		panid_comp = bin(header >> 6)&0x0001
		ack_req = bin(header >> 5)&0x0001
		pending = bin(header >> 4)&0x0001
		seq_enb = bin(header >> 3)&0x0001
		frame_type = bin(header >> 3)&0x0007

		addr_type = rx_addr_type*4 + tx_addr_type*2 + panid_comp

		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		elif addr_type == 1:
                        rx_panid = True
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		if addr_type == 0:
                        rx_panid = False
                        tx_panid = False
		header=unpack_from("H",raw,0)[0]
		header=unpack_from("H",raw,0)[0]
		header=unpack_from("H",raw,0)[0]
		header=unpack_from("H",raw,0)[0]
		header=unpack_from("H",raw,0)[0]
		header=unpack_from("H",raw,0)[0]
		header=unpack_from("H",raw,0)[0]
		header=unpack_from("H",raw,0)[0]
		header=unpack_from("H",raw,0)[0]
		return 0
