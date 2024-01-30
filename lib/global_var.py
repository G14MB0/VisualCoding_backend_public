from asyncio import Queue
from lib.node.node import PollingNode
from datetime import datetime
from lib import local_config

g_wakeupCounter = 0
g_inSleep = 0
g_busLoad = 0
 

local_config.readLocalConfig()

runningNodes = {}
notificationQueue = Queue()


globalVarDict = {}
globalVarQueue = Queue()


pollingNodes = []

async def setRunningNode(id, value=None):
    current_time = datetime.now()
    delta = None
    if id in runningNodes and 'timestamp' in runningNodes:
        delta = (current_time - datetime.fromisoformat(runningNodes[id]['timestamp'])).total_seconds()* 1_000_000
    
    data = {
        "value": value,
        "timestamp": current_time.isoformat(),
        "delta": delta
    }
    runningNodes[id] = {"isRunning": "running", "value": data, "timestamp": datetime.now().isoformat()}
    await notificationQueue.put(runningNodes)

async def setStoppingNode(id, value=None):
    current_time = datetime.now()
    delta = None
    if id in runningNodes and 'timestamp' in runningNodes:
        delta = (current_time - datetime.fromisoformat(runningNodes[id]['timestamp'])).total_seconds()* 1_000_000
    
    data = {
        "value": value,
        "timestamp": current_time.isoformat(),
        "delta": delta
    }
    runningNodes[id] = {"isRunning": "not running", "value": data}
    await notificationQueue.put(runningNodes)


async def putGlobalValue(value):
    await globalVarQueue.put(value)
    await PollingNode.broadcast(value)