import json
from typing import Dict, Any

class SettingsManager:
    def __init__(self, settings_file: str):
        self.settings_file = settings_file
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        try:
            with open(self.settings_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            default_settings = {'daily_paperclips': 5}
            self.save_settings(default_settings)
            return default_settings
    
    def save_settings(self, settings: Dict[str, Any]) -> None:
        self.settings = settings
        with open(self.settings_file, 'w') as file:
            json.dump(settings, file)
    
    def update_daily_goal(self, goal: int) -> None:
        if goal <= 0:
            raise ValueError("Daily goal must be positive")
        self.settings['daily_paperclips'] = goal
        self.save_settings(self.settings)
    
    @property
    def daily_paperclips(self) -> int:
        return self.settings.get('daily_paperclips', 5)
