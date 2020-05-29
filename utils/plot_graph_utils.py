import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from .general_utils import in_node, out_node

max_noise = 1e-5

def _get_plot_positions(data):
  pos = {}
  pos['source'] = (1, len(data)//2)
  for i, person in enumerate(data):
    pos[in_node(person['name'])] = (2, i)
    pos[out_node(person['name'])] = (3, i)
  pos['sink'] = (4, len(data)//2)
  return pos

def _get_plot_labels(data):
  labels = {
    'source': 's',
    'sink': 't',
  }
  for person in data:
    name = person["name"]
    labels[in_node(name)] = name[0]
    labels[out_node(name)] = name[0]
  return labels

def _get_edge_colors(graph):
  edge_colors = np.array([-edge[1] for edge in nx.get_edge_attributes(graph,'weight').items()])
  low_priority_weight = np.unique(edge_colors)[1]
  edge_colors[(low_priority_weight + 1e-4 > edge_colors) & (edge_colors > low_priority_weight - 1e-4)] = 0 # TODO pass weights as function arg instead of this shananigans

  return edge_colors

def plot_graph(data, graph):
  pos = _get_plot_positions(data)
  labels = _get_plot_labels(data)
  edge_colors = _get_edge_colors(graph)
  
  nx.draw_networkx_nodes(graph, pos=pos, node_color='#ffe28a')
  nx.draw_networkx_edges(graph, pos=pos, edge_color=edge_colors, edge_cmap=plt.cm.GnBu, edge_vmin=0)
  nx.draw_networkx_labels(graph, pos=pos, labels=labels)

  plt.show()

def print_mincost_flow(mincost_flow):
  print()
  for key, value in mincost_flow.items():
    if 'in-' in key[:len('in-')+1]:
      in_name = key[len('in-'):]
      out_names = []
      for name, is_chosen in value.items():
        if is_chosen:
          out_names.append(name[len('out-'):])
      out_names = ' and '.join(out_names)
      print(f"{in_name} is paired with {out_names}")
  print()