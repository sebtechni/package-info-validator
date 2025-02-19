# -*- mode: python ; coding: utf-8 -*-

import os
import sys

#APP NAME
APP_NAME = "Package Checker"
COMPANY = "difuze"
ICONS = False

ICON_PATH = None

if ICONS:
    if os.name == 'nt': # Windows
        ICON_PATH = 'icons/windows/icon.ico'
    elif sys.platform == 'linux': # Linux
        ICON_PATH = 'icons/linux/icon.png'
    elif sys.platform == 'darwin': # macOS
        ICON_PATH = 'icons/macos/icon.icns'

current_dir = os.path.dirname(os.path.realpath(__name__))

block_cipher = None
a = Analysis(
    ['run.py'],
    pathex=[current_dir],
    binaries=[],
    datas=[('templates','templates')],
    upx=True,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    optimize=0,
    cypher=block_cipher,
    noarchive=False,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='run',
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
)

app = BUNDLE(exe,
             name=f'{APP_NAME}.app', 
             icon=ICON_PATH,
             bundle_identifier=f"com.{COMPANY}.{APP_NAME}")