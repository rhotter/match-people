import networkx as nx
import matplotlib.pyplot as plt
from utils import *
import time
from itertools import combinations
from math import factorial

def print_time(f, *args):
  print("time for: " + f.__name__)
  start_time = time.time()
  return_val = f(*args)
  print(time.time() - start_time)
  return return_val

spreadsheet_id = '1j7G_PzCfDEn4PDiDlR0hyp180baKbyaThdOxXz9O8HU'
# spreadsheet_range = 'Learning Experiment!A2:E'
spreadsheet_range = 'test!A2:E' # 10 people

data = get_data(spreadsheet_id, spreadsheet_range)

"""
 iterate over combinations of grouping n people into 2 groups
    returns (group1, group2) where each group is a list of people
    for each group:
    build a graph and solve it
  keep track of the minimum cost and its corresponding result
"""

# data = print_time(get_data, spreadsheet_id, spreadsheet_range)

weights = [1, 2, 3, 4, 8]

names = {person['name'] for person in data}
block_size = len(names) // 2

min_cost = None
min_configuration = None

block_combinations = list(combinations(names, block_size))

costs = []
for presenters in block_combinations[: len(block_combinations) // 2]: # first half
  presenters = set(presenters)
  audience = names.difference(presenters)

  graph1 = build_graph(presenters, audience, data, weights)
  mincost_flow = nx.max_flow_min_cost(graph1, 'source', 'sink')
  cost1 = nx.cost_of_flow(graph1, mincost_flow)

  graph2 = build_graph(audience, presenters, data, weights)
  mincost_flow = nx.max_flow_min_cost(graph2, 'source', 'sink')
  cost2 = nx.cost_of_flow(graph2, mincost_flow)

  total_cost = cost1 + cost2

  if min_cost is None or total_cost < min_cost:
    min_cost = total_cost
    min_configuration = (graph1, graph2)
  costs.append(total_cost)
print(min_cost)
print(min_configuration)
# plt.hist(costs, bins=20)
# plt.show()
# plot_graph(graph1)


# print_mincost_flow(mincost_flow)
# print_out(mincost_flow)

# # print(nx.cost_of_flow(G, mincost_flow))

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
