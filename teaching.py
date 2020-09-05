from utils import get_data, get_generated_data
from solver import TeachingSolver
from settings import spreadsheet_id, spreadsheet_range

data, people_to_topics = get_data(spreadsheet_id, spreadsheet_range, cols=[0,1,2,3,4])
# print(data)
# print(data)
# data = get_generated_data(n_people=11, n_preferences=4)
# print(data)
# weights = [1, 2**2, 3**2, 4**2]
# low_priority_weight = 5**2

weights = [1, 2, 3, 4]
low_priority_weight = 6

n_blocks = 2

solver = TeachingSolver(data, n_blocks, weights, low_priority_weight, exclude_presenters=["Raffi"])
solver.solve()

solver.print_results(people_to_topics, save_as_csv=True)