from igraph import *
import numpy as np
from utils import get_raw_spreadsheet_data, extract_person#, get_pairs_matrix, plot_pairs_matrix
# import matplotlib.pyplot as plt

spreadsheet_id="1Ju7_5GgQQeq0i3STwdjA2VjkzTfe6i_vhgz8pw1ntx8"
spreadsheet_range="Sheet1"
TEACHING_COLS = [1,2,3,4]
COLAB_COLS = [5,6,7]

def build_graph(log=False):
  data = get_raw_spreadsheet_data(spreadsheet_id, spreadsheet_range)

  people_names = set()
  edges = {}
  attendance = {}
  for row in data:
    if len(row) > 0:
      name = row[0]
      people_names.add(name)
      if name in attendance:
        attendance[name] += 1
      else:
        attendance[name] = 1

      # teaching
      for col_idx, col in enumerate([row[i] for i in TEACHING_COLS if i < len(row)]):
        if not log:
          priority = (len(TEACHING_COLS) - col_idx) / len(TEACHING_COLS)
        else:
          priority = np.log(20*(len(TEACHING_COLS) - col_idx) / len(TEACHING_COLS))
        if col != '':
          selected_person = extract_person(col)
          if (name, selected_person) in edges:
            edges[(name, selected_person)] += priority
          else:
            edges[(name, selected_person)] = priority
      
      # colab
      for col_idx, col in enumerate([row[i] for i in COLAB_COLS if i < len(row)]):
        if not log:
          priority = (len(COLAB_COLS) - col_idx) / len(COLAB_COLS)
        else:
          priority = np.log(20*(len(COLAB_COLS) - col_idx) / len(COLAB_COLS))
        if col != '':
          selected_person = extract_person(col)
          if (name, selected_person) in edges:
            edges[(name, selected_person)] += priority
          else:
            edges[(name, selected_person)] = priority

  # build graph
  weighted_edges = [(people[0], people[1], weight) for people, weight in edges.items() if people[0] != people[1]]

  g = Graph.TupleList(weighted_edges, weights=True, directed=True)
  return g


# adjacency_matrix = get_pairs_matrix(edges, people_names, directed=True)
# plot_pairs_matrix(adjacency_matrix, people_names)
# plt.show()
