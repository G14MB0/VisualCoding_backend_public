from asyncio import Queue

runningNodes = {}
notificationQueue = Queue()

async def setRunningNode(id, value=None):
    runningNodes[id] = {"isRunning": "running", "value": value}
    await notificationQueue.put(runningNodes)

async def setStoppingNode(id, value=None):
    runningNodes[id] = {"isRunning": "not running", "value": value}
    await notificationQueue.put(runningNodes)
