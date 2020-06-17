from utils import get_data, get_generated_data
from solver import TeachingSolver

spreadsheet_id = '1XYBChvlu-X218ZYkVJtTh7o0Vb0Y4vPQRsZVcnUuqF4'
spreadsheet_range = 'Learning Experiment! Episode 3'

data = get_data(spreadsheet_id, spreadsheet_range, cols=[1,2,3,4])
# data = get_generated_data(n_people=11, n_preferences=4)

weights = [1, 2, 3, 4]
low_priority_weight = 8
n_blocks = 2

solver = TeachingSolver(data, n_blocks, weights, low_priority_weight)
solver.solve()
solver.print_results(print_preferences=False)