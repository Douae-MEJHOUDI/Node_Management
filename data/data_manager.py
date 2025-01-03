import pandas as pd
from datetime import datetime, timedelta

class DataManager:
    @staticmethod
    def update_historical_data(new_data):
        """Updates the historical data CSV with new readings."""
        try:
            historical_data = pd.read_csv('historical_data.csv')
            historical_data['timestamp'] = pd.to_datetime(historical_data['timestamp'])
        except FileNotFoundError:
            historical_data = pd.DataFrame()
        
        new_data['timestamp'] = pd.to_datetime(new_data['timestamp'])
        updated_data = pd.concat([historical_data, new_data], ignore_index=True)
        
        cutoff_date = datetime.now() - timedelta(days=7)
        updated_data = updated_data[updated_data['timestamp'] > cutoff_date]
        
        updated_data = updated_data.sort_values('timestamp').drop_duplicates(
            subset=['NodeName', 'timestamp'], 
            keep='last'
        )
        
        updated_data.to_csv('historical_data.csv', index=False)
        return updated_data