import plotly.graph_objs as go
import pandas as pd

class GraphGenerator:
    @staticmethod
    def create_node_history_graph(node_history):
        """Creates a detailed historical graph for a node."""
        memory_usage = ((node_history['RealMemory'] - node_history['FreeMem']) / 
                       node_history['RealMemory'] * 100)
        
        daily_stats = node_history.resample('D', on='timestamp').agg({
            'CPULoad': ['mean', 'max'],
            'FreeMem': 'mean',
            'RealMemory': 'first'
        }).reset_index()
        
        daily_stats['MemoryUsage'] = ((daily_stats['RealMemory']['first'] - 
                                      daily_stats['FreeMem']['mean']) / 
                                     daily_stats['RealMemory']['first'] * 100)
        
        return {
            "data": [
                go.Scatter(
                    x=node_history['timestamp'],
                    y=node_history['CPULoad'],
                    name='CPU Load',
                    line=dict(color='blue'),
                    hovertemplate='CPU Load: %{y:.1f}%<br>Time: %{x}<extra></extra>'
                ),
                go.Scatter(
                    x=node_history['timestamp'],
                    y=memory_usage,
                    name='Memory Usage',
                    line=dict(color='red'),
                    hovertemplate='Memory Usage: %{y:.1f}%<br>Time: %{x}<extra></extra>'
                ),
                go.Scatter(
                    x=daily_stats['timestamp'],
                    y=daily_stats['CPULoad']['mean'],
                    name='Daily Avg CPU',
                    mode='markers',
                    marker=dict(size=10, symbol='star', color='blue'),
                    hovertemplate='Daily Avg CPU: %{y:.1f}%<br>Date: %{x}<extra></extra>'
                ),
                go.Scatter(
                    x=daily_stats['timestamp'],
                    y=daily_stats['MemoryUsage'],
                    name='Daily Avg Memory',
                    mode='markers',
                    marker=dict(size=10, symbol='star', color='red'),
                    hovertemplate='Daily Avg Memory: %{y:.1f}%<br>Date: %{x}<extra></extra>'
                )
            ],
            "layout": {
                "title": {
                    "text": "7-Day Resource Usage History",
                    "y": 1.2,
                    "x": 0.5,
                    "xanchor": "center",
                    "yanchor": "top"
                },
                "xaxis": {
                    "title": "Time",
                    "rangeslider": {
                        "visible": True,
                        "thickness": 0.1,
                        "bgcolor": "white"
                    },
                    "type": "date",
                    "domain": [0, 1]
                },
                "yaxis": {
                    "title": "Percentage (%)",
                    "range": [0, 100],
                    "gridcolor": "lightgray",
                    "zerolinecolor": "lightgray"
                },
                "height": 600,
                "hovermode": "x unified",
                "showlegend": True,
                "legend": {
                    "orientation": "h",
                    "yanchor": "bottom",
                    "y": 1.02,
                    "xanchor": "center",
                    "x": 0.5,
                    "bgcolor": "rgba(255, 255, 255, 0.9)"
                },
                "margin": {
                    "t": 100,
                    "b": 100,
                    "l": 60,
                    "r": 20,
                    "pad": 10
                },
                "plot_bgcolor": "white",
                "annotations": [{
                    "text": "Use the range slider to zoom into specific time periods",
                    "showarrow": False,
                    "x": 0.5,
                    "y": -0.15,
                    "xref": "paper",
                    "yref": "paper",
                    "font": {"size": 10, "color": "gray"}
                }]
            }
        }