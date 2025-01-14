import rumps
from datetime import datetime
from settings_manager import SettingsManager
from history_manager import HistoryManager
from statistics_calculator import StatisticsCalculator
from custom_window import CustomWindow, SettingsWindow, InfoWindow
import os

class PaperclipMenuBarApp(rumps.App):
    def __init__(self):
        super().__init__("📎", quit_button=None)  # Paperclip emoji as icon
        
        # Get the path to our app's resources
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.icons_dir = os.path.join(self.app_dir, 'icons')
        self.settings_icon = os.path.join(self.icons_dir, 'setting.png')
        self.history_icon = os.path.join(self.icons_dir, 'fast-backward.png')
        
        self.settings_manager = SettingsManager('/Users/frank/Documents/Projects/paperclip/settings.json')
        self.history_manager = HistoryManager('/Users/frank/Documents/Projects/paperclip/data.json')
        self.stats_calculator = StatisticsCalculator(self.history_manager)
        
        # Create menu items
        self.undone_item = rumps.MenuItem("Tasks Remaining: 0")
        self.done_item = rumps.MenuItem("Tasks Completed: 0")
        self.menu = [
            self.undone_item,
            self.done_item,
            None,  # Separator
            rumps.MenuItem("Complete Task", callback=self.complete_task),
            rumps.MenuItem("Undo Task", callback=self.undo_task),
            None,  # Separator
            rumps.MenuItem("Statistics", callback=self.show_statistics),
            rumps.MenuItem("Settings", callback=self.show_settings),
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]

        # Initialize counters
        self.check_daily_reset()
    
    def check_daily_reset(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        if self.history_manager.get_last_reset() != current_date:
            # Record previous day's stats if they exist
            if self.history_manager.get_last_reset():
                self.history_manager.record_day(
                    self.history_manager.get_last_reset(),
                    self.done_count,
                    self.settings_manager.daily_paperclips
                )
            
            # Reset for new day
            self.done_count = 0
            self.history_manager.update_done_count(self.done_count)
            self.update_display()
    
    @property
    def done_count(self) -> int:
        return self.history_manager.get_done_count()
    
    @done_count.setter
    def done_count(self, value: int):
        self.history_manager.update_done_count(value)
    
    @property
    def undone_count(self) -> int:
        return self.settings_manager.daily_paperclips - self.done_count
    
    def update_display(self):
        self.undone_item.title = f"Tasks Remaining: {self.undone_count}"
        self.done_item.title = f"Tasks Completed: {self.done_count}"
        self.title = f"📎 {self.done_count}/{self.settings_manager.daily_paperclips}"
    
    def complete_task(self, _):
        if self.undone_count > 0:
            self.done_count += 1
            self.update_display()
        else:
            rumps.notification(
                title="No Tasks Remaining",
                subtitle="Cannot Complete Task",
                message="There are no remaining tasks to complete."
            )
    
    def undo_task(self, _):
        if self.done_count > 0:
            self.done_count -= 1
            self.update_display()
        else:
            rumps.notification(
                title="No Completed Tasks",
                subtitle="Cannot Undo Task",
                message="There are no completed tasks to undo."
            )
    
    def show_settings(self, _):
        window = SettingsWindow(
            message='Enter new daily paperclip goal:',
            title='Settings',
            default_text=str(self.settings_manager.daily_paperclips),
            dimensions=(200, 20),
            icon_path=self.settings_icon
        )
        response = window.run()
        if response.clicked:
            try:
                new_goal = int(response.text)
                if new_goal > 0:
                    print("Updating daily goal to", new_goal)
                    self.settings_manager.update_daily_goal(new_goal)
                    self.check_daily_reset()  # Reset counters with new goal
                    self.update_display()
                else:
                    rumps.alert("Invalid Input", "Please enter a positive number.")
            except ValueError:
                rumps.alert("Invalid Input", "Please enter a valid number.")
    
    def show_statistics(self, _):
        stats = self.stats_calculator.calculate_statistics()
        message = (
            f"Today's Progress:\n"
            f"Tasks Completed: {self.done_count}\n"
            f"Tasks Remaining: {self.undone_count}\n\n"
            f"7-Day Summary:\n"
            f"Weekly Rate: {stats['weekly_rate']}%\n"
            f"Current Streak: {stats['current_streak']} days\n"
            f"Best Streak: {stats['best_streak']} days"
        )
        window = InfoWindow(
            message=message,
            title='Statistics',
            icon_path=self.history_icon
        )
        window.run()
    
    def quit_app(self, _):
        rumps.quit_application()

if __name__ == '__main__':
    PaperclipMenuBarApp().run()
