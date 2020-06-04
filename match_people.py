from utils import get_data, get_generated_data
from solver import Solver

spreadsheet_id = '1j7G_PzCfDEn4PDiDlR0hyp180baKbyaThdOxXz9O8HU'
# spreadsheet_range = 'Learning Experiment!A2:E'
spreadsheet_range = 'test!A2:E' # 10 people

data = get_data(spreadsheet_id, spreadsheet_range)
# data = get_generated_data(n_people=50, n_preferences=4)

weights = [1, 2, 3, 4, 8]
n_blocks = 2

solver = Solver(data, n_blocks, weights)
solver.solve()
solver.print_results()