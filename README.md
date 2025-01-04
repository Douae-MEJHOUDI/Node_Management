# SLURM Node Management System

## Project Overview
The Node Management System is a web-based application designed to monitor and manage SLURM cluster nodes in real-time. It provides a secure, interactive dashboard for system administrators to monitor resource usage, node states, and generate detailed reports.

## Features

- Secure SSH authentication
- Real-time node monitoring
- Interactive visualizations
- Automated data updates (5-minute intervals)
- PDF report generation
- 7-day historical data tracking


## Technical Stack
- **Backend**: FastAPI, Python
- **Frontend**: Dash, Plotly
- **Authentication**: SSH Client (Paramiko)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Report Generation**: ReportLab
- **Styling**: Custom CSS, Dash components


## Project Structure
```
project/
├── assets/
│   └── custom.css
├── auth/
│   └── auth_manager.py
├── utils/
│   ├── ssh_client.py
│   └── report_generator.py
├── visualization/
│   ├── dashboard.py
│   └── graphs.py
├── node/
│   ├── node_controller.py
│   └── node_parser.py
├── config/
│   └── settings.py
└── main.py
```



## How to run the project 
- First install all the libraries in requirements.txt  
- Run ``` python main.py ``` (make sure you're connected to UM6P.local WiFi)
