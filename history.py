import json

class HistoryManager:
    def __init__(self, history_file='data.json'):
        self.history_file = history_file
        self.load_history()

    def load_history(self):
        try:
            with open(self.history_file, 'r') as file:
                self.history = json.load(file)
        except FileNotFoundError:
            self.history = {}

    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file)

    def add_entry(self, date, success):
        self.history[date] = self.history.get(date, 0) + success
        self.save_history()

    def get_history(self):
        return self.history

# This module can be imported and used in the main application file.
