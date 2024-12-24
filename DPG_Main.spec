# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['DPG_Main.py'],
    pathex=[],
    binaries=[],
    datas=[('Resources.dat','.'),('Facility.dat','.'),
			('ManifoldSpark.ico','.'),('OpenSans-VariableFont_wdth,wght.ttf','.')],
    hiddenimports=["pywin32","win32gui"],
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
    name='ManifoldSpark',
    debug=False,
	clean = True,
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
	icon = "./ManifoldSpark.ico"
)
