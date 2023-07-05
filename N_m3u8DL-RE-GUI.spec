# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['index.py'],
    pathex=[],
    binaries=[('./bin/*', './bin/')],
    datas=[],
    hiddenimports=['desktop_notifier.resources'],
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
    [],
    exclude_binaries=True,
    name='N_m3u8DL-RE-GUI',
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
    icon=['logo/logo.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='N_m3u8DL-RE-GUI',
)
app = BUNDLE(
    coll,
    name='N_m3u8DL-RE-GUI.app',
    icon='./logo/logo.icns',
    bundle_identifier=None,
)
