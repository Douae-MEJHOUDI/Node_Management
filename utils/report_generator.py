from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from datetime import datetime
import io
import matplotlib.pyplot as plt
import seaborn as sns
import base64

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12
        )
        self.body_style = self.styles['Normal']

    def generate_report(self, node_data, filename="node_report.pdf"):
        """Generate a PDF report with node information."""
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Create story (content) for the PDF
        story = []
        
        # Add Title
        story.append(Paragraph("Node Management System Report", self.title_style))
        story.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.body_style
        ))
        story.append(Spacer(1, 20))

        # Add System Overview
        story.append(Paragraph("System Overview", self.heading_style))
        
        # Create overview table
        total_nodes = len(node_data)
        total_cpu_load = node_data['CPULoad'].mean()
        total_memory = node_data['RealMemory'].sum()
        used_memory = (node_data['RealMemory'] - node_data['FreeMem']).sum()
        
        overview_data = [
            ['Metric', 'Value'],
            ['Total Nodes', str(total_nodes)],
            ['Average CPU Load', f"{total_cpu_load:.2f}%"],
            ['Total Memory', f"{total_memory/1024:.2f} GB"],
            ['Used Memory', f"{used_memory/1024:.2f} GB"],
            ['Memory Utilization', f"{(used_memory/total_memory)*100:.2f}%"]
        ]
        
        table = Table(overview_data, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))

        # Add Node Details
        story.append(Paragraph("Node Details", self.heading_style))
        
        node_details = []
        # Create header row
        node_details.append(['Node Name', 'CPU Load', 'Memory Usage', 'State'])
        
        # Add data rows
        for _, row in node_data.iterrows():
            memory_usage = ((row['RealMemory'] - row['FreeMem']) / row['RealMemory'] * 100)
            node_details.append([
                row['NodeName'],
                f"{row['CPULoad']:.1f}%",
                f"{memory_usage:.1f}%",
                row['State']
            ])

        table = Table(node_details, colWidths=[120, 100, 100, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))

        # Add visualizations using matplotlib
        story.append(Paragraph("System Visualizations", self.heading_style))
        
        # CPU Load Distribution
        plt.figure(figsize=(8, 4))
        sns.histplot(data=node_data, x='CPULoad', bins=10)
        plt.title('CPU Load Distribution')
        plt.xlabel('CPU Load (%)')
        plt.ylabel('Count')
        
        # Save plot to memory
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png', bbox_inches='tight')
        img_data.seek(0)
        plt.close()
        
        # Add plot to PDF
        img = Image(img_data)
        img.drawWidth = 400
        img.drawHeight = 300
        story.append(img)
        story.append(Spacer(1, 20))

        # Memory Usage by Node
        plt.figure(figsize=(10, 5))
        memory_usage = ((node_data['RealMemory'] - node_data['FreeMem']) / 
                       node_data['RealMemory'] * 100)
        plt.bar(node_data['NodeName'], memory_usage)
        plt.title('Memory Usage by Node')
        plt.xlabel('Node')
        plt.ylabel('Memory Usage (%)')
        plt.xticks(rotation=45)
        
        # Save plot to memory
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png', bbox_inches='tight')
        img_data.seek(0)
        plt.close()
        
        # Add plot to PDF
        img = Image(img_data)
        img.drawWidth = 400
        img.drawHeight = 300
        story.append(img)

        # Build PDF
        doc.build(story)
        return filename