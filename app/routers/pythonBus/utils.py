'''
these methods are here in order to be used
in different part of the app.
'''

# this dict contain all the VectorCanChannel Object
canChannel = {}
hwChannelPairs = {}
hwChannelPairsWithDetails = []
DAIOChannel = None
DAIOChannelDetails = {}

def pythonBusStop():
    global canChannel
    for key in canChannel.keys():
        canChannel[key].stop()
    return "succesfully stopped all the buses"

def pythonBusGetPropagation():
    global canChannel
    temp = []
    for key in canChannel.keys():
        for element in canChannel[key].propagate.keys():
            temp.append(element)
    return temp

def pythonBusClear():
    global canChannel
    pythonBusStop()
    canChannel = {}
    return "succesfully stopped all the buses"
    

def startAllLog():
    for bus in canChannel.values():
        bus.startLog()
    return "Succesfully started all the logs"
    

def stopAllLog():
    for bus in canChannel.values():
        bus.stopLog()
    DAIOChannel.stopLog()
    return "Succesfully stopped all the logs"



