from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
import json
from asyncio import sleep

from lib.pythonBus import pythonBus as pb
from lib.pythonBus import DAIO as d2
from lib import global_var

from lib import local_config

from app import schemas
from app.routers.pythonBus import utils

import traceback

# Custom serialization function
def custom_serializer(obj):
    if isinstance(obj, pb.VectorCanChannel):
        # Here, you can decide how you want to represent your object.
        # For example, you might choose to just represent it with a string:
        return f"VectorCanChannel {obj.channelName}, channel num: {obj.channelNum}"
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")





router = APIRouter(
    prefix="/pythonbus",
    tags=['Python Bus']
)


@router.get("/")
def getInfo():
    return "pythonbus"


@router.get("/availableHw")
def getAvailableHardware():
    """this return the dictionary of all available hardware 
    connected to the COM port of the pc.

    Returns:
        _type_: _description_
    """    
    return pb.getAvailableHw()


@router.get("/availableHw/can")
def getAvailableHardwareCanCompatible():
    """this returns a well formatted list of all available hardware 
    connected to the COM port of the pc with CAN capabilities (no virtual).

    Returns:
        _type_: _description_
    """    
    try:
        temp = pb.getAvailableHw()
        hwList = []
        for key in temp.keys():
            if key != 100:
                if key not in hwList:
                    toappend = f"{temp[key][0]['name'].split(' ')[0]} - {key}"
                    hwList.append(toappend)

        return hwList 
    except:
        raise HTTPException(status_code=404, detail="Error getting available hw")
    

@router.get("/availableHw/daio")
def getAvailableHardwareCanCompatible():
    """this returns a well formatted list of all available hardware 
    connected to the COM port of the pc with CAN capabilities (no virtual).

    Returns:
        _type_: _description_
    """    
    try:
        temp = pb.getAvailableHw()
        hwDict = []
        for key in temp.keys():
            if key != 100:
                for channel in temp[key]:
                    if 64 in temp[key][channel]["bus_capabilities"] or 4194304 in temp[key][channel]["bus_capabilities"]:
                        hwDict.append(key)
        return hwDict 
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Error getting available DAIO channel")



@router.get("/hwAvailableChannel/{serial}")
def getAvailableHardwareCanCompatible(serial: int):
    """this returns a well formatted list of all available hardware 
    connected to the COM port of the pc with CAN capabilities (no virtual).

    Returns:
        _type_: _description_
    """    
    try:
        temp = pb.getAvailableHw()
        selectedHw = temp[serial]
        availableChannel = []
        for key in selectedHw.keys():
            if 65536 in selectedHw[key]['bus_capabilities'] or 1 in selectedHw[key]['bus_capabilities'] and not "LIN" in selectedHw[key]["transceiver_name"] and selectedHw[key]["transceiver_name"] != "":
                if not serial in utils.hwChannelPairs:
                    availableChannel.append(int(key)+1)
                else:
                    if not int(key) in utils.hwChannelPairs[serial]:
                        availableChannel.append(int(key)+1)

        return availableChannel 
    except:
        raise HTTPException(status_code=404, detail="Error getting available hw channel")




@router.post("/initialize")
def pythonBusInitialize(data: schemas.VectorChannelConfig):

    userChannelConfig = {
        "hw_channel": data.hw_channel, #the channel number (relative to the hardware physical channel)
        "serial_number": data.serial_number, #the serial number of the harware 
        "ch_num": data.ch_num, #application channel number (this should be managed automatically to avoid definition of channel usage number like CANoe)
        "hw_type": pb.getAvailableHw()[data.serial_number][0]['hw_type'], #hardware type among the hardwareDict
        "bitrate": data.bitrate, #bitrate of the current channel
        "fd": data.fd,
        "data_bitrate": data.data_bitrate,
        "name": data.name
    }
    utils.canChannel[data.name] = pb.VectorCanChannel(userChannelConfig, data.db_path, data.txtLog)

    print(f"CAN CHANNEL NUMBER: {userChannelConfig['ch_num']}")

    utils.canChannel[data.name].maxSize = data.maxSize
    utils.canChannel[data.name].decode = data.decode
    
    userChannelConfig["dbPath"] = data.db_path

    if data.propagate != "":
        userChannelConfig["propagation"] = data.propagate
        temp = data.propagate.split(",")
        utils.canChannel[data.name].populatePropagation(temp)
        pass

    
    utils.canChannel[data.name].start()

    # This is used to filter the active hw-channel in "/hwAvailableChannel/{serial}"
    if data.serial_number in utils.hwChannelPairs:
        utils.hwChannelPairs[data.serial_number].append(data.hw_channel)
    else:
        utils.hwChannelPairs[data.serial_number] = [data.hw_channel]

    utils.hwChannelPairsWithDetails.append(userChannelConfig)

    
    
    return {"message": "succesfully started the bus"}


@router.post("/updatepropagation")
def updatePropagation(data: schemas.VectorChannelConfig):

    if data.propagate != "":
        temp = data.propagate.split(",")
        utils.canChannel[data.name].populatePropagation(temp)
    else:
        # If no propagation is given, call the function with empty string to delete all the values propagated
        utils.canChannel[data.name].populatePropagation("")

    # Now update the hwChannelPairsWithDetails list with the new propagation string
    newList = []
    for element in utils.hwChannelPairsWithDetails:
        if element["name"] == data.name:
            element["propagation"] = data.propagate
            newList.append(element)
        else:
            newList.append(element)
        

    return {"message": "succesfully updated propagation"}
    
# @router.get("/canchannel")
# def getActiveChannel():
#     return json.dumps(utils.canChannel, default=custom_serializer)


@router.get("/canchannel")
def getActiveChannel():
    return utils.hwChannelPairsWithDetails

@router.get("/propagatedvalues")
def getPropagatedValues():
    return utils.pythonBusGetPropagation()


@router.post("/deleteChannel")
def getActiveChannel(data: schemas.RemoveChannel):
    try:
        utils.canChannel[data.name].stop()
        utils.canChannel.pop(data.name)
        utils.hwChannelPairs[data.serial_number].remove(data.hw_channel)
        utils.hwChannelPairsWithDetails = [d for d in utils.hwChannelPairsWithDetails if d.get('name') != data.name]
    except Exception as e:
        print(f"error: {e}")


@router.post("/daio/start")
def startDAIO(data: schemas.DAIOstart):
    index = pb.getAvailableHw()[data.serial_number][0]['hw_index']
    utils.DAIOChannel = d2.DAIOChannel(index, data.frequency, channelNum=data.ch_num)
    utils.DAIOChannel.start()
    utils.DAIOChannelDetails = {"serial_number":data.serial_number,
                                 "frequency": data.frequency,
                                 "ch_num": data.ch_num}
    print(f"DAIO CHANNEL NUMBER: {data.ch_num}")
    return {"message": "succesfully started the DAIO"}

@router.get("/daiochannel")
def getActiveDAIOChannel():
    #Return as a list, since in react I'll use the value as an array
    if utils.DAIOChannelDetails:
        return [utils.DAIOChannelDetails]
    else:
        return []
    


@router.get("/daio/stop")
def stopDAIO():
    utils.DAIOChannel.stop()
    # Delete the DAIOChannel object
    del utils.DAIOChannel

    utils.DAIOChannel = None
    utils.DAIOChannelDetails = {}
    return {"message": "succesfully stopped the DAIO"}


@router.get("/daio/startlog")
def startlogDAIO():
    utils.DAIOChannel.startLog()
    return {"message": "succesfully started the DAIO log"}


@router.get("/daio/stoplog")
def stoplogDAIO():
    try:
        utils.DAIOChannel.stopLog()
    except:
        print(traceback.print_exc())
    return {"message": "succesfully stopped the DAIO log"}



@router.get("/all/stop")
def pbs():
    return utils.pythonBusStop()
    


@router.get("/all/startlog")
def sal():
    return utils.startAllLog()



@router.get("/all/stoplog")
def stal():
    try:
        return utils.stopAllLog()
    except:
        return {"stopped"}



@router.websocket("/ws/daio/start")
async def websocket_endpoint_daio(websocket: WebSocket):
    sample_time = local_config.readLocalConfig().get("CHART_SAMPLE_UPDATE", 1)
    # Accept 
    await websocket.accept()
    try:
        while True:
            messages = {}  # Array to collect messages
            if utils.DAIOChannel.newMessageFlag:
                messages["value"] = utils.DAIOChannel.lastValue
                utils.DAIOChannel.newMessageFlag = False
            # If there are messages, send them as a single array
            if messages:
                # Serialize the dictionary to JSON
                await websocket.send_text(json.dumps(messages))
            await sleep(float(sample_time))
    except WebSocketDisconnect:
        # Handle the disconnect
        print("WebSocket disconnected")
        # Exit the while loop
        return
    except Exception as e:
        print(e)
        print("WebSocket disconnected")
        return
    


import queue
@router.websocket("/ws/start")
async def websocket_endpoint(websocket: WebSocket):
    # Accept 
    sample_time = local_config.readLocalConfig().get("CHART_SAMPLE_UPDATE", 1)
    voltageName = local_config.readLocalConfig().get("VOLTAGE", "voltage")
    voltageID = local_config.readLocalConfig().get("VOLTAGE_MSG_ID", 9999)

    queues = []
    for name in utils.canChannel.keys():
        for element in utils.canChannel[name].propagate.values():
            queues.append(element)

    await websocket.accept()
    try:
        for name in utils.canChannel.keys():
            utils.canChannel[name].traceLog = True
        while True:
            messageDict = {} # Array to collect messages
            for name in utils.canChannel.keys():
                try:
                    item = utils.canChannel[name].messages.get_nowait()
                    messageDict[name] = [item]
                except queue.Empty:
                    continue  # Queue is empty, check the next one
                
            
            if utils.DAIOChannel:
                if utils.DAIOChannel.newMessageFlag:
                    messageDict["DAIO"] = [{voltageID: {voltageName: utils.DAIOChannel.lastValue_raw, "rawMessageValue": utils.DAIOChannel.lastValue_raw}}]
                    utils.DAIOChannel.newMessageFlag = False

            # If there are messages, send them as a single array
            if messageDict:
                await websocket.send_text(json.dumps(messageDict))
            await sleep(float(sample_time))
    except WebSocketDisconnect:
        # Handle the disconnect
        print("WebSocket disconnected")
        for name in utils.canChannel.keys():
            utils.canChannel[name].traceLog = True
        # Exit the while loop
        return

    
'''
@router.websocket("/ws/info/start")
async def websocket_endpoint_info(websocket: WebSocket):

    sample_time = local_config.readLocalConfig().get("CHART_SAMPLE_UPDATE", 1)
    # Accept 
    await websocket.accept()
    try:
        while True:
            messageDict = {} # Array to collect messages

            messageDict["busLoad"] = global_var.g_busLoad
            messageDict["inSleep"] = global_var.g_inSleep
            messageDict["wakeupCounter"] = global_var.g_wakeupCounter

            for name in utils.canChannel.keys():
                for key, lastValue in utils.canChannel[name].lastValue_dict.items():
                    messageDict[key] = lastValue

            if utils.DAIOChannel:       
                messageDict["voltage"] = utils.DAIOChannel.lastValue_raw

            # If there are messages, send them as a single array
            if messageDict:
                await websocket.send_text(json.dumps(messageDict))
            await sleep(float(sample_time))
    except WebSocketDisconnect:
        # Handle the disconnect
        print("WebSocket disconnected")
        # Exit the while loop
        return
    except Exception as e:
        print(traceback.print_exc())
        print("WebSocket disconnected")
        return
'''