from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpStatus, value, LpInteger

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

class Solver:
  def __init__(self, data, n_blocks, weights):
    self.n_people = len(data)
    self.n_blocks = n_blocks
    self.weights = weights
    self.problem_solved = False

    self.problem = LpProblem("learning-experiment-minimum-cost-schedule", LpMinimize)
    self.x = {(i,j,k): LpVariable(name=f"x[{i},{j},{k}]", cat=LpInteger, lowBound=0, upBound=1) for i in range(self.n_people) for j in set(range(self.n_people)).difference(set({i})) for k in range(self.n_blocks)} # continuous variables by default
    
    self.index_to_person = {i: data[i]['name'] for i in range(self.n_people)}
    self.person_to_index = {data[i]['name']: i for i in range(self.n_people)}

    self._add_constraints()
    self._add_objective(data)
  
  def _add_constraints(self):
    # each person listens once in total
    for i in range(self.n_people):
      self.problem += lpSum(self.x[i,j,k] for j in set(range(self.n_people)).difference(set({i})) for k in range(self.n_blocks)) == 1
    
    # each person either presents once or listens once in each block
    for i in range(self.n_people):
      for k in range(self.n_blocks):
        self.problem += lpSum(self.x[i,j,k] + self.x[j,i,k] for j in set(range(self.n_people)).difference(set({i}))) == 1

    # each block has exactly n/2 presentations
    for k in range(self.n_blocks):
      self.problem += lpSum(self.x[i,j,k] for i in range(self.n_people) for j in set(range(self.n_people)).difference(set({i}))) == self.n_people // 2
    
  def _get_edge_costs(self, data):
    edge_costs = {}
    low_priority_weight = self.weights[-1]
    for listener in data:
      listener_idx = self.person_to_index[listener['name']]
      for priority, presenter_name in enumerate(listener['out']):
        presenter_idx = self.person_to_index[presenter_name]
        edge_costs[listener_idx, presenter_idx] = self.weights[priority]
      listener_out_indeces = [self.person_to_index[person_name] for person_name in listener['out']]
      for presenter_idx in set(range(self.n_people)).difference(set(listener_out_indeces)).difference(set({listener_idx})):
        edge_costs[listener_idx, presenter_idx] = low_priority_weight
    return edge_costs

  def _add_objective(self, data):
    self.edge_costs = self._get_edge_costs(data)
    self.problem += lpSum(self.x[i,j,k]*self.edge_costs[i,j] for i in range(self.n_people) for j in set(range(self.n_people)).difference(set({i})) for k in range(self.n_blocks))
  
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

    results = [[] for _ in range(self.n_blocks)]
    for key in self.x.keys():
      i,j,k = key
      if int(value(self.x[i,j,k])):
        presenter_name = self.index_to_person[j]
        listener_name = self.index_to_person[i]
        preference = self._get_preference(i,j)
        results[k].append({"presenter": presenter_name, "listener": listener_name, "preference": preference})
    
    for k in range(self.n_blocks):
      print(f"Block {k+1}")
      for presentation in results[k]:
        to_print = f"{presentation['presenter']} => {presentation['listener']}"
        if print_preferences:
          to_print += f" ({presentation['preference']})"
        print(to_print)
      print()