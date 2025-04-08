# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files
import os
import sys

# Configuración manual de rutas (¡CAMBIAR ESTA RUTA!)
PROJECT_PATH = r'C:\Users\Admin\Documents\GitHub\programa_recepcion_kia'

a = Analysis(
    ['main.py'],
    pathex=[
        PROJECT_PATH,
        os.path.join(PROJECT_PATH, 'controllers')
    ],
    binaries=[],
    datas=[
        (os.path.join(PROJECT_PATH, 'key.json'), '.'),
        *collect_data_files('google')
    ],
    hiddenimports=[
        'controllers.citas_controller',
        'google.auth',
        'google_auth_httplib2',
        'pandas'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='programa_recepcion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Cambiar a True si necesitas ver la consola
    icon=None
)