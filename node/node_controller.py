from utils.ssh_client import SSHClient
from node.node_parser import NodeParser
from data.data_manager import DataManager
import pandas as pd

class NodeController:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.ssh_client = SSHClient()
        self.node_parser = NodeParser()
        self.data_manager = DataManager()
    
    def get_current_node_data(self):
        """Fetches and processes current node data."""
        slurm_output = self.ssh_client.get_node_info(self.username, self.password)
        if not slurm_output:
            raise Exception("Failed to fetch node data")
        return self.node_parser.parse_slurm_output(slurm_output)
    
    def update_node_data(self):
        """Updates node data and returns both current and historical data."""
        current_data = self.get_current_node_data()
        historical_data = self.data_manager.update_historical_data(current_data)
        return current_data, historical_data
    
    def get_node_history(self, node_name):
        """Retrieves historical data for a specific node."""
        try:
            historical_data = pd.read_csv('historical_data.csv')
            historical_data['timestamp'] = pd.to_datetime(historical_data['timestamp'])
            return historical_data[historical_data['NodeName'] == node_name].copy()
        except FileNotFoundError:
            return pd.DataFrame()
    
    def get_node_current_state(self, node_name):
        """Gets current state for a specific node."""
        current_data = self.get_current_node_data()
        node_data = current_data[current_data['NodeName'] == node_name]
        return node_data.iloc[0] if not node_data.empty else None