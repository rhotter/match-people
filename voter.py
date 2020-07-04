from utils import get_data, get_generated_data
from pyvotecore.schulze_method import SchulzeMethod
from pyvotecore.condorcet import CondorcetHelper
from pyvotecore.ranked_pairs import RankedPairs
from tabulate import tabulate
from settings import spreadsheet_id, spreadsheet_range

data = get_data(spreadsheet_id, spreadsheet_range, cols=[1,9,10,11], people=False, ignore_topics={"MICROWAVE COOKING", "Acapella exercise, which will involve singing a song with multiple harmonies"})


topics = {topic for x in data for topic in x['out']}
int_to_topics = {i: topic_name for i, topic_name in enumerate(topics)}
topics_to_int = {topic_name: i for i, topic_name in int_to_topics.items()}

voter_data = []
for x in data:
  voter_data.append([[topics_to_int[topic]] for topic in x['out']])

ballots = [{"count":1, "ballot": topics} for topics in voter_data]

# ballots = [{"count":1, "ballot": [["AV"],["B"]]},{"count":1, "ballot": [["C"],["AV"]]}]
# print(SchulzeMethod(ballots, ballot_notation = CondorcetHelper.BALLOT_NOTATION_GROUPING).as_dict())
results = RankedPairs(ballots, ballot_notation = RankedPairs.BALLOT_NOTATION_GROUPING).as_dict()
if "tied_winners" in results.keys():
  winning_ints = results["tied_winners"]
else:
  winning_ints = results["winner"]
if not isinstance(winning_ints, list):
  winning_ints = [winning_ints]
winners = [[int_to_topics[x]] for x in winning_ints]
print("Winners")

print(tabulate(winners, tablefmt="grid_tables"))
