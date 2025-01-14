import rumps
import os
from AppKit import (
    NSStatusBar, NSScreen, NSMakeRect, NSAlert, NSApp, NSWindow,
    NSWindowStyleMaskTitled, NSWindowStyleMaskClosable, NSBackingStoreBuffered,
    NSFloatingWindowLevel
)

def create_parent_window():
    """Create a window positioned under the menubar."""
    screen = NSScreen.mainScreen()
    if not screen:
        print("Failed to get main screen")
        return None
        
    screen_frame = screen.frame()
    menubar_height = NSStatusBar.systemStatusBar().thickness()
    
    # Create a small window
    window_width = 1
    window_height = 1
    
    # Position near top-right of screen, below menubar
    x = screen_frame.size.width - window_width - 20
    y = screen_frame.size.height - menubar_height - window_height - 10
    
    # Create the window
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(x, y, window_width, window_height),
        NSWindowStyleMaskTitled | NSWindowStyleMaskClosable,
        NSBackingStoreBuffered,
        False
    )
    window.setLevel_(NSFloatingWindowLevel)
    
    return window

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

        self._alert = NSAlert.alloc().init()
        self._alert.setMessageText_(title)
        self._alert.setInformativeText_(message)
        self._alert.addButtonWithTitle_("OK")
        
    def run(self):
        alert = self._alert
        
        # Create and show parent window
        parent_window = create_parent_window()
        if parent_window is None:
            # Fallback to regular modal if we can't create parent window
            alert.runModal()
            return
            
        # Show the parent window
        parent_window.makeKeyAndOrderFront_(None)
        
        # Run alert as sheet on parent window
        alert.beginSheetModalForWindow_completionHandler_(
            parent_window,
            lambda response: parent_window.close()  # Close parent window when done
        )

class SettingsWindow(CustomWindow):
    """A custom window that supports setting an icon and custom positioning."""
    
    def __init__(self, message='', title='', default_text='', ok=None, cancel=None, dimensions=(320, 160),
                 secure=False, icon_path=None):
        super().__init__(message, title, default_text, ok, cancel, dimensions, secure, icon_path=icon_path)
    
    def run(self):
        alert = self._alert
        
        # Create and show parent window
        parent_window = create_parent_window()
        if parent_window is None:
            # Fallback to regular modal if we can't create parent window
            clicked = alert.runModal()
        else:
            # Show the parent window
            parent_window.makeKeyAndOrderFront_(None)
            
            # Run alert as sheet on parent window
            def completion_handler(response):
                nonlocal clicked
                clicked = response
                parent_window.close()
                
            clicked = None
            alert.beginSheetModalForWindow_completionHandler_(
                parent_window,
                completion_handler
            )
            
            # Wait for completion
            while clicked is None:
                NSApp.runModalForWindow_(parent_window)
            
        if clicked > 2 and self._cancel:
            clicked -= 1
        self._textfield.validateEditing()
        text = self._textfield.stringValue()
        self.default_text = self._default_text
        parent_window.close()
        return Response(clicked, text)


class Response(object):
    """Holds information from user interaction with a Window after it has been closed."""

    def __init__(self, clicked, text):
        self._clicked = clicked
        self._text = text

    def __repr__(self):
        shortened_text = self._text if len(self._text) < 21 else self._text[:17] + '...'
        return '<{0}: [clicked: {1}, text: {2}]>'.format(type(self).__name__, self._clicked, repr(shortened_text))

    @property
    def clicked(self):
        return self._clicked

    @property
    def text(self):
        return self._text