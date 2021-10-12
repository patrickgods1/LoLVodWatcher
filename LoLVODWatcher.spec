# -*- mode: python -*-

block_cipher = None


a = Analysis(['LoLVODWatcher.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='LoLVODWatcher v0.13',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )

import shutil
shutil.copyfile('config.ini', f'{DISTPATH}/config.ini')
shutil.copyfile('chromedriver.exe', f'{DISTPATH}/chromedriver.exe')
shutil.copyfile('geckodriver.exe', f'{DISTPATH}/geckodriver.exe')
