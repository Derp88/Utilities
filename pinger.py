import subprocess
import time
from datetime import datetime

#IPs that we will be pinging
routerIP = "10.0.0.1"
modemIP = "192.168.100.1"
DNSGoogleIP = "8.8.8.8"

#Log file
logFile = open("pingLog.txt", "a+")
def logSuccess(sourceName, result):
    #Get current time
    currentTime = datetime.now().strftime("%H:%M:%S")
    #Get positions of string to grab data from
    timeStartPosition = result.find("Average = ") + 10
    timeEndPosition = len(result)-2
    packetLossStartPosition = result.find(" (") + 2
    packetLossEndPosition = result.find(")")
    #Results
    averageTime = result[timeStartPosition:timeEndPosition]
    packetLoss = result[packetLossStartPosition:packetLossEndPosition]
    #Log output
    with open("pingLog.txt", "a+") as logFile:
        logFile.write(currentTime + " " + sourceName + "  Responded in " + averageTime + " with " + packetLoss + "\n")

def logFailure(sourceName):
    #Get current time
    currentTime = datetime.now().strftime("%H:%M:%S")
    #Log output
    with open("pingLog.txt", "a+") as logFile:
        logFile.write(currentTime + " " + sourceName + "  ### FAILED TO RESPOND ###" + "\n")
    #Log output in special file
    with open("failLog.txt", "a+") as logFile:
        logFile.write(currentTime + " " + sourceName + "  Failure to respond" + "\n")

def attemptPingLog(ip, sourceName):
    #Try to ping device
    try: 
        result = subprocess.check_output(["ping", '-n', "1", ip]).decode("utf-8")
    except: #The ping returned an error code
        logFailure(sourceName)
    else: #The ping didn't return an error, but this is not nessecarily a success
        if ("Reply from " + ip) in result:
            logSuccess(sourceName, result)
        else:
            logFailure(sourceName)

while True:
    #Try to ping router
    attemptPingLog(routerIP, "ROUTER")
    #Try to ping Modem
    attemptPingLog(modemIP, "MODEM ")
    #Try to ping DNS
    attemptPingLog(DNSGoogleIP, "DNS   ")
    
    #Wait 60 seconds before running again
    time.sleep(60)



