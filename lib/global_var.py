from asyncio import Queue
from lib.node.node import PollingNode

runningNodes = {}
notificationQueue = Queue()


globalVarDict = {}
globalVarQueue = Queue()


pollingNodes = []

async def setRunningNode(id, value=None):
    runningNodes[id] = {"isRunning": "running", "value": value}
    await notificationQueue.put(runningNodes)

async def setStoppingNode(id, value=None):
    runningNodes[id] = {"isRunning": "not running", "value": value}
    await notificationQueue.put(runningNodes)


async def putGlobalValue(value):
    await globalVarQueue.put(value)
    await PollingNode.broadcast(value)