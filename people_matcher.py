from .utils import get_raw_spreadsheet_data, process_raw_spreadsheet_data, get_edges
import networkx as nx

class PeopleMatcher():
  def __init__(self, spreadsheet_id, spreadsheet_range, weights, low_priority_weight,
  group_size, random_noise=False):
    self.data = self._get_data_from_spreadsheet(spreadsheet_id, spreadsheet_range)
    self.weights = weights
    self.low_priority_weight = low_priority_weight
    self.group_size = group_size
    self.G = nx.DiGraph()
    self.random_noise = random_noise
  
  def _get_data_from_spreadsheet(self, spreadsheet_id, spreadsheet_range):
    values = get_raw_spreadsheet_data(spreadsheet_id, spreadsheet_range)
    data = process_raw_spreadsheet_data(values)
    return data
  
  def optimize(self):
    edges = get_edges(self)