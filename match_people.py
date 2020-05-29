import networkx as nx
import matplotlib.pyplot as plt
from utils import *

G = nx.DiGraph() # directed graph

# data = [
#   {'name': 'Raffi',
#   'out': ['Santi', 'Erin'] # in priority ordering
#   },
#   {'name': 'Santi',
#   'out': ['Raffi', 'Marley'],
#   },
#   {'name': 'Marley',
#   'out': ['Santi', 'Erin']
#   },
#   {'name': 'Erin',
#   'out': ['Raffi', 'Marley']
#   }]
# optimal grouping is (Marley, Santi, Erin), (Raffi, Erin, Santi), (Erin, Raffi, Marley), (Santi, Raffi, Marley)

spreadsheet_id = '1j7G_PzCfDEn4PDiDlR0hyp180baKbyaThdOxXz9O8HU'
spreadsheet_range = 'Learning Experiment!A2:E'

data = get_data(spreadsheet_id, spreadsheet_range)
# print(data)

weights = [1, 2, 3, 4, 8] # TODO use [1,2,3,4,8] weights instead
group_size=3

edges = get_edges(data, weights, group_size)
G.add_edges_from(edges)
# print(edges)
mincost_flow = nx.max_flow_min_cost(G, 'source', 'sink')
# print(mincost_flow)
print_mincost_flow(mincost_flow)

# # print(nx.cost_of_flow(G, mincost_flow))

# plot_graph(data, G)