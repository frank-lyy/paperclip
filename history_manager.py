import json
from datetime import datetime, timedelta

class HistoryManager:
    def __init__(self, history_file: str):
        self.history_file = history_file
        self.history = self.load_history()
        
    def load_history(self):
        try:
            with open(self.history_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {'last_reset': None, 'done_count': 0, 'daily_records': {}}
    
    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file)
    
    def update_done_count(self, count: int):
        self.history['done_count'] = count
        self.save_history()
    
    def get_done_count(self) -> int:
        return self.history.get('done_count', 0)
    
    def get_last_reset(self) -> str:
        return self.history.get('last_reset')
    
    def record_day(self, date: str, completed: int, goal: int):
        if 'daily_records' not in self.history:
            self.history['daily_records'] = {}
        
        self.history['daily_records'][date] = {
            'completed': completed,
            'goal': goal
        }
        self.history['last_reset'] = date
        self.save_history()
    
    def get_daily_records(self):
        return self.history.get('daily_records', {})
