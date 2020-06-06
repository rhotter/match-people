from utils import get_data, get_generated_data
from teaching_solver import Solver

spreadsheet_id = '1wqk7ZYDw_R2VFOsZCWIvK0CiID-2OBzKyDUGPzaJfO0'
spreadsheet_range = 'Teaching'

data = get_data(spreadsheet_id, spreadsheet_range, cols=[1,2,3,4])
# data = get_generated_data(n_people=11, n_preferences=4)

weights = [1, 2, 3, 4, 8]
n_blocks = 2

solver = Solver(data, n_blocks, weights, exclude_presenters=['Raffi'])
# solver = Solver(data, n_blocks, weights, exclude_presenters=[0])
solver.solve()
solver.print_results()