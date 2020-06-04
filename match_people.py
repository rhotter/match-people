import matplotlib.pyplot as plt
from utils import *
import time
from itertools import combinations
from math import factorial
from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpStatus, value, LpInteger
import numpy as np

def print_time(f, *args):
  print("time for: " + f.__name__)
  start_time = time.time()
  return_val = f(*args)
  print(time.time() - start_time)
  return return_val

def add_constraints(problem, x, n_people, n_blocks):
  # each person listens once in total
  for i in range(n_people):
    problem += lpSum(x[i,j,k] for j in set(range(n_people)).difference(set({i})) for k in range(n_blocks)) == 1
  
  # each person either presents once or listens once in each block
  for i in range(n_people):
    for k in range(n_blocks):
      problem += lpSum(x[i,j,k] + x[j,i,k] for j in set(range(n_people)).difference(set({i}))) == 1

  # each block has exactly n/2 presentations
  for k in range(n_blocks):
    problem += lpSum(x[i,j,k] for i in range(n_people) for j in set(range(n_people)).difference(set({i}))) == n_people // 2
  
  return problem

def get_edge_costs(data, weights, n_people, n_blocks):
  edge_costs = {}
  low_priority_weight = weights[-1]
  for listener in data:
    listener_idx = person_to_index[listener['name']]
    for priority, presenter_name in enumerate(listener['out']):
      presenter_idx = person_to_index[presenter_name]
      edge_costs[listener_idx, presenter_idx] = weights[priority]
    listener_out_indeces = [person_to_index[person_name] for person_name in listener['out']]
    for presenter_idx in set(range(n_people)).difference(set(listener_out_indeces)).difference(set({listener_idx})):
      edge_costs[listener_idx, presenter_idx] = low_priority_weight
  return edge_costs

def add_objective(problem, x, data, weights, n_people, n_blocks):
  edge_costs = get_edge_costs(data, weights, n_people, n_blocks)
  # for key, val in edge_costs.items():
  #   i,j = key
  #   print(f"{index_to_person[i]} listening to {index_to_person[j]} has value {val}")
  problem += lpSum(x[i,j,k]*edge_costs[i,j] for i in range(n_people) for j in set(range(n_people)).difference(set({i})) for k in range(n_blocks))
  return problem

"""
We solve a linear program with 3 constraints:
(1) Each person listens once:
    sum_{j,k} [i listens to j at block k] = 1
    for each person i

(2) Each person presents or listens exactly once per block: 
    sum_{j}[i listens to j at block k] + sum{j}[j listens to i at block k] = 1
    for each person i and each block k

(3) Each block has exactly n/2 presentations:
    sum_{i,j}[i listens to j at block k] = n/2

"""

spreadsheet_id = '1j7G_PzCfDEn4PDiDlR0hyp180baKbyaThdOxXz9O8HU'
# spreadsheet_range = 'Learning Experiment!A2:E'
spreadsheet_range = 'test!A2:E' # 10 people

results = {}
# data = get_data(spreadsheet_id, spreadsheet_range)
q_range = 5*[10*q for q in range(1,10)]
for q in q_range:#,40,60,80,100]:
  data = get_generated_data(n_people=q, n_preferences=4)

  weights = [1, 2, 3, 4, 8]
  # weights = [x**2 for x in range(1,6)]

  names = {person['name'] for person in data}
  n_people = len(names)
  n_blocks = 2
  block_size = n_people // n_blocks

  x = {(i,j,k): LpVariable(name=f"x[{i},{j},{k}]", cat=LpInteger, lowBound=0, upBound=1) for i in range(n_people) for j in set(range(n_people)).difference(set({i})) for k in range(n_blocks)} # continuous variables by default
  problem = LpProblem("learning-experiment-minimum-cost-schedule", LpMinimize)

  index_to_person = {i: data[i]['name'] for i in range(n_people)}
  person_to_index = {data[i]['name']: i for i in range(n_people)}

  problem = print_time(add_constraints,problem, x, n_people, n_blocks)
  problem = print_time(add_objective,problem, x, data, weights, n_people, n_blocks)
  status = print_time(problem.solve)

  # print(LpStatus[status])
  # print(value(problem.objective))
  print(value(problem.objective)/n_people)
  if q in results.keys():
    results[q].append(value(problem.objective)/n_people)
  else:
    results[q] = [value(problem.objective)/n_people]

x = []
mean = []
std = []
for key, val in results.items():
  x.append(key)
  mean.append(np.mean(val))
  std.append(np.std(val))

plt.errorbar(x, mean, std, linestyle='None', marker='^')
plt.xlabel('Number of people')
plt.ylabel('Average preference achieved')
plt.show()
  # # how many people got their choices
  # edge_costs = get_edge_costs(data, weights, n_people, n_blocks)
  # priorities = {w: 0 for w in weights}
  # for i in range(n_people):
  #   for j in set(range(n_people)).difference(set({i})):
  #     for k in range(n_blocks):
  #       priorities[edge_costs[i,j]] += value(x[i,j,k])
  # for key in priorities.keys():
  #   priorities[key] *= 100/n_people # in percentage
  # print(priorities)
      
# for key in x.keys():
#   i,j,k = key
#   print(value(x[i,j,k]))

# for key in x.keys():
#   i,j,k = key
#   if int(value(x[i,j,k])):
#     presenter_name = index_to_person[j]
#     listener_name = index_to_person[i]
#     print(f"{presenter_name} presents to {listener_name} in round {k}")


# data = [
#   {'name': 'Raffi',
#   'out': ['Santi', 'Erin'] # in priority ordering
#   },
#   {'name': 'Santi',
#   'out': ['Raffi', 'Marley'],
#   },
#   {'name': 'Marley',
#   'out': ['Santi', 'Erin']
#   },
#   {'name': 'Erin',
#   'out': ['Raffi', 'Marley']
#   }]
# optimal grouping is (Marley, Santi, Erin), (Raffi, Erin, Santi), (Erin, Raffi, Marley), (Santi, Raffi, Marley)
