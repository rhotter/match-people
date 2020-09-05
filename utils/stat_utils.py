import re
import numpy as np
import pandas as pd
import seaborn as sn

def get_names(names_str, separators=[':','>','+',',']):
  names_str = names_str.replace(" ", "").replace("=","")
  names = re.split(f"[{''.join(separators)}]", names_str)
  names = [name.lower() for name in names]
  return names

def get_pairs_matrix(pairs_data, people, directed=False):
  person_to_index = {person: i for i, person in enumerate(people)}

  pairs_arr = np.zeros((len(people), len(people)))
  for pair, frequency in pairs_data.items():
    idx1 = person_to_index[pair[0]]
    idx2 = person_to_index[pair[1]]
    pairs_arr[idx1, idx2] = frequency
    if not directed:
      pairs_arr[idx2, idx1] = frequency
  return pairs_arr

def plot_pairs_matrix(pairs_arr, people):
  df = pd.DataFrame(pairs_arr, index = [i for i in people],
                    columns = [i for i in people])
  sn.heatmap(df, annot=False, cbar=True, cmap="Purples")

def plot_frequency_histogram(pairs_arr):
  data = np.array([x for x in np.triu(pairs_arr).flatten() if x > 0])
  sn.countplot(x=data)