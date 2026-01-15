# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/joeywalter/antigravity-nexus/shader_overlay/index.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/spline.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/snippets.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/blueprint.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/ecs_sim.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/sdf_graph.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/level_stream.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/editor_ui.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/unreal_stream.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/sonar_xr.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/asset_explorer.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/mesh_volume.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/native_stack_viz.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/sim_vs_stream.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/git_timemachine.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/java_monitor.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/live_scratchpad.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/mobile_sync.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/extensions_launcher.html', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/theme.css', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/three.min.js', '.'), ('/Users/joeywalter/antigravity-nexus/shader_overlay/unreal_asset_thumbnails_1768423247157.png', '.')],
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
    name='UnrealTacticalSuite',
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
    icon=['/Users/joeywalter/antigravity-nexus/shader_overlay/ue_app_icon_1768423980485.png'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='UnrealTacticalSuite',
)
app = BUNDLE(
    coll,
    name='UnrealTacticalSuite.app',
    icon='/Users/joeywalter/antigravity-nexus/shader_overlay/ue_app_icon_1768423980485.png',
    bundle_identifier=None,
)
