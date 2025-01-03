# Node Management System - Project Report

## Project Overview
The Node Management System is a web-based application designed to monitor and manage SLURM cluster nodes in real-time. It provides a secure, interactive dashboard for system administrators to monitor resource usage, node states, and generate detailed reports.

## Architecture

### Core Components
1. **Authentication System**
   - Secure login interface
   - SSH-based credential verification
   - Session management for user persistence
   - Protection against unauthorized access

2. **Dashboard Interface**
   - Real-time monitoring of node status
   - Interactive visualizations
   - Resource usage metrics
   - Node-specific detailed views

3. **Reporting System**
   - PDF report generation
   - Customizable report content
   - Visual data representation
   - Historical data analysis

### Technical Stack
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
