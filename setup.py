from setuptools import setup

APP = ['weather_wire.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'requests',
        'pythonosc',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'typing_extensions'
    ],
    'includes': [
        'datetime',
        'time',
        'json',
        'sys',
        'os'
    ],
    'plist': {
        'LSUIElement': True,  # This makes it a background app
        'CFBundleName': 'The Weather Wire',
        'CFBundleDisplayName': 'The Weather Wire',
        'CFBundleIdentifier': 'com.weatherwire.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2024',
        'LSEnvironment': {
            'PYTHONPATH': '@executable_path/../Resources/lib/python3.9/site-packages/'
        }
    },
    'iconfile': None,  # No icon file needed
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=[
        'requests==2.31.0',
        'python-osc==1.8.1',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'typing_extensions'
    ]
) 