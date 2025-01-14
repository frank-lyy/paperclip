# import rumps
# import os
# from Foundation import NSMakeRect
# from AppKit import (
#     NSWindow,
#     NSPanel,
#     NSFloatingWindowLevel,
#     NSWindowStyleMaskTitled,
#     NSWindowStyleMaskClosable,
#     NSImage,
#     NSApp,
#     NSStatusBar,
#     NSBitmapImageRep
# )

# class CustomWindow(rumps.Window):
#     def __init__(self, *args, **kwargs):
#         self.icon_path = kwargs.pop('icon_path', None)
#         super().__init__(*args, **kwargs)
    
#     def _cancel(self, *args):
#         self._response = None
#         self._cancel_button.setEnabled_(True)
#         NSApp.stopModal()
    
#     def _ok(self, *args):
#         self._response = True
#         self._ok_button.setEnabled_(True)
#         NSApp.stopModal()
    
#     def run(self):
#         alert = self._alert()  # This creates the window
#         self._window = alert.window()
        
#         # Make it a floating panel and set window level
#         self._window.setLevel_(NSFloatingWindowLevel)
#         self._window.setStyleMask_(NSWindowStyleMaskTitled | NSWindowStyleMaskClosable)
        
#         # Set custom icon if provided
#         if self.icon_path and os.path.exists(self.icon_path):
#             icon = NSImage.alloc().initWithContentsOfFile_(self.icon_path)
#             if icon:
#                 # For SVG files, we need to ensure proper sizing
#                 icon.setSize_((16, 16))  # Standard size for window icons
#                 self._window.standardWindowButton_(1).setImage_(icon)  # 1 is the close button
        
#         # Position window below the menubar
#         self.position_below_menubar()
        
#         alert.layout()
#         NSApp.runModalForWindow_(alert.window())
        
#         return self._response
    
#     def position_below_menubar(self):
#         if not hasattr(self, '_window'):
#             return
            
#         # Get the menubar height and screen frame
#         menubar_height = NSStatusBar.systemStatusBar().thickness()
#         screen_frame = NSApp.mainScreen().frame()
        
#         # Get our window's frame
#         window_frame = self._window.frame()
        
#         # Calculate the x position to center under the menubar icon
#         # This is an approximation since we can't get the exact menubar item position
#         x = screen_frame.size.width - window_frame.size.width - 20
        
#         # Position right below the menubar
#         new_frame = NSMakeRect(
#             x,
#             screen_frame.size.height - menubar_height - window_frame.size.height,
#             window_frame.size.width,
#             window_frame.size.height
#         )
        
#         # Set the new position
#         self._window.setFrame_display_animate_(new_frame, True, True)