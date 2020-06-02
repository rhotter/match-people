import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from .general_utils import in_node, out_node

max_noise = 1e-5

def _get_plot_positions(graph):
  pos = {}
  middle = len(list(graph.edges('source')))//2
  pos['source'] = (1, middle)

  for i, edge in enumerate(graph.edges('source')):
    audience_name = edge[1]
    pos[audience_name] = (2, i)
  
  for i, edge in enumerate(graph.in_edges('sink')):
    presenter_name = edge[0]
    pos[presenter_name] = (3, i)
  pos['sink'] = (4, middle)
  return pos

def _get_plot_labels(graph):
  labels = {}
  for node in graph.nodes():
    labels[node] = node[:2]  # taking the first 2 characters
  return labels

def _get_edge_colors(graph):
  edge_colors = np.array([edge[1] for edge in nx.get_edge_attributes(graph,'weight').items()])
  low_priority_weight = np.unique(edge_colors)[1]
  edge_colors[(low_priority_weight + 1e-4 > edge_colors) & (edge_colors > low_priority_weight - 1e-4)] = 0 # TODO pass weights as function arg instead of this shananigans

  return edge_colors

def plot_graph(graph):
  graph.edges('source')

  pos = _get_plot_positions(graph)
  labels = _get_plot_labels(graph)
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

def print_out(mincost_flow):
  print()
  presenters = {}
  for key, value in mincost_flow.items():
    if 'in-' in key[:len('in-')+1]:
      in_name = key[len('in-'):]
      for name, is_chosen in value.items():
        if is_chosen:
          person_chosen = name[len('out-'):]
          if person_chosen in presenters.keys():
            presenters[person_chosen].append(in_name)
          else:
            presenters[person_chosen] = [in_name]
  for presenter, audience in presenters.items():
    audience_string = ' and '.join(audience)
    print(f"{presenter} is presenting to {audience_string}")
  print()