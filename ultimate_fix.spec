# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Define paths
python_path = r'C:\Users\UnknwN\AppData\Local\Programs\Python\Python313'
site_packages = os.path.join(python_path, 'Lib', 'site-packages')

# Collect all Streamlit files
streamlit_datas = collect_data_files('streamlit')

# Add specific metadata files
metadata_datas = []
try:
    # Try to include metadata files
    import importlib.metadata
    dist_packages = [
        'streamlit', 'altair', 'pandas', 'numpy', 'tornado', 'watchdog', 
        'validators', 'packaging', 'toml', 'requests', 'click', 'pydeck', 
        'pyarrow', 'protobuf', 'pillow', 'matplotlib', 'plotly'
    ]
    
    for pkg in dist_packages:
        try:
            dist_info_path = os.path.join(site_packages, f"{pkg}.dist-info")
            if os.path.exists(dist_info_path):
                metadata_datas.append((dist_info_path, f"{pkg}.dist-info"))
            
            # Also try with underscores
            dist_info_path = os.path.join(site_packages, f"{pkg.replace('-', '_')}.dist-info")
            if os.path.exists(dist_info_path):
                metadata_datas.append((dist_info_path, f"{pkg.replace('-', '_')}.dist-info"))
                
        except Exception:
            continue
            
except Exception:
    pass

# Hidden imports
hiddenimports = [
    'streamlit',
    'streamlit._version',
    'streamlit.version',
    'streamlit.runtime',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.scriptrunner.magic_funcs',
    'streamlit.runtime.caching',
    'streamlit.runtime.caching.cache_data_api',
    'streamlit.runtime.caching.cache_resource_api',
    'streamlit.runtime.media_file_manager',
    'streamlit.runtime.uploaded_file_manager',
    'streamlit.web',
    'streamlit.web.bootstrap',
    'streamlit.web.server',
    'streamlit.web.server.server',
    'streamlit.web.server.server_util',
    'streamlit.web.server.websocket_headers',
    'streamlit.web.cli',
    'streamlit.components',
    'streamlit.components.v1',
    'streamlit.components.v1.components',
    'streamlit.hello',
    'streamlit.hello.hello',
    'streamlit.testing',
    'streamlit.testing.v1',
    'streamlit.external',
    'altair',
    'altair.vegalite',
    'altair.vegalite.v4',
    'altair.vegalite.v4.api',
    'altair.vegalite.v4.schema',
    'altair.utils',
    'altair.utils.core',
    'tornado',
    'tornado.web',
    'tornado.websocket',
    'tornado.httpserver',
    'tornado.ioloop',
    'tornado.platform',
    'tornado.platform.windows',
    'watchdog',
    'watchdog.observers',
    'watchdog.observers.winapi',
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
    'toml',
    'requests',
    'requests.adapters',
    'requests.auth',
    'requests.cookies',
    'requests.models',
    'requests.sessions',
    'urllib3',
    'urllib3.util',
    'urllib3.util.ssl_',
    'urllib3.contrib',
    'certifi',
    'chardet',
    'idna',
    'click',
    'click.core',
    'pydeck',
    'pydeck.bindings',
    'pyarrow',
    'pyarrow.lib',
    'pyarrow.parquet',
    'pillow',
    'PIL',
    'PIL.Image',
    'PIL.ImageTk',
    'numpy',
    'pandas',
    'matplotlib',
    'matplotlib.pyplot',
    'matplotlib.backends',
    'matplotlib.backends.backend_tkagg',
    'plotly',
    'plotly.graph_objects',
    'plotly.express',
    'fastapi',
    'uvicorn',
    'pydantic',
    'paho.mqtt',
    'paho.mqtt.client',
    'json',
    'hashlib',
    'uuid',
    'time',
    'datetime',
    'os',
    'sys',
    'logging',
    'importlib',
    'importlib.metadata',
    'importlib.util',
    'importlib.resources',
    'streamlit_fix_hook'
]

# Data files
all_datas = streamlit_datas + metadata_datas + [
    ('streamlit_fix_hook.py', '.'),
]

# Try to add specific Streamlit static files
streamlit_static = os.path.join(site_packages, 'streamlit', 'static')
if os.path.exists(streamlit_static):
    all_datas.append((streamlit_static, 'streamlit/static'))

streamlit_runtime = os.path.join(site_packages, 'streamlit', 'runtime')
if os.path.exists(streamlit_runtime):
    all_datas.append((streamlit_runtime, 'streamlit/runtime'))

block_cipher = None

a = Analysis(
    ['pb2s_dashboard.py'],
    pathex=[],
    binaries=[],
    datas=all_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate data files
seen = set()
unique_datas = []
for item in a.datas:
    if item[1] not in seen:
        seen.add(item[1])
        unique_datas.append(item)
a.datas = unique_datas

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PB2S-Dashboard-Ultimate-Fix',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)