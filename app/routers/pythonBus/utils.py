'''
these methods are here in order to be used
in different part of the app.
'''

from crc import Calculator, Crc8, Crc16, Crc32, Configuration

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
            temp.append(f"{key}_{element}")
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



def configureCrcCalculator(width=8,
        polynomial=0x1D,
        init_value=0xFF,
        final_xor_value=0xFF,
        reverse_input=False,
        reverse_output=False):
    config = Configuration(
        width=width,
        polynomial=polynomial,
        init_value=init_value,
        final_xor_value=final_xor_value,
        reverse_input=reverse_input,
        reverse_output=reverse_output,
    )
    return Calculator(config)


def calculateNewCrc(msg):
    new_crc = configureCrcCalculator().checksum(msg.data[:msg.dlc-1])
    # Create a new data array with the new CRC value replacing the last byte
    new_data = msg.data[:-1] + new_crc.to_bytes(1, byteorder='big')
    return new_data


