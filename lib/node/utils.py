import networkx as nx
import matplotlib.pyplot as plt
import asyncio

from lib import global_var as gv
import time
from lib.node import node as N
from app.routers.pythonBus import utils

# Create a NetworkX graph
G = nx.DiGraph()

# Used as starting points for graph
triggersNode = []


def updateNodesAndEdges(data):
    G.clear()
    gv.pollingNodes = []

    # Add nodes
    for node in data["nodes"]:
        if node["type"] == 'TimerNode' and 'timerInterval' in node["data"]: # or node["type"] == 'trigger':
            print("Add Timer Node")
            if 'loop' in node["data"]:
                temp = N.TimerNode(node['id'], node["data"]['timerInterval'], node["data"]['selected'], node["data"]['loop'])
            else:
                temp = N.TimerNode(node['id'], node["data"]['timerInterval'], node["data"]['selected'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], style=node['style'], obj=temp)
        elif (node["type"] == 'FunctionNode' and 'code' in node["data"]) or (node.get('data', {}).get('type') == 'FunctionNode' and 'code' in node["data"]):
            print("Add Function Node")
            temp = N.FunctionNode(node['id'], node["data"]['code'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], style=node['style'], obj=temp)
            if node.get('data', {}).get('isPolling') == 'true':
                print("Add Polling Node")
                gv.pollingNodes.append(N.PollingNode(node['id'], node['data']['replacementKey']))
        elif node["type"] == 'ComparatorNode' and 'code' in node["data"]:
            print("Add Comparator Node")
            temp = N.ComparatorNode(node['id'], node["data"]['code'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], style=node['style'], obj=temp)
        elif node["type"] == 'DebugNode':
            print("Add Debug Node")
            temp  = N.DebugNode(node['id'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], style=node['style'], obj=temp)
        elif node["type"] == 'SumNode' or node["type"] == 'MultiplyNode' or node["type"] == 'SubtractNode' or node["type"] == 'DivideNode':
            print("Add Muxer Node")
            temp  = N.MuxerNode(node['id'], node['data']['operation'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], style=node['style'], obj=temp)
        elif node["type"] == 'EqualsNode':
            print("Add Equals Node")
            temp  = N.EqualsNode(node['id'], node['data']['logic'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], style=node['style'], obj=temp)
        elif node["type"] == 'OnMessageNode':
            print("Add onMessageNode Node")
            temp  = N.OnMessageNode(node['id'], node['data']['propagatedSignal'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], style=node['style'], obj=temp)
        else:
            print(f"adding a node without object: {node['type']}")
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], style=node['style'])



    # Add edges
    for edge in data["edges"]:
        G.add_edge(edge["source"], edge["target"], sourceHandle=edge['sourceHandle'], targetHandle=edge['targetHandle'])


def plotGraph():
    nx.draw(G, with_labels=True, node_size=2000, node_color="lightblue", font_weight="bold", arrows=True)
    plt.show()  # Display the plot


def getNodesAndEdges():
    nodes = []
    edges = []

    for node in G.nodes:
        nodeData = G.nodes[node]
        nodes.append({
            "id": nodeData['data']['id'],
            'type': nodeData['type'],
            'data': nodeData['data'],
            'position': nodeData['position'],
            'style': nodeData['style']
                      })
    
    for edge in G.edges:
        edges.append({
            'source': edge[0],
            'target':edge[1],
            'type': 'smoothstep',
            'sourceHandle': G.edges[edge]['sourceHandle'],
            'targetHandle': G.edges[edge]['targetHandle'],
        })

    data = {"nodes": nodes, "edges": edges}

    return data


loop = asyncio.get_event_loop()

def runGraph():
    for name in utils.canChannel.keys():
        utils.canChannel[name].propagateLog = True
    # Ensure all nodes are set to run
    for node in G.nodes:
        if 'obj' in G.nodes[node]:
            G.nodes[node]['obj'].run = True
    # Schedule the start_graph_execution coroutine without using asyncio.run
    if not loop.is_running():
        loop.run_until_complete(N.start_graph_execution(G))
    else:
        N.tasks.append(loop.create_task(N.start_graph_execution(G)))


def stopGraph():
    for name in utils.canChannel.keys():
            utils.canChannel[name].propagateLog = False
    for node in G.nodes:
        if 'obj' in G.nodes[node]: 
            print(f"stopping {node}")
            G.nodes[node]['obj'].run = False
    time.sleep(0.5)
    for task in N.tasks:
        if task:
            task.cancel()
    N.tasks = []


