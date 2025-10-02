# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect Streamlit data files and metadata
streamlit_datas = collect_data_files('streamlit')

# Additional hidden imports for Streamlit
streamlit_hiddenimports = [
    'streamlit.runtime.scriptrunner.magic_funcs',
    'streamlit.runtime.caching.cache_data_api',
    'streamlit.runtime.caching.cache_resource_api',
    'streamlit.runtime.caching.storage.dummy_cache_storage',
    'streamlit.runtime.caching.storage.local_disk_cache_storage',
    'streamlit.runtime.legacy_caching.caching',
    'streamlit.runtime.media_file_manager',
    'streamlit.runtime.uploaded_file_manager',
    'streamlit.web.bootstrap',
    'streamlit.web.server.server',
    'streamlit.web.server.server_util',
    'streamlit.web.server.websocket_headers',
    'streamlit.web.cli',
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
    'watchdog',
    'watchdog.observers',
    'validators',
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
    'toml',
    'requests',
    'urllib3',
    'urllib3.util',
    'urllib3.util.ssl_',
    'urllib3.contrib.pyopenssl',
    'certifi',
    'chardet',
    'idna',
    'click',
    'click.core',
    'pydeck',
    'pydeck.bindings',
    'gitpython',
    'git',
    'blinker',
    'cachetools',
    'pyarrow',
    'protobuf',
    'tzlocal',
    'rich',
    'rich.console',
    'rich.text',
    'pillow',
    'PIL',
    'PIL.Image',
    'numpy',
    'pandas',
    'matplotlib',
    'matplotlib.pyplot',
    'plotly',
    'plotly.graph_objects',
    'plotly.express'
]

# Core application hidden imports
core_hiddenimports = [
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
    'logging'
]

all_hiddenimports = streamlit_hiddenimports + core_hiddenimports

block_cipher = None

a = Analysis(
    ['pb2s_dashboard.py'],
    pathex=[],
    binaries=[],
    datas=streamlit_datas + [
        ('C:\\Users\\UnknwN\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\streamlit\\static', 'streamlit/static'),
        ('C:\\Users\\UnknwN\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\streamlit\\runtime', 'streamlit/runtime'),
        ('C:\\Users\\UnknwN\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\altair\\vegalite', 'altair/vegalite'),
    ],
    hiddenimports=all_hiddenimports,
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
    name='PB2S-Dashboard-Enhanced-Fixed',
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