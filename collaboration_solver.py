from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpStatus, value, LpInteger

"""
We solve a linear program with 2 constraints:
(1) Each person goes to one topic:
    sum_i [j goes to j's topic] = 1
    for each person i

(2) If your topic is picked, you have to be there (there could be 2 people at your topic): 
    sum_{j≠i}[j goes to i's topic] ≤ 2*[i goes to i's topic]
    for each person i

(3) If you're at your topic, someone else has to be there:
    sum_{j≠i}[j goes to i's topic] ≥ [i goes to i's topic]
    for each person i

(4) There are exactly n_people // 2 presentations:
    sum_i [i goes to i's topic] = n_people // 2
"""

class Solver:
  def __init__(self, data, weights, dont_want_my_topic_weight, dont_want_someone_else_topic_weight):
    self.n_people = len(data)
    self.weights = weights
    self.dont_want_my_topic_weight = dont_want_my_topic_weight
    self.dont_want_someone_else_topic_weight = dont_want_someone_else_topic_weight
    self.problem_solved = False

    self.problem = LpProblem("learning-experiment-minimum-cost-schedule", LpMinimize)
    self.x = {(i,j): LpVariable(name=f"x[{i},{j}]", cat=LpInteger, lowBound=0, upBound=1) for i in range(self.n_people) for j in range(self.n_people)}
    
    self.index_to_person = {i: data[i]['name'] for i in range(self.n_people)}
    self.person_to_index = {data[i]['name']: i for i in range(self.n_people)}

    self._add_constraints()
    self._add_objective(data)
  
  def _add_constraints(self):
    # each person goes to one topic
    for i in range(self.n_people):
      self.problem += lpSum(self.x[i,j] for j in set(range(self.n_people))) == 1

    # if your topic is picked, you have to be there
    for i in range(self.n_people):
      self.problem += lpSum(self.x[j,i] for j in set(range(self.n_people)).difference(set({i}))) <= 2*self.x[i,i]
    
    # if you're at your topic, someone else has to be there
    for i in range(self.n_people):
      self.problem += lpSum(self.x[j,i] for j in set(range(self.n_people)).difference(set({i}))) >= self.x[i,i]
    
    # there are exactly n_people // 2 presentations
    self.problem += lpSum(self.x[i,i] for i in range(self.n_people)) == self.n_people // 2
    
  def _get_edge_costs(self, data):
    edge_costs = {}
    low_priority_weight = self.weights[-1]
    for listener in data:
      listener_idx = self.person_to_index[listener['name']]
      for priority, presenter_name in enumerate(listener['out']):
        presenter_idx = self.person_to_index[presenter_name]
        edge_costs[listener_idx, presenter_idx] = self.weights[priority]
      listener_out_indeces = [self.person_to_index[person_name] for person_name in listener['out']]
      for presenter_idx in set(range(self.n_people)).difference(set(listener_out_indeces)):
        if presenter_idx == listener_idx:
          edge_costs[listener_idx, presenter_idx] = self.dont_want_my_topic_weight
        else:
          edge_costs[listener_idx, presenter_idx] = self.dont_want_someone_else_topic_weight
    return edge_costs

  def _add_objective(self, data):
    self.edge_costs = self._get_edge_costs(data)
    self.problem += lpSum(self.x[i,j]*self.edge_costs[i,j] for i in range(self.n_people) for j in range(self.n_people))
  
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
    if edge_weight == self.dont_want_my_topic_weight or edge_weight == self.dont_want_someone_else_topic_weight:
      preference = None
    else:
      preference = self.weights.index(edge_weight) + 1
    return preference

  def print_results(self):
    if not self.problem_solved:
      raise Exception('Solve the problem first')

    talks = {}
    for key in self.x.keys():
      i,j = key
      if int(value(self.x[i,j])):
        listener_name = self.index_to_person[i]
        presenter_name = self.index_to_person[j]
        preference = self._get_preference(i,j)
        if presenter_name in talks.keys():
          talks[presenter_name] += ", " + listener_name + " (" + str(preference) + ")"
        else:
          talks[presenter_name] = listener_name + " (" + str(preference) + ")"
    
    for presenter, listeners in talks.items():
      print(f"{presenter}: {listeners}")