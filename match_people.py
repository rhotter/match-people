import networkx as nx
import matplotlib.pyplot as plt
from helpers import *

G = nx.DiGraph() # directed graph

data = [
  {'name': 'Raffi',
  'out': ['Santi', 'Erin'] # in priority ordering
  },
  {'name': 'Santi',
  'out': ['Raffi', 'Marley'],
  },
  {'name': 'Marley',
  'out': ['Santi', 'Erin']
  },
  {'name': 'Erin',
  'out': ['Raffi', 'Marley']
  }]
# optimal grouping is (Marley, Santi, Erin), (Raffi, Erin, Santi), (Erin, Raffi, Marley), (Santi, Raffi, Marley)

weights = [1, 1/2, 1/4]
group_size=3

edges = get_edges(data, weights, group_size)
G.add_edges_from(edges)

mincost_flow = nx.max_flow_min_cost(G, 'source', 'sink')
print_mincost_flow(mincost_flow)


# print(nx.cost_of_flow(G, mincost_flow))

# plot_graph(data, G)
