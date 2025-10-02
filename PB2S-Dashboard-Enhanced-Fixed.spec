# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules

datas = []
hiddenimports = ['streamlit.runtime.scriptrunner.magic_funcs', 'streamlit.runtime.caching', 'streamlit.web.bootstrap', 'altair', 'tornado', 'watchdog', 'validators', 'packaging', 'toml', 'requests', 'click', 'pydeck', 'pyarrow', 'protobuf']
datas += collect_data_files('streamlit')
hiddenimports += collect_submodules('streamlit')


a = Analysis(
    ['pb2s_dashboard.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.binaries,
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
)
