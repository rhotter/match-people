from utils import get_data
from solver import CollaborationSolver
from settings import spreadsheet_id, spreadsheet_range

data, people_to_topics = get_data(spreadsheet_id, spreadsheet_range, cols=[1,6,7,8])

weights = [1, 2, 3] # weights for getting your 1st, 2nd, 3rd topic choices
dont_want_my_topic_weight = 4 # weight for not getting your own topic
dont_want_someone_else_topic_weight = 10 # weight for not getting someone else's topic

solver = CollaborationSolver(data, weights, dont_want_my_topic_weight, dont_want_someone_else_topic_weight)
solver.solve()
solver.print_results(people_to_topics, save_as_csv=False)