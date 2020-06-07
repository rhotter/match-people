from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpStatus, value, LpInteger
from math import ceil
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

class TeachingSolver():
  def __init__(self, data, n_blocks, weights, low_priority_weight, exclude_presenters=[]):
    self.n_people = len(data)
    self.n_blocks = n_blocks
    self.weights = weights
    self.low_priority_weight = low_priority_weight
    self.exclude_presenters = set(exclude_presenters)
    self.index_to_person = {i: data[i]['name'] for i in range(self.n_people)}
    self.person_to_index = {data[i]['name']: i for i in range(self.n_people)}
    self.exclude_presenters_indeces = {self.person_to_index[person_name] for person_name in self.exclude_presenters if person_name in self.person_to_index.keys()}

    self.problem_solved = False
    self.problem = LpProblem("learning-experiment-minimum-cost-schedule", LpMinimize)
    self.x = {(i,j,k): LpVariable(name=f"x[{i},{j},{k}]", cat=LpInteger, lowBound=0, upBound=1) for i in range(self.n_people) for j in self._people_minus({i}, self.exclude_presenters_indeces) for k in range(self.n_blocks)}

    self._add_constraints()
    self._add_objective(data)
  
  def _people_minus(self, *indeces_ignored):
    ignore_set = indeces_ignored[0].union(*indeces_ignored[1:])
    return set(range(self.n_people)).difference(ignore_set)


  def _add_constraints(self):
    # each person listens once in total (except exclude_presenters)
    for i in set(range(self.n_people)).difference(self.exclude_presenters_indeces):
      self.problem += lpSum(self.x[i,j,k] for j in self._people_minus({i}, self.exclude_presenters_indeces) for k in range(self.n_blocks)) == 1

    # each person either presents once or listens once in each block
    for i in set(range(self.n_people)).difference(self.exclude_presenters_indeces):
      for k in range(self.n_blocks):
        present_times = lpSum(self.x[j,i,k] for j in self._people_minus({i}))
        listen_times = lpSum(self.x[i,j,k] for j in self._people_minus({i}, self.exclude_presenters_indeces))
        self.problem += present_times + listen_times >= 1
        self.problem += present_times + 2*listen_times <= 2
    
    # exclude_presenter listens once per block
    for i in self.exclude_presenters_indeces:
      for k in range(self.n_blocks):
        self.problem += lpSum(self.x[i,j,k] for j in self._people_minus({i}, self.exclude_presenters_indeces)) == 1
    
    # each block has exactly n/2 presentations
    for k in range(self.n_blocks):
      self.problem += lpSum(self.x[i,j,k] for i in range(self.n_people) for j in self._people_minus({i}, self.exclude_presenters_indeces)) == ceil(self.n_people/2)
  
  def _get_priority_edges_for_listener(self, listener_idx, out_names):
    priority_edge_costs = {}
    for priority, presenter_name in enumerate(out_names):
      if presenter_name not in self.exclude_presenters:
        presenter_idx = self.person_to_index[presenter_name]
        priority_edge_costs[listener_idx, presenter_idx] = self.weights[priority]
    return priority_edge_costs

  def _get_low_priority_edges_for_listener(self, listener_idx, out_names):
    low_priority_edge_costs = {}
    listener_out_indeces = {self.person_to_index[person_name] for person_name in out_names}
    for presenter_idx in self._people_minus(listener_out_indeces, {listener_idx}):
      low_priority_edge_costs[listener_idx, presenter_idx] = self.low_priority_weight
    return low_priority_edge_costs

  def _get_edge_costs(self, data):
    edge_costs = {}
    for listener in data:
      listener_idx = self.person_to_index[listener['name']]
      priority_edge_costs = self._get_priority_edges_for_listener(listener_idx, listener['out'])
      low_priority_edge_costs = self._get_low_priority_edges_for_listener(listener_idx, listener['out'])
      edge_costs = {**edge_costs, **priority_edge_costs, **low_priority_edge_costs}
    return edge_costs

  def _add_objective(self, data):
    self.edge_costs = self._get_edge_costs(data)
    self.problem += lpSum(self.x[i,j,k]*self.edge_costs[i,j] for i in range(self.n_people) for j in self._people_minus({i}, self.exclude_presenters_indeces) for k in range(self.n_blocks))
  
  def solve(self, print_status=True, print_cost_achieved=True):
    status = self.problem.solve()
    self.problem_solved = True
    print_blank_line = False
    if print_status:
      print(f"Status: {LpStatus[status]}")
      print_blank_line = True
    if print_cost_achieved:
      print(f"Cost: {value(self.problem.objective)}")
      print_blank_line = True
    if print_blank_line:
      print()
  
  def _get_preference(self, i, j):
    # listener i, presenter j
    edge_weight = self.edge_costs[i,j]
    idx = self.weights.index(edge_weight)
    if idx == len(self.weights) - 1:
      preference = None
    else:
      preference = idx + 1
    return preference

  def print_results(self, print_preferences=True):
    if not self.problem_solved:
      raise Exception('Solve the problem first')

    results = [{} for _ in range(self.n_blocks)]
    for key in self.x.keys():
      i,j,k = key
      if int(value(self.x[i,j,k])):
        presenter_name = self.index_to_person[j]
        listener_name = self.index_to_person[i]
        preference = self._get_preference(i,j)
        if presenter_name in results[k].keys():
          results[k][presenter_name] += ", " + str(listener_name)
        else:
          results[k][presenter_name] = str(listener_name)
        
        if print_preferences:
          results[k][presenter_name] += " (" + str(preference) + ")"
    
    for k in range(self.n_blocks):
      print(f"Block {k+1}")
      for presenter, listeners in results[k].items():
        print(f"{presenter} => {listeners}")
      print()