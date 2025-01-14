import rumps
import os
from AppKit import (
    NSStatusBar, NSScreen, NSMakeRect, NSAlert, NSApp, NSWindow,
    NSWindowStyleMaskBorderless, NSBackingStoreBuffered,
    NSFloatingWindowLevel, NSColor
)

def create_parent_window():
    """Create an invisible window positioned under the menubar."""
    screen = NSScreen.mainScreen()
    if not screen:
        print("Failed to get main screen")
        return None
        
    screen_frame = screen.frame()
    menubar_height = NSStatusBar.systemStatusBar().thickness()
    
    # Small but non-zero size (1x1 pixel)
    window_width = 1
    window_height = 1
    
    # Position near top-right of screen, below menubar
    x = screen_frame.size.width - window_width - 20
    y = screen_frame.size.height - menubar_height - 10
    print(f"Window position: ({x}, {y})")
    
    # Create a borderless window
    window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
        NSMakeRect(x, y, window_width, window_height),
        NSWindowStyleMaskBorderless,  # No border or title bar
        NSBackingStoreBuffered,
        False
    )
    
    # Make it invisible
    window.setBackgroundColor_(NSColor.clearColor())
    window.setAlphaValue_(0.0)  # Fully transparent
    window.setOpaque_(False)
    window.setHasShadow_(False)  # No shadow
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
            
        # Show the invisible parent window
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
        self._clicked = None
    
    def run(self):
        # Create a default response with the initial text
        response = Response(0, self.default_text)
            
        # Now show it as a sheet on our invisible window
        parent_window = create_parent_window()
        if parent_window is None:
            return response
            
        # Show the invisible parent window
        parent_window.makeKeyAndOrderFront_(None)
        
        # Get the alert from parent class
        alert = self._alert
        
        # Run alert as sheet on parent window and wait for response
        def completion_handler(sheet_response):
            self._clicked = sheet_response
            parent_window.close()
            NSApp.stopModal()
            
        alert.beginSheetModalForWindow_completionHandler_(
            parent_window,
            completion_handler
        )
        
        # Run modal session
        NSApp.runModalForWindow_(parent_window)
        
        # Create response with the clicked value and text
        # print(self._clicked, self._textfield.stringValue())
        if self._clicked is not None:
            response = Response(self._clicked, self._textfield.stringValue())
            
        return response

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