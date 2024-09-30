import socket # for sockets
import sys # for exit
import time # for sleep
#-----------------------------------------------------------------------------

try:
    #create and AF_INET, STEREAM socket(TCP)
    inst = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    inst.settimeout(3)
except socket.error(msg):
    print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    inst.exit();

print('Socket Created')

# Alter this host name, or IP address, in the line below to accommodate your specific instrument
host = '10.0.0.68' # Or you could utilize an IP address.

# Alter the socket port number in the line below to accommodate your 
# specific instrument socket port. Traditionally, most BK Precision, 
# LAN based instrumentation socket ports use 10001. 
# Refer to your specific instrument User Guide for additional details.
port = 30000
#
# A delay time variable for the sleep function call, unit is seconds
# For clarification of the use of the waitTime variable used in the sleep timer call
# please refer to any one of these function calls and the notes on the timer use:
    # getDataAsAsciiTransfer() - FUNCTION
    # getDataAsBinBlockTransfer() - FUNCTION 
    # getStimulusArrayAsBinBlock() - FUNCTION
waitTime = 0.2

try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    #could not resolve
    print('Hostname could not be resolved. Exiting')
    inst.exit()
    inst.close()
    
print('Ip address of ' + host + ' is ' + remote_ip)

# Given the instrument's computer name or IP address and socket port number now
# connect to the instrument remote server socket connection. At this point we
# are instantiating the instrument as a LAN SOCKET CONNECTION.

try: 
    inst.connect((remote_ip , port))

except socket.gaierror:
        #could not resolve
    print('Failed to connect to.' + remote_ip + 'Exiting')
    inst.exit()
    inst.close()

print('Socket Connected to ' + host + ' on ip ' + remote_ip)

# ==========================================================================
# Function to initialize the instrument
def instrumentInit():
  
    try :
        #Clear the event status register and all prior errors in the queue
        #inst.sendall(b"*CLS\n")
        
        # Reset instrument and via *OPC? hold-off for reset completion.
        #inst.sendall(b"*RST\n")
        #opComplete = inst.recv(8)
        #print "Operation complete detection = " + resetComplete
        
        # Assert a Identification query
        inst.sendall(b"*IDN?\n")
        idnResults = inst.recv(255)
        ID = str(idnResults, "UTF-8")
        print("ID = \n")
        print(ID)
        instrumentErrCheck()
        inst.sendall(b"system:serial?\n")
        time.sleep(1)
        serial = inst.recv(255)
        SN = str(serial, "UTF-8")
        print("SN = \n")
        print(SN)

        
    except socket.error:
        #Send failed
        print('Instrument Init failed')
        inst.exit()
    return;

# ==========================================================================
# Function to check the system error queue
def instrumentErrCheck():
   
    try :
        # Instrument error queues may store several errors. Loop and display all errors until 
        # no error indication
        
        errOutClear = -1
        noErrResult = "NO ERROR"
         
        while (errOutClear < 0  ):
            inst.sendall(b"SYST:ERR?\n")
            errQueryResults = inst.recv(255)
            Error = str(errQueryResults, "UTF-8")
            Error = Error.upper()
            print("Error query reults = " + Error)
            errOutClear = Error.find(noErrResult)
    except socket.error:
        #Send failed
        print('Error Check failed')
        inst.exit()
    return

def readData():
    try:

        while True: 
            instrumentErrCheck()
            inst.sendall(b"MEAS:VOLT?\n")                             #delay of 250 ms can change for data acquisition rate
            time.sleep(.25)
            read = inst.recv(255)
            meas = str(read, "UTF-8")
            print(meas + "\n")
            time.sleep(.25)
           
    except KeyboardInterrupt:
        print("Data Acquired")
        inst.close() 
        print ("Application complete")

def main():
    instrumentInit()
    #readData()
    inst.close()

if __name__ == "__main__":
    proc = main()
