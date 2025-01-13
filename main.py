import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional

from paperclip import Paperclip, PaperclipState
from settings_manager import SettingsManager

class PaperclipContainer:
    def __init__(self, frame: ttk.Frame, name: str):
        self.frame = ttk.LabelFrame(frame, text=name)
        self.canvas = tk.Canvas(self.frame, width=200, height=300)
        self.count_var = tk.StringVar(value='0')
        self.label = ttk.Label(self.frame, textvariable=self.count_var)
        self.paperclips: List[Paperclip] = []
        
        self.frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.label.pack(pady=5)
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    def clear(self):
        self.canvas.delete('all')
        self.paperclips.clear()
    
    def add_paperclip(self, paperclip: Paperclip):
        self.paperclips.append(paperclip)
        self.update_display()
    
    def remove_paperclip(self, paperclip: Paperclip):
        self.paperclips.remove(paperclip)
        self.update_display()
    
    def update_display(self):
        self.canvas.delete('all')
        self.count_var.set(f'Count: {len(self.paperclips)}')
        
        for i, clip in enumerate(self.paperclips):
            y_pos = 20 + (i * 30)
            clip.update_position(50, y_pos)
            self.canvas.create_rectangle(
                50, y_pos, 150, y_pos + 20,
                fill=clip.color,
                tags=(f'clip_{clip.id}', 'clip')
            )

class PaperclipApp:
    def __init__(self):
        self.settings_manager = SettingsManager('settings.json')
        self.history_file = 'data.json'
        self.load_history()
        self.create_ui()
        self.next_clip_id = 1

    def create_ui(self):
        self.root = tk.Tk()
        self.root.title('Paperclip Task Tracker')
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        
        # Main tab
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text='Tasks')
        
        # Settings tab
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text='Settings')
        
        self.setup_main_tab()
        self.setup_settings_tab()
        
        # Check for new day initialization
        self.check_daily_reset()

    def setup_main_tab(self):
        self.undone_container = PaperclipContainer(self.main_frame, 'Undone Tasks')
        self.done_container = PaperclipContainer(self.main_frame, 'Completed Tasks')
        
        # Setup drag and drop for both containers
        self.setup_drag_drop(self.undone_container, self.done_container)
        self.setup_drag_drop(self.done_container, self.undone_container)

    def setup_settings_tab(self):
        ttk.Label(self.settings_frame, text='Daily Paperclip Goal:').pack(pady=10)
        
        self.daily_goal_var = tk.StringVar(value=str(self.settings_manager.daily_paperclips))
        self.daily_goal_entry = ttk.Entry(self.settings_frame, textvariable=self.daily_goal_var)
        self.daily_goal_entry.pack(pady=5)
        
        ttk.Button(self.settings_frame, text='Save Settings', 
                  command=self.save_daily_goal).pack(pady=10)

    def save_daily_goal(self):
        try:
            goal = int(self.daily_goal_var.get())
            self.settings_manager.update_daily_goal(goal)
            messagebox.showinfo('Success', 'Daily goal updated!')
        except ValueError as e:
            messagebox.showerror('Error', str(e))

    def setup_drag_drop(self, source_container: PaperclipContainer, target_container: PaperclipContainer):
        source_container.canvas.bind('<B1-Motion>', 
            lambda e: self.on_drag(e, source_container))
        source_container.canvas.bind('<ButtonRelease-1>', 
            lambda e: self.on_drop(e, source_container, target_container))

    def on_drag(self, event: tk.Event, container: PaperclipContainer):
        closest = container.canvas.find_closest(event.x, event.y)
        if closest and 'clip' in container.canvas.gettags(closest):
            self.dragged_clip = next(
                (clip for clip in container.paperclips 
                 if f'clip_{clip.id}' in container.canvas.gettags(closest)),
                None
            )
            if self.dragged_clip:
                container.canvas.tag_raise(f'clip_{self.dragged_clip.id}')

    def on_drop(self, event: tk.Event, source: PaperclipContainer, target: PaperclipContainer):
        if hasattr(self, 'dragged_clip') and self.dragged_clip:
            widget_x = target.canvas.winfo_rootx()
            widget_y = target.canvas.winfo_rooty()
            if (widget_x <= event.x_root <= widget_x + target.canvas.winfo_width() and
                widget_y <= event.y_root <= widget_y + target.canvas.winfo_height()):
                # Move paperclip between containers
                source.remove_paperclip(self.dragged_clip)
                if target == self.done_container:
                    self.dragged_clip.move_to_done()
                else:
                    self.dragged_clip.move_to_undone()
                target.add_paperclip(self.dragged_clip)
                self.save_current_state()
            
            self.dragged_clip = None

    def check_daily_reset(self):
        current_date = datetime.now().strftime('%Y-%m-%d')
        if self.history.get('last_reset') != current_date:
            self.history['last_reset'] = current_date
            self.initialize_daily_paperclips()
            self.save_history()

    def initialize_daily_paperclips(self):
        self.undone_container.clear()
        self.done_container.clear()
        
        for i in range(self.settings_manager.daily_paperclips):
            clip = Paperclip(id=self.next_clip_id, state=PaperclipState.UNDONE)
            self.undone_container.add_paperclip(clip)
            self.next_clip_id += 1

    def save_current_state(self):
        self.history['undone_clips'] = [clip.id for clip in self.undone_container.paperclips]
        self.history['done_clips'] = [clip.id for clip in self.done_container.paperclips]
        self.save_history()

    def load_history(self):
        try:
            with open(self.history_file, 'r') as file:
                self.history = json.load(file)
        except FileNotFoundError:
            self.history = {}
            self.save_history()

    def save_history(self):
        with open(self.history_file, 'w') as file:
            json.dump(self.history, file)

if __name__ == '__main__':
    app = PaperclipApp()
    app.root.mainloop()
