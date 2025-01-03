from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objs as go
from datetime import datetime
from visualization.graphs import GraphGenerator
from node.node_controller import NodeController
from utils.report_generator import ReportGenerator
from config.settings import UPDATE_INTERVAL


COLORS = {
    'background': '#f8f9fa',
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#3498db',
    'success': '#2ecc71',
    'warning': '#f1c40f',
    'danger': '#e74c3c',
    'text': '#2c3e50',
    'light': '#ecf0f1'
}

STYLES = {
    'page_container': {
        'padding': '20px',
        'backgroundColor': COLORS['background'],
        'minHeight': '100vh'
    },
    'header': {
        'backgroundColor': COLORS['primary'],
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'marginBottom': '20px',
        'position': 'relative'
    },
    'title': {
        'color': 'white',
        'textAlign': 'center',
        'margin': '0',
        'fontSize': '2.5em',
        'fontWeight': 'bold'
    },
    'report_button': {
        'position': 'absolute',
        'right': '20px',
        'top': '50%',
        'transform': 'translateY(-50%)',
        'backgroundColor': COLORS['accent'],
        'color': 'white',
        'border': 'none',
        'padding': '12px 24px',
        'borderRadius': '5px',
        'cursor': 'pointer',
        'fontWeight': 'bold',
        'transition': 'background-color 0.3s ease',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    },
    'card': {
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    },
    'section_title': {
        'color': COLORS['primary'],
        'textAlign': 'center',
        'marginBottom': '20px',
        'fontSize': '1.8em',
        'fontWeight': 'bold'
    },
    'dropdown_container': {
        'backgroundColor': 'white',
        'padding': '15px',
        'borderRadius': '8px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'marginBottom': '20px'
    },
    'dropdown_label': {
        'fontWeight': 'bold',
        'fontSize': '16px',
        'color': COLORS['primary'],
        'marginBottom': '8px',
        'display': 'block'
    },
    'timestamp': {
        'textAlign': 'center',
        'color': COLORS['secondary'],
        'marginBottom': '20px',
        'fontSize': '14px'
    }
}


class Dashboard:
    def __init__(self, requests_pathname_prefix='/dashboard/'):
        self.app = None
        self.requests_pathname_prefix = requests_pathname_prefix
        self.node_controller = None
        self.graph_generator = GraphGenerator()

    def initialize_with_credentials(self, username: str, password: str):
        """Initialize dashboard with user credentials."""
        if not self.app:
            self.app = Dash(__name__, requests_pathname_prefix=self.requests_pathname_prefix)
            self.node_controller = NodeController(username, password)
            self.setup_layout()
            self.setup_callbacks()

    def setup_layout(self):
        """Set up the dashboard layout."""
        try:
            initial_data = self.node_controller.get_current_node_data()
            self.app.layout = html.Div([
                
                html.Div([
                    html.H1("Node Management System", style=STYLES['title']),
                    html.Button(
                        [
                            html.I(className="fas fa-file-pdf", style={'marginRight': '8px'}),
                            "Generate Report"
                        ],
                        id="generate-report-btn",
                        style=STYLES['report_button']
                    ),
                    dcc.Download(id="download-report")
                ], style=STYLES['header']),
                
                
                html.Div([
                    dcc.Interval(
                        id='interval-component',
                        interval=UPDATE_INTERVAL,
                        n_intervals=0
                    ),
                    
                    html.Div(id='last-update-timestamp', 
                             style=STYLES['timestamp']),

                    
                    html.Div([
                        html.Label("Select a Node:", style=STYLES['dropdown_label']),
                        dcc.Dropdown(
                            id="node-dropdown",
                            options=[{"label": node, "value": node} 
                                    for node in initial_data["NodeName"]],
                            placeholder="Choose a node",
                            style={'marginTop': '5px'}
                        ),
                    ], style=STYLES['dropdown_container']),

                    
                    html.Div([
                        html.H3("Selected Node Details", style=STYLES['section_title']),
                        html.Div(id="node-state-indicator", 
                                style={"textAlign": "center", "marginTop": "20px"}),
                        html.Div([
                            html.Div([
                                dcc.Graph(id="node-cpu-gauge")
                            ], style={'width': '50%', 'display': 'inline-block'}),
                            html.Div([
                                dcc.Graph(id="node-memory-gauge")
                            ], style={'width': '50%', 'display': 'inline-block'})
                        ]),
                        dcc.Graph(id="node-history-graph"),
                        
                    ], style=STYLES['card']),

                    
                    html.Div([
                        html.H3("Cluster Resource Usage", style=STYLES['section_title']),
                        dcc.Graph(id="cpu-graph"),
                        dcc.Graph(id="memory-graph"),
                        dcc.Graph(id="state-pie-chart")
                    ], style=STYLES['card'])
                ], style=STYLES['page_container'])
            ])
        
        except Exception as e:
            print(f"Error setting up layout: {e}")
            self.app.layout = html.Div([
                html.H1("Error Loading Dashboard", style={'color': COLORS['danger']}),
                html.P(f"An error occurred: {str(e)}", style={'color': COLORS['danger']})
            ], style=STYLES['page_container'])

    def setup_callbacks(self):
        """Set up all dashboard callbacks."""
        self.setup_update_metrics_callback()
        self.setup_node_graphs_callback()
        self.setup_report_callback()

    def setup_update_metrics_callback(self):
        @self.app.callback(
            [Output('last-update-timestamp', 'children'),
             Output('node-dropdown', 'options'),
             Output('cpu-graph', 'figure'),
             Output('memory-graph', 'figure'),
             Output('state-pie-chart', 'figure')],
            Input('interval-component', 'n_intervals')
        )
        def update_metrics(n):
            try:
                current_data, _ = self.node_controller.update_node_data()
                
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                timestamp_div = html.Div([
                    "Last updated: ",
                    html.Span(timestamp, style={'fontWeight': 'bold'})
                ])
                
                dropdown_options = [{"label": node, "value": node} 
                                  for node in current_data["NodeName"]]
                
                cpu_figure = {
                    "data": [
                        {"x": current_data["NodeName"], 
                         "y": current_data["CPULoad"], 
                         "type": "bar", 
                         "name": "CPU Load"}
                    ],
                    "layout": {
                        "title": "CPU Load per Node",
                        "xaxis": {"title": "Nodes"},
                        "yaxis": {"title": "CPU Load (%)"}
                    }
                }
                
                memory_figure = {
                    "data": [
                        {
                            "x": current_data["NodeName"],
                            "y": current_data["RealMemory"],
                            "type": "bar",
                            "name": "Total Memory",
                            "marker": {"color": "rgba(255, 140, 0, 0.7)"}
                        },
                        {
                            "x": current_data["NodeName"],
                            "y": current_data["RealMemory"] - current_data["FreeMem"],
                            "type": "bar",
                            "name": "Used Memory",
                            "marker": {"color": "rgba(31, 119, 180, 0.9)"}
                        }
                    ],
                    "layout": {
                        "title": "Memory Usage per Node",
                        "barmode": "overlay",
                        "xaxis": {"title": "Nodes"},
                        "yaxis": {"title": "Memory (MB)"},
                        "showlegend": True,
                        "legend": {"orientation": "h", "y": -0.15},
                        "margin": {"t": 40, "b": 100, "l": 60, "r": 20},
                        "height": 500
                    }
                }
                
                state_figure = {
                    "data": [
                        {
                            "labels": current_data["State"].value_counts().index,
                            "values": current_data["State"].value_counts().values,
                            "type": "pie",
                            "name": "Node States"
                        }
                    ],
                    "layout": {"title": "Node State Distribution"}
                }
                
                return timestamp_div, dropdown_options, cpu_figure, memory_figure, state_figure
            except Exception as e:
                print(f"Error updating metrics: {e}")
                return html.Div("Error updating data"), [], {}, {}, {}

    def setup_node_graphs_callback(self):
        @self.app.callback(
            [Output("node-cpu-gauge", "figure"),
             Output("node-memory-gauge", "figure"),
             Output("node-history-graph", "figure"),
             Output("node-state-indicator", "children")],
            [Input("node-dropdown", "value"),
             Input('interval-component', 'n_intervals')]
        )
        def update_node_graphs(selected_node, n):
            if not selected_node:
                empty_gauge = {
                    "data": [],
                    "layout": {"height": 300, "showlegend": False}
                }
                return empty_gauge, empty_gauge, empty_gauge, "Select a node to view its details."
            
            try:
                node_history = self.node_controller.get_node_history(selected_node)
                current_data = self.node_controller.get_node_current_state(selected_node)

                if current_data is None:
                    raise Exception("No current data available for node")

                cpu_gauge = self._create_cpu_gauge(current_data)
                memory_gauge = self._create_memory_gauge(current_data)
                history_figure = self.graph_generator.create_node_history_graph(node_history)
                state_indicator = self._create_state_indicator(current_data)

                return cpu_gauge, memory_gauge, history_figure, state_indicator

            except Exception as e:
                print(f"Error updating node graphs: {e}")
                empty_gauge = {
                    "data": [],
                    "layout": {"height": 300, "showlegend": False}
                }
                return empty_gauge, empty_gauge, empty_gauge, f"Error: {str(e)}"

    def setup_report_callback(self):
        @self.app.callback(
            Output("download-report", "data"),
            Input("generate-report-btn", "n_clicks"),
            prevent_initial_call=True
        )
        def generate_report(n_clicks):
            if n_clicks is None:
                return None
            
            try:
                current_data = self.node_controller.get_current_node_data()
                report_gen = ReportGenerator()
                filename = f"node_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                report_gen.generate_report(current_data, filename)
                
                return dcc.send_file(
                    filename,
                    filename=filename
                )
            except Exception as e:
                print(f"Error generating report: {e}")
                return None

    def _create_cpu_gauge(self, node_data):
        return {
            "data": [go.Indicator(
                mode="gauge+number",
                value=node_data['CPULoad'],
                title={'text': "CPU Load (%)"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgreen"},
                        {'range': [50, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            )],
            "layout": {"height": 300}
        }

    def _create_memory_gauge(self, node_data):
        memory_usage = ((node_data['RealMemory'] - node_data['FreeMem']) / 
                       node_data['RealMemory'] * 100)
        return {
            "data": [go.Indicator(
                mode="gauge+number+delta",
                value=memory_usage,
                title={'text': "Memory Usage (%)"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgreen"},
                        {'range': [60, 85], 'color': "yellow"},
                        {'range': [85, 100], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            )],
            "layout": {"height": 300}
        }

    def _create_state_indicator(self, node_data):
        state_colors = {
            'ALLOCATED': COLORS['success'],
            'IDLE': COLORS['warning'],
            'DOWN': COLORS['danger']
        }
        state_style = {
            'padding': '12px 24px',
            'borderRadius': '5px',
            'backgroundColor': state_colors.get(node_data['State'], COLORS['secondary']),
            'color': 'white',
            'display': 'inline-block',
            'marginTop': '10px',
            'fontWeight': 'bold',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }
        return html.Div([
            html.H4("Node State", style={'color': COLORS['primary']}),
            html.Div(node_data['State'], style=state_style)
        ])