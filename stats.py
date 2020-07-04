import re
from utils import get_raw_spreadsheet_data
from itertools import combinations
import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil

def get_names(names_str, separators=[':','>','+',',']):
  names_str = names_str.replace(" ", "").replace("=","")
  names = re.split(f"[{''.join(separators)}]", names_str)
  names = [name.lower() for name in names]
  return names

spreadsheet_id = '1u286TDoao6ucRdFVLTnNTCD_4UmbuZHPYXHeyN2FN6I'
spreadsheet_range = 'Sheet1'

data = get_raw_spreadsheet_data(spreadsheet_id, spreadsheet_range)
pairs_data = {}
people = set()
for row in data:
  for cell in row:
    names = get_names(cell)
    for person in names:
      people.add(person)
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

def get_pairs_matrix(pairs_data, people):
  person_to_index = {person: i for i, person in enumerate(people)}

  pairs_arr = np.zeros((len(people), len(people)))
  for pair, frequency in pairs_data.items():
    idx1 = person_to_index[pair[0]]
    idx2 = person_to_index[pair[1]]
    pairs_arr[idx1, idx2] = frequency
    pairs_arr[idx2, idx1] = frequency
  return pairs_arr

def plot_pairs_matrix(pairs_arr, people):
  df = pd.DataFrame(pairs_arr, index = [i for i in people],
                    columns = [i for i in people])
  sn.heatmap(df, annot=False, cbar=True, cmap="Purples")

def plot_frequency_histogram(pairs_arr):
  data = np.array([x for x in np.triu(pairs_arr).flatten() if x > 0])
  sn.countplot(x=data)

pairs_arr = get_pairs_matrix(pairs_data, people)
# plot_pairs_matrix(pairs_arr, people)
plot_frequency_histogram(pairs_arr)
plt.show()
# print(sorted_pairs)