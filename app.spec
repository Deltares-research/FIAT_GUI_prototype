# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['FIAT_GUI\\server.py'],
    pathex=["FIAT_GUI"],
    binaries=[],
    datas=[
        ("C:/Users/jong/miniforge/envs/FIAT-GUI/Lib/site-packages/dash_bootstrap_components", "dash_bootstrap_components"),
        ("C:/Users/jong/miniforge/envs/FIAT-GUI/Lib/site-packages/dash", "dash"),
        ("C:/Users/jong/miniforge/envs/FIAT-GUI/Lib/site-packages/visdcc", "visdcc")
        
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [('v', None, 'OPTION')],
    icon="NONE",
    exclude_binaries=True,
    name='FIAT_GUI',
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
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='FIAT_GUI')