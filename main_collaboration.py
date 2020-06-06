from utils import get_data, get_generated_data
# from solver import Solver
from collaboration_solver import Solver

spreadsheet_id = '1wqk7ZYDw_R2VFOsZCWIvK0CiID-2OBzKyDUGPzaJfO0'
# spreadsheet_range = 'Learning Experiment!A2:E'
spreadsheet_range = 'Learning Experiment! Episode 2' # 10 people

# data = get_data(spreadsheet_id, spreadsheet_range, cols=[1,2,3,4])
data = get_data(spreadsheet_id, spreadsheet_range, cols=[5,6,7])
# print(data)
# data = get_generated_data(n_people=50, n_preferences=4)


weights = [1, 2, 3]
dont_want_my_topic_weight = 4
dont_want_someone_else_topic_weight = 8

# weights = [1, 2, 3, 4, 8]
# n_blocks = 2

solver = Solver(data, weights, dont_want_my_topic_weight, dont_want_someone_else_topic_weight)
# solver = Solver(data, n_blocks, weights)
solver.solve()
solver.print_results()