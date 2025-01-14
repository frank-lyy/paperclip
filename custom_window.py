import rumps
import os
from AppKit import NSStatusBar, NSScreen, NSMakeRect, NSAlert

class CustomWindow(rumps.Window):
    """Base window class that supports setting an icon and custom positioning."""
    
    def __init__(self, *args, **kwargs):
        self.icon_path = kwargs.pop('icon_path', None)
        super().__init__(*args, **kwargs)
        
        # Set the icon if provided
        if self.icon_path and os.path.exists(self.icon_path):
            self.icon = self.icon_path

class InfoWindow:
    """A window for displaying information without text input."""
    
    def __init__(self, message='', title='', icon_path=None):
        self.message = message
        self.title = title
        self.icon_path = icon_path
        
    def run(self):
        alert = NSAlert.alloc().init()
        alert.setMessageText_(self.title)
        alert.setInformativeText_(self.message)
        alert.addButtonWithTitle_("OK")
        
        window = alert.window()
        if window:
            # Get screen dimensions
            screen = NSScreen.mainScreen()
            if screen:
                screen_frame = screen.frame()
                window_frame = window.frame()
                menubar_height = NSStatusBar.systemStatusBar().thickness()
                
                # Position near top-right of screen, below menubar
                new_frame = NSMakeRect(
                    screen_frame.size.width - window_frame.size.width - 20,
                    screen_frame.size.height - menubar_height - window_frame.size.height - 10,
                    window_frame.size.width,
                    window_frame.size.height
                )
                window.setFrame_display_(new_frame, True)
        
        alert.runModal()

class SettingsWindow(CustomWindow):
    """A custom window that supports setting an icon and custom positioning."""
    
    def __init__(self, message='', title='', default_text='', ok=None, cancel=None, dimensions=(320, 160),
                 secure=False, icon_path=None):
        super().__init__(message, title, default_text, ok, cancel, dimensions, secure, icon_path=icon_path)
    
    def run(self):
        print("Running custom window")
        # Create but don't run the alert
        alert = self._alert
        window = alert.window()
        print("Window:", window)
        
        if window:
            # Get screen dimensions
            screen = NSScreen.mainScreen()
            if screen:
                screen_frame = screen.frame()
                window_frame = window.frame()
                menubar_height = NSStatusBar.systemStatusBar().thickness()
                
                # Position near top-right of screen, below menubar
                new_frame = NSMakeRect(
                    screen_frame.size.width - window_frame.size.width - 20,  # 20px from right edge
                    screen_frame.size.height - menubar_height - window_frame.size.height - 10,  # 10px below menubar
                    window_frame.size.width,
                    window_frame.size.height
                )
                window.setFrame_display_(new_frame, True)
        
        # Now run the alert and return the response
        clicked = alert.runModal() % 999
        if clicked > 2 and self._cancel:
            clicked -= 1
        self._textfield.validateEditing()
        text = self._textfield.stringValue()
        self.default_text = self._default_text  # reset default text
        return Response(clicked, text)