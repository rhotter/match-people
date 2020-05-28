import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

max_noise = 1e-5

def in_node(name):
  return 'in-' + name

def out_node(name):
  return 'out-' + name

def _get_low_priority_edges(data, weights, random_noise=True):
  low_priority_weight = -weights[-1]
  low_priority_edges = []

  people_names = {person["name"] for person in data}
  for person in data:
    in_name = person["name"]

    # add people who aren't yourself and who haven't already been selected
    for out_name in people_names.difference(set(person["out"])).difference({in_name}):
      weight = low_priority_weight
      if random_noise:
        weight += random.uniform(-max_noise, +max_noise) # perturb weights slightly to get a unique solution
      low_priority_edges.append((in_node(in_name), out_node(out_name), {'capacity': 1, 'weight': weight}))
  return low_priority_edges

def _get_cross_edges(data, weights, random_noise=True):
  # TODO add custom weights
  cross_edges = []
  for person in data:
    for i, out_person_name in enumerate(person['out']):
      weight = -weights[i]
      if random_noise:
        weight += random.uniform(-max_noise, +max_noise) # perturb weights slightly to get a unique solution
      cross_edges.append((in_node(person['name']), out_node(out_person_name), {'capacity': 1, 'weight': weight}))
  cross_edges.extend(_get_low_priority_edges(data, weights, random_noise=True))
  return cross_edges

def _get_source_edges(data, group_size):
  return [('source', in_node(person['name']), {'capacity': group_size - 1, 'weight': 0}) for person in data]

def _get_sink_edges(data, group_size):
  return [(out_node(person['name']), 'sink', {'capacity': group_size - 1, 'weight': 0}) for person in data]

def get_edges(data, weights, group_size):
  source_edges = _get_source_edges(data, group_size)
  sink_edges = _get_sink_edges(data, group_size)
  cross_edges = _get_cross_edges(data, weights, random_noise=True)
  edges = source_edges + sink_edges + cross_edges
  return edges

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
  edge_colors[edge_colors == low_priority_weight] = 1/50

  return edge_colors

def plot_graph(data, graph):
  pos = _get_plot_positions(data)
  labels = _get_plot_labels(data)
  edge_colors = _get_edge_colors(graph)
  
  nx.draw_networkx_nodes(graph, pos=pos, node_color='#ffe28a')
  nx.draw_networkx_edges(graph, pos=pos, edge_color=edge_colors, edge_cmap=plt.cm.GnBu, edge_vmin=-0.1)
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