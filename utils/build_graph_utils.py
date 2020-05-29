import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random
from .general_utils import in_node, out_node

max_noise = 1e-5

def _get_low_priority_edges(data, weights, random_noise=True):
  low_priority_weight = weights[-1]
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
  cross_edges = []
  for person in data:
    for i, out_person_name in enumerate(person['out']):
      if out_person_name != '':
        weight = weights[i]
        if random_noise:
          weight += random.uniform(-max_noise, +max_noise) # perturb weights slightly to get a unique solution
        cross_edges.append((in_node(person['name']), out_node(out_person_name), {'capacity': 1, 'weight': weight}))
  cross_edges.extend(_get_low_priority_edges(data, weights, random_noise))
  return cross_edges

def _get_source_edges(data, group_size):
  return [('source', in_node(person['name']), {'capacity': group_size - 1, 'weight': 0}) for person in data]

def _get_sink_edges(data, group_size):
  return [(out_node(person['name']), 'sink', {'capacity': group_size - 1, 'weight': 0}) for person in data]

def get_edges(data, weights, group_size):
  source_edges = _get_source_edges(data, group_size)
  sink_edges = _get_sink_edges(data, group_size)
  cross_edges = _get_cross_edges(data, weights, random_noise=False)
  edges = source_edges + sink_edges + cross_edges
  return edges
