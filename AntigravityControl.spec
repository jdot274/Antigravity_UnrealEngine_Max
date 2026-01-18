# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tools/dashboard/nexus_dashboard.py'],
    pathex=['tools/dashboard/.venv/lib/python3.14/site-packages'],
    binaries=[],
    datas=[('tools/dashboard/nexus-web-view/dist', 'nexus-web-view/dist')],
    hiddenimports=[],
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
    name='AntigravityControl',
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
    icon=['tools/gemini-vscode-extension/assets/icon_neon_variant.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AntigravityControl',
)
app = BUNDLE(
    coll,
    name='AntigravityControl.app',
    icon='tools/gemini-vscode-extension/assets/icon_neon_variant.png',
    bundle_identifier=None,
)
