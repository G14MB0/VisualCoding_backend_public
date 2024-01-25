import time
import threading
import asyncio
import re
import traceback

from lib import global_var as gv

# Asyncio tasks
tasks = []



async def execute_successors(graph, node_id, data=None):
    # global tasks
    print(f"task created on {node_id} with data {data}")
    if node_id in graph.nodes:
        if 'obj' in graph.nodes[node_id]:
            node = graph.nodes[node_id]['obj']
            await node.execute(graph, data)  





async def start_graph_execution(graph):
    # Identifica i nodi senza predecessori e avviali in modo asincrono
    initial_nodes = [node for node in graph.nodes if len(list(graph.predecessors(node))) == 0]
    for node_id in initial_nodes:
        gv.runningNodes
        task = asyncio.create_task(execute_successors(graph, node_id))
        tasks.append(task)

     # Now, await all tasks to complete. This is where concurrency happens.
    await asyncio.gather(*tasks)


class Node:
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.run = True
        self.output = None

    def execute(self):
        pass  # To be overridden by subclasses



class FunctionNode(Node):
    """A function Node extend the Node class as a type: "function"
    
    Define also function: function
    """    
    def __init__(self, id, code):
        super().__init__(id, "function")

        # Returns of the funciton
        self.output = None
        self.code = code
        

    async def execute(self, graph, data=None):
        if self.run:
            await gv.setRunningNode(self.id)
            try:
                # Use regular expression to extract the function name
                match = re.search(r'def (\w+)\(', self.code)
                if match:
                    self.function_name = match.group(1)
                else:
                    self.function_name = None
                    print("Function name could not be determined.")

                # Execute the function definition if a name was found
                if self.function_name:
                    exec(self.code, globals())
                    print(f"funciton defined: {self.function_name}")
                    function_ref = globals().get(self.function_name)
                    if function_ref:
                        # Check if the function is a coroutine function
                        if asyncio.iscoroutinefunction(function_ref):
                            # If it is, await it
                            self.output = await function_ref(data) if data else await function_ref()
                        else:
                            # Call the function normally if it's not async
                            self.output = function_ref(data) if data else function_ref()
                    else:
                        print("Function reference not found.")

                
                # Procedi con l'esecuzione dei nodi successori sequenzialmente
                successors = list(graph.successors(self.id))
                await gv.setStoppingNode(self.id)
                for successor in successors:
                    await execute_successors(graph, successor, data=self.output)  

                return
            except:
                await gv.setStoppingNode(self.id)
                print(traceback.print_exc())
                return
                    



class ComparatorNode(Node):
    def __init__(self, id, code):
        super().__init__(id, "comparator")
        # Returns of the funciton
        self.output = 0
        self.code = code


    async def execute(self, graph, data=None):
        if self.run:
            await gv.setRunningNode(self.id)
            try:
                # Use regular expression to extract the function name
                match = re.search(r'def (\w+)\(', self.code)
                if match:
                    self.function_name = match.group(1)
                else:
                    self.function_name = None
                    print("Function name could not be determined.")

                # Execute the function definition if a name was found
                if self.function_name:
                    exec(self.code, globals())
                    print(f"funciton defined: {self.function_name}")
                    function_ref = globals().get(self.function_name)
                    if function_ref:
                        # Check if the function is a coroutine function
                        if asyncio.iscoroutinefunction(function_ref):
                            # If it is, await it
                            self.output = await function_ref(data) if data else await function_ref()
                        else:
                            # Call the function normally if it's not async
                            self.output = function_ref(data) if data else function_ref()
                    else:
                        print("Function reference not found.")

                if self.output == 0:
                    specific_successors = [successor for successor in graph.successors(self.id)
                                        if graph.get_edge_data(self.id, successor)['sourceHandle'] == 'a']
                else:
                    specific_successors = [successor for successor in graph.successors(self.id)
                                        if graph.get_edge_data(self.id, successor)['sourceHandle'] == 'b']

                await gv.setStoppingNode(self.id)
                await execute_successors(graph, specific_successors[0])  

            except:
                await gv.setStoppingNode(self.id)
                print(traceback.print_exc())
                return




class TriggerNode(Node):
    def __init__(self, id, trigger_condition_func, polling):
        super().__init__(id, "trigger")
        self.trigger_condition_func = trigger_condition_func
        self.polling = polling
        self.triggered = False  # This flag will indicate whether the trigger condition has been met

    def check_trigger(self):
        """Check the trigger condition in a loop."""
        while not self.triggered:
            self.triggered = self.trigger_condition_func()
            if not self.triggered:
                time.sleep(self.polling)


    def execute(self, graph, data):
        trigger_thread = threading.Thread(target=self.check_trigger)
        trigger_thread.start()
        trigger_thread.join()  # Wait for the trigger condition to be met
        return self.triggered
    


class TimerNode(Node):
    def __init__(self, id, value, mu, loop=False):
        super().__init__(id, "timer")
        self.value = value
        self.mu = mu
        self.loop = loop


    async def waitTimer(self):
        delay = self.value
        if self.mu == "m":
            delay *= 60
        elif self.mu == "h":
            delay *= 3600
        await asyncio.sleep(delay)
        return


    async def execute(self, graph, data):
        while self.run:
            await gv.setRunningNode(self.id)
            print(f"Starting Timer {self.id}")
            await self.waitTimer()
            print(f"Timer {self.id} finished.")

            # Procedi con l'esecuzione dei nodi successori sequenzialmente
            successors = list(graph.successors(self.id))
            for successor in successors:
                await gv.setStoppingNode(self.id)
                task = asyncio.create_task(execute_successors(graph, successor))
                tasks.append(task)

            
            if not self.loop:
                await gv.setStoppingNode(self.id)
                break
        
        await gv.setStoppingNode(self.id)
        

