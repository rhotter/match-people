import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import heapq

from utils import get_data, get_generated_data
from solver import TeachingSolver
from settings import spreadsheet_id, spreadsheet_range

data, _ = get_data(spreadsheet_id, spreadsheet_range, cols=[1,2,3,4,5])
# print(data)

people =  ["Marley Xiong",
"Raffi Hotter",
"Felipe Calero Forero",
"Harshu Musunuri",
"Stephen Fay",
"Chris Axon",
"Geffen Avraham",
"Dmitri Brereton",
"Kesava Kiruva Dinakaran",
"Dima Dolgopolov",
"Athena Leong",
"William Bryk",
"Emma Qian",
"Bonnie Li",
"Tiago Sada",
"Vincent Huang",
"Dhruvik Parikh",
"Jonathan Xu",
"Phoebe Yao",
"Noah Trenaman",
"Matt Siu",
"David Holz",
"Azlen Elza",
"Liam Hinzman"]

people.sort()

# df = pd.DataFrame(0, index=names, columns=names)
G = nx.DiGraph()

def complete_name(name):
    for full_name in people:
        if name in full_name:
            return full_name
    else:
        return "ERROR: " + name


for person in data:
    student = complete_name(person["name"])
    teachers = [complete_name(x) for x in person["out"]]
    for priority, teacher in enumerate(teachers):
        G.add_edge(student, teacher, weight=np.log(5+priority))
# nx.draw(G)
# plt.show()
shortest_paths = dict(nx.all_pairs_dijkstra_path_length(G, weight="weight"))

df = pd.DataFrame.from_dict(shortest_paths).transpose()
df = df.fillna(0)

bad_people = []

for full_name in people:
    if full_name not in G.nodes:
        df[full_name] = 0
        df.loc[full_name] = 0
        bad_people.append(full_name)

df = df[people]
df = df.sort_index(ascending=True)

n_people = len(people)
n_bad_people = len(bad_people)


for i in range(n_people):
    row = df.iloc[i]
    row = [1/x if x > 0 else 0 for x in row]
    row = np.array(row)
    if people[i] not in bad_people:
        if "Emma" not in people[i]:
            row = row / np.sum(row) * (n_people-n_bad_people-2)/(n_people-1)
        else:
            row = row / np.sum(row) * (n_people-n_bad_people-1)/(n_people-1)
        c=0.2
        row = [x if x > 0 else c/(n_people-1) for x in row]
        row /= np.sum(row)
    else:
        row = [1/(n_people-1)] * (n_people)
    row[i] = 0
    df.iloc[i] = row
df *= 6
print(df)
df.to_csv("raffi-hotter-submission.csv")

# take top 6
for i in range(n_people):
    row = np.array(df.iloc[i])
    top_n = 6
    idx = np.argpartition(row, -top_n)[-top_n:]
    indices = idx[np.argsort((-row)[idx])]
    print(indices)
    row = [1 if i in indices else 0 for i in range(n_people)]
    df.iloc[i] = row

df.to_csv("raffi-hotter-submission-top6.csv")

# sns.heatmap(df, cmap="YlGnBu")
# plt.show()