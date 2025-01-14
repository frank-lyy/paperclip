from datetime import datetime, timedelta
from typing import Dict, Any

class StatisticsCalculator:
    def __init__(self, history_manager):
        self.history_manager = history_manager
    
    def calculate_statistics(self) -> Dict[str, Any]:
        records = self.history_manager.get_daily_records()
        
        return {
            'weekly_rate': self._calculate_weekly_rate(records),
            'current_streak': self._calculate_current_streak(records),
            'best_streak': self._calculate_best_streak(records)
        }
    
    def _calculate_weekly_rate(self, records: Dict) -> int:
        success_count = 0
        total_days = 0
        current_date = datetime.now()
        
        for i in range(7):
            check_date = (current_date - timedelta(days=i)).strftime('%Y-%m-%d')
            if check_date in records:
                total_days += 1
                if records[check_date]['completed'] >= records[check_date]['goal']:
                    success_count += 1
        
        return round((success_count / max(total_days, 1)) * 100)
    
    def _calculate_current_streak(self, records: Dict) -> int:
        current_streak = 0
        
        if records:
            check_date = datetime.now()
            while check_date.strftime('%Y-%m-%d') in records:
                date_str = check_date.strftime('%Y-%m-%d')
                if records[date_str]['completed'] >= records[date_str]['goal']:
                    current_streak += 1
                else:
                    break
                check_date -= timedelta(days=1)
        
        return current_streak
    
    def _calculate_best_streak(self, records: Dict) -> int:
        dates = sorted(records.keys())
        best_streak = 0
        temp_streak = 0
        
        for date in dates:
            if records[date]['completed'] >= records[date]['goal']:
                temp_streak += 1
                best_streak = max(best_streak, temp_streak)
            else:
                temp_streak = 0
        
        return best_streak
