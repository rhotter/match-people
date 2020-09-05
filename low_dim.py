from utils import get_raw_spreadsheet_data
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, MDS
from settings import personality_personality_spreadsheet_id, personality_personality_spreadsheet_range

import csv


def percent_to_decimal(percent_string):
  decimal = float(percent_string[:-1])/100
  return decimal

def get_processed_data(raw_data):
  # processed_data = {}
  processed_data = []
  for row in raw_data[1:]:
    # name = row[name_col]
    data = [percent_to_decimal(row[j]) for j in data_cols]
    # processed_data[name] = data
    processed_data.append(data)
    
  return np.array(processed _data)

data_cols = [2,3,4,5,6]
name_col = 0

raw_data = get_raw_spreadsheet_data(personality_spreadsheet_id, personality_spreadsheet_range)
processed_data = get_processed_data(raw_data)

# pca = PCA(n_components=2)
# dim_reduced_data = pca.fit_transform(processed_data)

# tsne = TSNE(n_components=2)
# dim_reduced_data = tsne.fit_transform(processed_data)

mds = MDS(n_components=2)
dim_reduced_data = mds.fit_transform(processed_data)

pretty_dim_reduced_data = dim_reduced_data - dim_reduced_data.min(axis=0)
pretty_dim_reduced_data /= pretty_dim_reduced_data.max()

print(dim_reduced_data)
print(pretty_dim_reduced_data)

# fig = plt.figure()
# ax = Axes3D(fig)
# ax.scatter(pretty_dim_reduced_data[:,0],pretty_dim_reduced_data[:,1],pretty_dim_reduced_data[:,2])
# plt.show()
with open("dummy.csv", "w") as f:
  writer = csv.writer(f)
  writer.writerows(pretty_dim_reduced_data)