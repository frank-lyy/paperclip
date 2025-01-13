import rumps
import json
from datetime import datetime
from paperclip import Paperclip, PaperclipState
from settings_manager import SettingsManager

class PaperclipMenuBarApp(rumps.App):
    def __init__(self):
        super().__init__("📎", quit_button=None)  # Paperclip emoji as icon
        
        self.settings_manager = SettingsManager('/Users/frank/Documents/Projects/paperclip/settings.json')
        self.history_file = '/Users/frank/Documents/Projects/paperclip/data.json'
        self.load_history()
        
        # Initialize counters
        self.undone_count = 0
        self.done_count = 0
        
        # Create menu items
        self.create_menu_items()
        self.check_daily_reset()
        
    def create_menu_items(self):
        # Status items
        self.undone_item = rumps.MenuItem(f"Tasks Remaining: {self.undone_count}")
        self.done_item = rumps.MenuItem(f"Tasks Completed: {self.done_count}")
        
        # Action items
        self.complete_task = rumps.MenuItem("Complete Task", callback=self.on_complete_task)
        self.undo_task = rumps.MenuItem("Undo Task", callback=self.on_undo_task)
        self.settings_button = rumps.MenuItem("Settings", callback=self.show_settings)
        
        # Add items to menu
        self.menu = [
            self.undone_item,
            self.done_item,
            None,  # Separator
            self.complete_task,
            self.undo_task,
            None,  # Separator
            self.settings_button,
            None,  # Separator
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]
    
    def check_daily_reset(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        if self.history.get('last_reset') != current_date:
            self.history['last_reset'] = current_date
            self.undone_count = self.settings_manager.daily_paperclips
            self.done_count = 0
            self.save_current_state()
            self.update_display()
    
    def update_display(self):
        self.undone_item.title = f"Tasks Remaining: {self.undone_count}"
        self.done_item.title = f"Tasks Completed: {self.done_count}"
        self.title = f"📎 {self.done_count}/{self.settings_manager.daily_paperclips}"
    
    @rumps.clicked("Complete Task")
    def on_complete_task(self, _):
        if self.undone_count > 0:
            self.undone_count -= 1
            self.done_count += 1
            self.save_current_state()
            self.update_display()
            if self.undone_count == 0:
                rumps.notification(
                    title="All Tasks Complete!",
                    subtitle="Great job!",
                    message="You've completed all your tasks for today!"
                )
        else:
            rumps.notification(
                title="No Tasks Remaining",
                subtitle="Can't complete task",
                message="There are no remaining tasks to complete."
            )
    
    @rumps.clicked("Undo Task")
    def on_undo_task(self, _):
        if self.done_count > 0:
            self.done_count -= 1
            self.undone_count += 1
            self.save_current_state()
            self.update_display()
        else:
            rumps.notification(
                title="No Completed Tasks",
                subtitle="Can't undo",
                message="There are no completed tasks to undo."
            )
    
    @rumps.clicked("Settings")
    def show_settings(self, _):
        response = rumps.Window(
            message='Enter daily paperclip goal:',
            default_text=str(self.settings_manager.daily_paperclips),
            ok='Save',
            cancel='Cancel'
        ).run()
        
        if response.clicked:
            try:
                new_goal = int(response.text)
                if new_goal <= 0:
                    raise ValueError("Goal must be positive")
                self.settings_manager.update_daily_goal(new_goal)
                # If it's a new day, reset with new goal
                self.check_daily_reset()
            except ValueError as e:
                rumps.notification(
                    title="Invalid Input",
                    subtitle="Error",
                    message="Please enter a positive number."
                )
    
    def quit_app(self, _):
        self.save_current_state()
        rumps.quit_application()
    
    def load_history(self):
        try:
            with open(self.history_file, 'r') as file:
                self.history = json.load(file)
                self.undone_count = self.history.get('undone_count', 0)
                self.done_count = self.history.get('done_count', 0)
        except FileNotFoundError:
            self.history = {}
            self.save_current_state()
    
    def save_current_state(self):
        self.history['undone_count'] = self.undone_count
        self.history['done_count'] = self.done_count
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file)

if __name__ == '__main__':
    PaperclipMenuBarApp().run()
