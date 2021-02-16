from utils import get_data
from solver import TeachingSolver
from settings import spreadsheet_id, spreadsheet_range

# get preferences data from a google sheet
# cols[0] specifies the name column. cols[1], ..., cols[4] specifies the 1st to 4th choices
data, people_to_topics = get_data(spreadsheet_id, spreadsheet_range, cols=[1,2,3,4,5])

weights = [1, 2, 3, 4] # weight for getting your 1st, 2nd, 3rd and 4th choice
low_priority_weight = 10 # weight for not getting any of your choices

n_blocks = 2 # currently supports only 2 blocks but passing it into the function anyways...

# add exclude_presenters if there is an odd number of people
solver = TeachingSolver(data, n_blocks, weights, low_priority_weight, exclude_presenters=["Clay"])
solver.solve()

solver.print_results(people_to_topics, save_as_csv=False)