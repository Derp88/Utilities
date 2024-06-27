import subprocess
import time
import os
from datetime import datetime

#Example IPs
#routerIP = "10.0.0.1"
#modemIP = "192.168.100.1"
#DNSGoogleIP = "8.8.8.8"
IPs = []
IPnames = []

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
    print(sourceName + ": OK  "+ "  Ping: " + averageTime + "   @(" + currentTime + ")" )

def logFailure(sourceName):
    #Get current time
    currentTime = datetime.now().strftime("%H:%M:%S")
    #Log output
    with open("pingLog.txt", "a+") as logFile:
        logFile.write(currentTime + " " + sourceName + "  ### FAILED TO RESPOND ###" + "\n")
    #Log output in special file
    with open("failLog.txt", "a+") as logfailFile:
        logfailFile.write(currentTime + " " + sourceName + "  Failure to respond" + "\n")
    print(sourceName + ": FAIL  "+ "(" + currentTime + ")" )

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

#Get duration
def getDuration():
    try:
        return int(input("How much time (seconds) in between pings: "))
    except ValueError:
        print("Non-Integer entered, try again.")
        getDuration() #Call this function again if a bad value was entered

def getIPs():
    ip = input("Please enter the IP you want to ping: ")
    name = input("Enter a name for this ip (Enter 'N' if you don't want a name): ")
    if name == "N" or name == "n":
        name = ip #Just use the IP as the name if the user doesn't give one.
    keepGoing = input("Enter 'Y' to input more IPs. Enter 'N' to finish entering IPs: ").capitalize()
    IPs.append(ip) #Add IP to list
    IPnames.append(name) #Add IP name to list
    if keepGoing == "Y": #In case the user wants more names
        getIPs()
    
#User input
duration = getDuration() #This only needs to called once, so outside the loop
getIPs() #Get the IPs we want to use from the user
#Main program loop
while True:
    #Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    for ipIndex, ip in enumerate(IPs):
        attemptPingLog(ip, IPnames[ipIndex])

    #Wait before running again
    time.sleep(duration)



