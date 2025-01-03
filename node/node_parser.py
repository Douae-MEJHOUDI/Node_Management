import re
import pandas as pd
from datetime import datetime

class NodeParser:
    @staticmethod
    def parse_slurm_output(output):
        """Parses the SLURM output and returns a pandas DataFrame."""
        nodes = []
        node_blocks = output.strip().split("\n\n")
        timestamp = datetime.now()
        
        for block in node_blocks:
            node = {
                'timestamp': timestamp,
                'CPULoad': 0.0,
                'RealMemory': 0,
                'FreeMem': 0,
                'State': 'UNKNOWN'
            }
            for line in block.split("\n"):
                if match := re.search(r"NodeName=(\S+)", line):
                    node["NodeName"] = match.group(1)
                if match := re.search(r"CPULoad=(\S+)", line):
                    node["CPULoad"] = float(match.group(1))
                if match := re.search(r"RealMemory=(\S+)", line):
                    node["RealMemory"] = int(match.group(1))
                if match := re.search(r"FreeMem=(\S+)", line):
                    if match.group(1) == 'N/A':
                        node["FreeMem"] = 0
                    else:
                        node["FreeMem"] = int(match.group(1))
                if match := re.search(r"State=(\S+)", line):
                    node["State"] = match.group(1)
            nodes.append(node)
        return pd.DataFrame(nodes)