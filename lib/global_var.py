from asyncio import Queue

runningNodes = {}
notificationQueue = Queue()

async def setRunningNode(id):
    runningNodes[id] = "running"
    await notificationQueue.put(runningNodes)

async def setStoppingNode(id):
    runningNodes[id] = "not running"
    await notificationQueue.put(runningNodes)
