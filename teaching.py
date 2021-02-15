from utils import get_data
from solver import TeachingSolver
from settings import spreadsheet_id, spreadsheet_range

data, people_to_topics = get_data(spreadsheet_id, spreadsheet_range, cols=[1,2,3,4,5])

weights = [1, 2, 3, 4]
low_priority_weight = 10

n_blocks = 2 # currently supports only 2 blocks but passing it into the function anyways...

solver = TeachingSolver(data, n_blocks, weights, low_priority_weight, exclude_presenters=["Jonathan"])
solver.solve()

solver.print_results(people_to_topics, save_as_csv=False)
