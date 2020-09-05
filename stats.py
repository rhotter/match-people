import re
from utils import get_raw_spreadsheet_data, get_names, get_pairs_matrix, plot_pairs_matrix, plot_frequency_histogram
from itertools import combinations
import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil
from sklearn.cluster import SpectralClustering

if __name__ == "__main__":
  spreadsheet_id = '1u286TDoao6ucRdFVLTnNTCD_4UmbuZHPYXHeyN2FN6I'
  spreadsheet_range = 'Sheet1'
  min_count = 5

  data = get_raw_spreadsheet_data(spreadsheet_id, spreadsheet_range)
  data = [x[0] for x in data if len(x)>0] # keep only first column

  person_count = {}
  pairs_data = {}
  people = set()
  for cell in data:
    names = get_names(cell)
    for person in names:
      if person in person_count.keys():
        person_count[person] += 1
      else:
        person_count[person] = 1
  
  for person, count in person_count.items():
    if count >= min_count:
      people.add(person)

  print(people)
  for cell in data:
    names = get_names(cell)
    invalid_person = False
    for person in names:
      if person not in people:
        invalid_person = True
        break
    if not invalid_person:
      names_combs = combinations(names,2) # works for 3 tuples
      for pair in names_combs:
        pair = list(pair)
        pair.sort()
        pair = tuple(pair)
        if pair not in pairs_data.keys():
          pairs_data[pair] = 1
        else:
          pairs_data[pair] += 1
  sorted_pairs = {k: v for k, v in sorted(pairs_data.items(), key=lambda item: item[1])}
  print(sorted_pairs)

  adjacency_matrix = np.array(get_pairs_matrix(pairs_data, people))
  n_clusters=4

  clustering = SpectralClustering(n_clusters=n_clusters, affinity="precomputed").fit_predict(adjacency_matrix)
  
  clusters = [[] for _ in range(n_clusters)]
  for x, person in zip(clustering, people):
    clusters[x].append(person)
  for i, cluster in enumerate(clusters):
    print("")
    print(f"Cluster {i+1}")
    for person in cluster:
      print(person)
    

  print("")
  print(clustering)

  shifted_adjacency_matrix = []
  shifted_people = []
  people_list = [i for i in people]
  for cluster in clusters:
    for person in cluster:
      shifted_adjacency_matrix.append(adjacency_matrix[people_list.index(person)])
      shifted_people.append(person)
  
  shifted_adjacency_matrix2 = []
  shifted_adjacency_matrix = np.array(shifted_adjacency_matrix).T
  for cluster in clusters:
    for person in cluster:
      shifted_adjacency_matrix2.append(shifted_adjacency_matrix[people_list.index(person)])

  # print([(i,person) for i, person in enumerate(people)])

  
  plot_pairs_matrix(shifted_adjacency_matrix2, shifted_people)
  
  # plot_pairs_matrix(adjacency_matrix, people)
  # plot_frequency_histogram(pairs_arr)
  plt.show()
  # print(sorted_pairs)