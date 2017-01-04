from socket import *
import threading
from Crypto.Cipher import AES

Host = ''
Porta = 4000
Portb = 4005
Portc = 4006
Portd = 4007
BEPort1 = 4001
BEPort2 = 4002
BEPort3 = 4003
BEPort4 = 4004
Port3=4002

flagForConnectedPrimaryBEserver1 = 1
flagForSecondaryBEserver1 = 1
flagForConnectedPrimaryBEserver2 = 1
flagForSecondaryBEserver2 = 1

def do_encrypt(message):
        obj = AES.new('key1234567890123', AES.MODE_CBC, '1234567890123456')
        ciphertext = obj.encrypt(message)
        return ciphertext

def do_decrypt(ciphertext):
    obj2 = AES.new('key1234567890123', AES.MODE_CBC, '1234567890123456')
    message = obj2.decrypt(ciphertext)
    return message

connectedClients=[]

file1=open('configfile','r')
for line in file1:
	linelist = line.split()
	if linelist[0] == "primary1":
		connectedPrimaryBEserver1 = linelist[1]
	elif linelist[0] == "primary2":
		connectedPrimaryBEserver2 = linelist[1]
	elif linelist[0] == "secondary1":
		connectedSecondaryBEserver1 = linelist[1]
	elif linelist[0] == "secondary2":
		connectedSecondaryBEserver2 = linelist[1]

print "Primary BE server is", connectedPrimaryBEserver1
print "Secondary BE server is", connectedSecondaryBEserver1
print "Primary BE server2 is", connectedPrimaryBEserver2
print "Secondary BE server2 is", connectedSecondaryBEserver2
print "flagForConnectedPrimaryBEserver1", flagForConnectedPrimaryBEserver1
print "flagForSecondaryBEserver1", flagForSecondaryBEserver1
print "flagForConnectedPrimaryBEserver2", flagForConnectedPrimaryBEserver2
print "flagForSecondaryBEserver2", flagForSecondaryBEserver2

socket1 = socket(AF_INET, SOCK_DGRAM)
socket2 = socket(AF_INET, SOCK_DGRAM)
socket3 = socket(AF_INET, SOCK_DGRAM)
socket4 = socket(AF_INET, SOCK_DGRAM)
socket5 = socket(AF_INET, SOCK_DGRAM)
socket1.bind((Host,Porta))
socket3.bind((Host,Portb))
socket4.bind((Host,Portc))
socket5.bind((Host,Portd))
socket2.bind((Host,Port3))
socket1.settimeout(5.0)
# socket2.settimeout(5.0)
socket3.settimeout(5.0)
socket4.settimeout(5.0)
socket5.settimeout(5.0)

def serverside1(): 
	global flagForConnectedPrimaryBEserver1
	while 1:
		data = "SYN-SENT"	
		# Primary Back End server 1
		socket1.sendto(data,(connectedPrimaryBEserver1, BEPort1))
		# print "sent1"
		try:
			data2, address = socket1.recvfrom(2048)
			# print "received 1"
			if data2 == "SYN-RECEIVED":
				flagForConnectedPrimaryBEserver1 = 1
			else:
				flagForConnectedPrimaryBEserver1 = 0
		except Exception:
			flagForConnectedPrimaryBEserver1 = 0

def serverside2(): 

	global flagForSecondaryBEserver1
	while 1:
		data = "SYN-SENT"	
		# Primary Back End server 1
		socket3.sendto(data,(connectedSecondaryBEserver1, BEPort2))
		# print "sent2"
		try:
			data2, address = socket3.recvfrom(2048)
			# print "received 2"
			if data2 == "SYN-RECEIVED":
				flagForSecondaryBEserver1 = 1
			else:
				flagForSecondaryBEserver1 = 0
		except Exception:
			flagForSecondaryBEserver1 = 0

def serverside3(): 
	global flagForConnectedPrimaryBEserver2
	while 1:
		data = "SYN-SENT"	
		# Primary Back End server 1
		socket4.sendto(data,(connectedPrimaryBEserver2, BEPort3))
		# print "sent3"
		try:
			data2, address = socket4.recvfrom(2048)
			# print "received 3"
			if data2 == "SYN-RECEIVED":
				flagForConnectedPrimaryBEserver2 = 1
			else:
				flagForConnectedPrimaryBEserver2 = 0
				
		except Exception:
			flagForConnectedPrimaryBEserver2 = 0

def serverside4(): 
	global flagForSecondaryBEserver2
	while 1:
		data = "SYN-SENT"	
		socket5.sendto(data,(connectedSecondaryBEserver2, BEPort4))
        # print "sent 2"
        	try:
        		data2, address = socket5.recvfrom(2048)
            		# print "received 4"
            		if data2 == "SYN-RECEIVED":
                		flagForSecondaryBEserver2 = 1
	    		else:
				flagForSecondaryBEserver2 = 0
        	except Exception:
            		flagForSecondaryBEserver2 = 0

def clientside():
	global flagForConnectedPrimaryBEserver1, flagForSecondaryBEserver1
	global flagForConnectedPrimaryBEserver2, flagForSecondaryBEserver2
	global even, odd
	# print "entered client recv thread outside"
	while 1:
		# print "entered client recv thread inside"
		data, address = socket2.recvfrom(2048)
		print "client joined from address", address
   		data2 = do_decrypt(data)
		data3 = data2.split('^')
		data = data3[0]
		load = len(data)
		data = data.ljust(16, '^')
		data = do_encrypt(data)
		if (address not in connectedClients):
			print "new client is sent to BE", address
			connectedClients.append(address)
			update_data="add!"+str(address)
			socket1.sendto(update_data,(connectedPrimaryBEserver1, BEPort1))
			socket4.sendto(update_data,(connectedPrimaryBEserver2, BEPort2))
			socket3.sendto(update_data,(connectedSecondaryBEserver1, BEPort3))
			socket5.sendto(update_data,(connectedSecondaryBEserver2, BEPort4))
		odd = 0
		even = 0
		for i in range(len(connectedClients)):
			if address == connectedClients[i]:
				j = i%2
				if j == 0:
					even = 1
					break
				else:
					odd = 1
					break
			else:
				even = 0
				odd = 0
		data="message!"+str(address)+"!"+data
		if load >= 7:
			odd = 0
			even = 0
			if flagForConnectedPrimaryBEserver1 == 1:
				print "data sent to P1"
				socket1.sendto(data,(connectedPrimaryBEserver1, BEPort1))
			elif flagForSecondaryBEserver1 == 1:
				print "data sent to S1"
				socket3.sendto(data,(connectedSecondaryBEserver1, BEPort2))
			elif flagForConnectedPrimaryBEserver2 == 1:
				print "data sent to P2"
				socket4.sendto(data,(connectedPrimaryBEserver2, BEPort3))
			elif flagForSecondaryBEserver2 == 1:
				print "data sent to s2"
				socket5.sendto(data,(connectedSecondaryBEserver2, BEPort4))

		print "data received is", data
		print "even is", even
		print "odd is", odd
		print "flagForConnectedPrimaryBEserver1", flagForConnectedPrimaryBEserver1
		print "flagForSecondaryBEserver1", flagForSecondaryBEserver1
		print "flagForConnectedPrimaryBEserver2", flagForConnectedPrimaryBEserver2
		print "flagForSecondaryBEserver2", flagForSecondaryBEserver2 
		if even == 1:
			if flagForConnectedPrimaryBEserver1 == 1:
				print "data sent to P1"
				socket1.sendto(data,(connectedPrimaryBEserver1, BEPort1))
			elif flagForSecondaryBEserver1 == 1:
				print "data sent to S1"
				socket3.sendto(data,(connectedSecondaryBEserver1, BEPort2))
			elif flagForConnectedPrimaryBEserver2 == 1:
				print "data sent to P2"
				socket4.sendto(data,(connectedPrimaryBEserver2, BEPort3))
			elif flagForSecondaryBEserver2 == 1:
				print "data sent to S2"
				socket5.sendto(data,(connectedSecondaryBEserver2, BEPort4))

		if odd == 1:
			if flagForConnectedPrimaryBEserver2 == 1:
				print "data sent to P2"
				socket4.sendto(data,(connectedPrimaryBEserver2, BEPort3))
			elif flagForSecondaryBEserver2 == 1:
				print "data sent to S2"
				socket5.sendto(data,(connectedSecondaryBEserver2, BEPort4))
			elif flagForConnectedPrimaryBEserver1 == 1:
				print "data sent to P1"
				socket1.sendto(data,(connectedPrimaryBEserver1, BEPort1))
			elif flagForSecondaryBEserver1 == 1:
				print "data sent to S1"
				socket3.sendto(data,(connectedSecondaryBEserver1, BEPort2))
	
def updateClient():
	# print "entered updating client recv thread outside"
	global flagForConnectedPrimaryBEserver, flagForconnectedSecondaryBEserver
	while 1:
		# print "entered updating client recv thread inside"
		for i in range(len(connectedClients)):
                        update_data="add!"+str(connectedClients[i])
                        socket1.sendto(update_data,(connectedPrimaryBEserver1, BEPort1))
                        socket3.sendto(update_data,(connectedSecondaryBEserver1, BEPort2))
                        socket4.sendto(update_data,(connectedPrimaryBEserver2, BEPort3))
                        socket5.sendto(update_data,(connectedSecondaryBEserver2, BEPort4))
	Timer(3,updateClient).start()

first1 = threading.Thread(target = serverside1)
first1.daemon = True
first2 = threading.Thread(target = serverside2)
first2.daemon = True
first3 = threading.Thread(target = serverside3)
first3.daemon = True
first4 = threading.Thread(target = serverside4)
first4.daemon = True
second = threading.Thread(target = clientside)
second.daemon = True
third = threading.Thread(target = updateClient)
third.daemon = True
# second.setDaemon(False)
# third.setDaemon(False)
first1.start()
first2.start()
first3.start()
first4.start()
second.start()
third.start()
first1.join()
first2.join()
first3.join()
first4.join()
second.join()
third.join()
sys.exit()
