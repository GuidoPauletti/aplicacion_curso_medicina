# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['curso_medicina\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Python311\\tcl\\tcl8.6', './tcl8.6'), ('C:\\Python311\\tcl\\tk8.6', './tk8.6')],
    hiddenimports=['tkinter', 'customtkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='enyn',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='enyn',
)
