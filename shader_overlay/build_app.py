import PyInstaller.__main__
import os

# Define assets to include
assets = [
    ('index.html', '.'),
    ('spline.html', '.'),
    ('snippets.html', '.'),
    ('blueprint.html', '.'),
    ('ecs_sim.html', '.'),
    ('sdf_graph.html', '.'),
    ('level_stream.html', '.'),
    ('editor_ui.html', '.'),
    ('unreal_stream.html', '.'),
    ('sonar_xr.html', '.'),
    ('asset_explorer.html', '.'),
    ('mesh_volume.html', '.'),
    ('native_stack_viz.html', '.'),
    ('sim_vs_stream.html', '.'),
    ('git_timemachine.html', '.'),
    ('java_monitor.html', '.'),
    ('live_scratchpad.html', '.'),
    ('mobile_sync.html', '.'),
    ('extensions_launcher.html', '.'),
    ('theme.css', '.'),
    ('three.min.js', '.'),
    ('unreal_asset_thumbnails_1768423247157.png', '.'),
]

# Build command parts
datas = [f"{os.path.abspath(src)}:{dst}" for src, dst in assets]
icon_path = os.path.abspath("ue_app_icon_1768423980485.png")

PyInstaller.__main__.run([
    'main.py',
    '--name=UnrealTacticalSuite',
    '--windowed',
    '--noconfirm',
    '--clean',
    f'--icon={icon_path}',
    *[f'--add-data={d}' for d in datas],
])
