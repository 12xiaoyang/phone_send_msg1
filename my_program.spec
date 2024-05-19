# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['./'],  # 确保 PyInstaller 知道项目的根路径
    binaries=[],
    datas=[
        ('config.json', '.'),  # 添加 config.json 文件
        ('get_img_path.py', '.'),  # 添加 get_img_path.py 文件
        ('get_name.py', '.'),  # 添加 get_name.py 文件
        ('send_img_phone.py', '.'),  # 添加 send_img_phone.py 文件
        ('daily_report.txt', '.')  # 添加数据文件
    ],
    hiddenimports=[
        'get_img_path',  # 添加 get_img_path 模块
        'get_name',  # 添加 get_name 模块
        'send_img_phone',  # 添加 send_img_phone 模块
    ],
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
    name='my_program',
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

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='my_program',
)
