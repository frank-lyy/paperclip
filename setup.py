from setuptools import setup

APP = ['menubar_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # This makes it a "background" app without a dock icon
        'CFBundleName': 'Paperclip Counter',
        'CFBundleDisplayName': 'Paperclip Counter',
        'CFBundleGetInfoString': "Track your daily tasks",
        'CFBundleIdentifier': "com.paperclip.counter",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2025, Your Name, All Rights Reserved"
    },
    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
