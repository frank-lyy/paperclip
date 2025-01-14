import rumps
import os
from AppKit import (
    NSStatusBar, NSScreen, NSMakeRect, NSAlert, 
    NSApp, NSWindow, NSWindowStyleMaskTitled,
    NSWindowStyleMaskClosable, NSBackingStoreBuffered,
    NSFloatingWindowLevel
)

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
        # Create a custom window
        screen = NSScreen.mainScreen()
        if not screen:
            # Fallback to NSAlert if we can't get screen info
            alert = NSAlert.alloc().init()
            alert.setMessageText_(self.title)
            alert.setInformativeText_(self.message)
            alert.addButtonWithTitle_("OK")
            alert.runModal()
            return

        screen_frame = screen.frame()
        window_width = 300
        window_height = 200
        menubar_height = NSStatusBar.systemStatusBar().thickness()
        
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
        
        window.setTitle_(self.title)
        window.setLevel_(NSFloatingWindowLevel)
        window.center()  # This will center the window
        
        # Make the window key and order front
        window.makeKeyAndOrderFront_(None)
        NSApp.activateIgnoringOtherApps_(True)
        
        # Run modal for window
        NSApp.runModalForWindow_(window)
        
        # Clean up
        window.orderOut_(None)
        NSApp.stopModal()

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
                    screen_frame.size.width - window_frame.size.width - 20,
                    screen_frame.size.height - menubar_height - window_frame.size.height - 10,
                    window_frame.size.width,
                    window_frame.size.height
                )
                print("New frame:", new_frame)
                window.setFrame_display_(new_frame, True)
        
        # Now run the alert and return the response
        clicked = alert.runModal()
        if clicked > 2 and self._cancel:
            clicked -= 1
        self._textfield.validateEditing()
        text = self._textfield.stringValue()
        self.default_text = self._default_text  # reset default text
        return Response(clicked, text)


class Response(object):
    """Holds information from user interaction with a :class:`rumps.Window` after it has been closed."""

    def __init__(self, clicked, text):
        self._clicked = clicked
        self._text = text

    def __repr__(self):
        shortened_text = self._text if len(self._text) < 21 else self._text[:17] + '...'
        return '<{0}: [clicked: {1}, text: {2}]>'.format(type(self).__name__, self._clicked, repr(shortened_text))

    @property
    def clicked(self):
        """Return a number representing the button pressed by the user."""
        return self._clicked

    @property
    def text(self):
        """Return the text collected from the user."""
        return self._text