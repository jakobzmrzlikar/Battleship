import sys
import os
from cx_Freeze import *

product_name = 'Battleship'

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# http://msdn.microsoft.com/en-us/library/windows/desktop/aa371847(v=vs.85).aspx
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     product_name,             # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]\main.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     "TARGETDIR",               # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"],
                    "include_files":[
                        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                        os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                        ],
                    "excludes": [""]}

bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
    'initial_target_dir': r'[ProgramFilesFolder]\%s' % (product_name),
    # 'includes': ['atexit', 'PySide.QtNetwork'], # <-- this causes error
    'data': msi_data,
    }

# GUI applications require a different base on Windows
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

exe = Executable(script='main.py',
                 base=base,
                 icon='Battleship.ico',
                 shortcutName=product_name,
                 shortcutDir='DesktopFolder'
                )


setup(name=product_name,
      author = "Jakob Zmrzlikar & Jon Mikoš",
      version='1.0',
      description='A simple battleship game with computer opponent.',
      executables=[exe],
      options={
            'bdist_msi': bdist_msi_options,
            'build_exe': build_exe_options,
            })
