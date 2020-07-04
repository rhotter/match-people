from utils import get_data, get_generated_data
from solver import CollaborationSolver
from settings import spreadsheet_id, spreadsheet_range

data, people_to_topics = get_data(spreadsheet_id, spreadsheet_range, cols=[1,6,7,8])
# data = get_generated_data(n_people=50, n_preferences=4)


weights = [1, 2, 3]
dont_want_my_topic_weight = 4
dont_want_someone_else_topic_weight = 8

solver = CollaborationSolver(data, weights, dont_want_my_topic_weight, dont_want_someone_else_topic_weight)
solver.solve()
solver.print_results(people_to_topics, print_preferences=True, save_as_csv=False)