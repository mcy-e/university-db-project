# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None

# Set up paths
app_dir = Path(SPECPATH)
project_root = app_dir.parent

# 1. Define your base data files
added_datas = [
    (str(app_dir / 'GUI' / 'UI'), 'GUI/UI'),
    (str(app_dir / 'GUI' / 'UI' / 'IMAGES'), 'GUI/UI/IMAGES'), 
    (str(app_dir / 'GUI' / 'styling'), 'GUI/styling'),
    (str(app_dir / 'Translations'), 'Translations'),
]

# 2. Safely add the .env file only if it exists to avoid NoneType errors
# Since .env is in the same folder as the .spec file, we use app_dir
env_path = app_dir / '.env'
if env_path.exists():
    added_datas.append((str(env_path), '.'))
    print(f"INFO: Successfully added .env to bundle from {env_path}")
else:
    print("WARNING: .env file not found in Application folder. It will not be bundled.")

a = Analysis(
    [str(app_dir / 'main.py')],
    pathex=[str(project_root), str(app_dir)],
    binaries=[],
    datas=added_datas,
    hiddenimports=[
        'PyQt6.QtCore', 
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'psycopg2', 
        'psycopg2.pool', 
        'dotenv',
        'Database.connection', 
        'Database.database',
        'GUI.main_window', 
        'GUI.screens', 
        'GUI.crud',
        'GUI.academic', 
        'GUI.performance', 
        'GUI.queries',
        'GUI.results', 
        'GUI.audit', 
        'GUI.settings',
        'UTILS.log', 
        'UTILS.screen_enum', 
        'UTILS.constriants',
        'config',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='UniversityManagement',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(app_dir / 'GUI' / 'UI' / 'IMAGES' / 'logo.ico')
)