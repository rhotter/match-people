import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def _get_low_priority_edges(presenters, audience, audience_preferences, weights):
  low_priority_weight = weights[-1]
  low_priority_edges = []

  for audience_member in audience_preferences:
    # add people who aren't yourself and who haven't already been selected
    for presenter_name in presenters.difference(set(audience_member["out"])):
      low_priority_edges.append((audience_member['name'], presenter_name, {'capacity': 1, 'weight': low_priority_weight}))
  return low_priority_edges

def _get_cross_edges(presenters, audience, audience_preferences, weights):
  cross_edges = []
  for audience_member in audience_preferences:
    for i, presenter_name in enumerate(audience_member['out']):
      if presenter_name in presenters:
        cross_edges.append((audience_member['name'], presenter_name, {'capacity': 1, 'weight': weights[i]}))
  cross_edges.extend(_get_low_priority_edges(presenters, audience, audience_preferences, weights))
  return cross_edges

def _get_source_edges(audience, group_size):
  return [('source', name, {'capacity': group_size - 1, 'weight': 0}) for name in audience]

def _get_sink_edges(presenters, group_size):
  return [(name, 'sink', {'capacity': group_size - 1, 'weight': 0}) for name in presenters]

def build_graph(presenters, audience, data, weights):
  group_size=2
  
  G = nx.DiGraph() # directed graph

  audience_preferences = [person for person in data if person['name'] in audience]
  
  source_edges = _get_source_edges(audience, group_size)
  sink_edges = _get_sink_edges(presenters, group_size)
  cross_edges = _get_cross_edges(presenters, audience, audience_preferences, weights)
  edges = source_edges + sink_edges + cross_edges

  G.add_edges_from(edges)
  return G