from utils import get_data, get_generated_data
from solver import TeachingSolver

spreadsheet_id = '1wqk7ZYDw_R2VFOsZCWIvK0CiID-2OBzKyDUGPzaJfO0'
# spreadsheet_range = 'Teaching'
spreadsheet_range = 'w/o Wilfred'

data = get_data(spreadsheet_id, spreadsheet_range, cols=[1,2,3,4])
print(data)
# data = get_generated_data(n_people=11, n_preferences=4)

weights = [1, 2, 3, 4]
low_priority_weight = 8
n_blocks = 2

solver = TeachingSolver(data, n_blocks, weights, low_priority_weight)
solver.solve()
solver.print_results()