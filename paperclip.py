from dataclasses import dataclass
from enum import Enum
from typing import Tuple

class PaperclipState(Enum):
    UNDONE = "undone"
    DONE = "done"

@dataclass
class Paperclip:
    id: int
    state: PaperclipState
    position: Tuple[int, int] = (0, 0)
    
    def move_to_done(self):
        self.state = PaperclipState.DONE
        
    def move_to_undone(self):
        self.state = PaperclipState.UNDONE
        
    def update_position(self, x: int, y: int):
        self.position = (x, y)
        
    @property
    def color(self):
        return "red" if self.state == PaperclipState.UNDONE else "green"
