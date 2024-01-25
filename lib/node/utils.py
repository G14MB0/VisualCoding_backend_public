import networkx as nx
import matplotlib.pyplot as plt
import asyncio

from lib.node import node as N

# Create a NetworkX graph
G = nx.DiGraph()

# Used as starting points for graph
triggersNode = []


def updateNodesAndEdges(data):
    G.clear()

    # Add nodes
    for node in data["nodes"]:
        if node["type"] == 'TimerNode' and 'timerInterval' in node["data"]: # or node["type"] == 'trigger':
            print("Add Timer Node")
            if 'loop' in node["data"]:
                temp = N.TimerNode(node['id'], node["data"]['timerInterval'], node["data"]['selected'], node["data"]['loop'])
            else:
                temp = N.TimerNode(node['id'], node["data"]['timerInterval'], node["data"]['selected'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], obj=temp)
        elif node["type"] == 'FunctionNode' and 'code' in node["data"]:
            print("Add Function Node")
            temp = N.FunctionNode(node['id'], node["data"]['code'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], obj=temp)
        elif node["type"] == 'ComparatorNode' and 'code' in node["data"]:
            print("Add Comparator Node")
            temp = N.ComparatorNode(node['id'], node["data"]['code'])
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'], obj=temp)
        else:
            G.add_node(node["id"], type=node["type"], data=node["data"], position=node['position'])



    # Add edges
    for edge in data["edges"]:
        G.add_edge(edge["source"], edge["target"], sourceHandle=edge['sourceHandle'])


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
            'position': nodeData['position']
                      })
    
    for edge in G.edges:
        edges.append({
            'source': edge[0],
            'target':edge[1],
            'type': 'smoothstep',
            'sourceHandle': G.edges[edge]['sourceHandle']
        })

    data = {"nodes": nodes, "edges": edges}

    return data


loop = asyncio.get_event_loop()

def runGraph():
    # Ensure all nodes are set to run
    for node in G.nodes:
        G.nodes[node]['obj'].run = True
    # Schedule the start_graph_execution coroutine without using asyncio.run
    if not loop.is_running():
        loop.run_until_complete(N.start_graph_execution(G))
    else:
        N.tasks.append(loop.create_task(N.start_graph_execution(G)))


def stopGraph():
    for node in G.nodes:
        G.nodes[node]['obj'].run = False
    # for task in N.tasks:
    #     if task:
    #         task.cancel()
    N.tasks = []


