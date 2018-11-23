# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)
block_cipher = None


a = Analysis(['pricedelta.py'],
             pathex=['D:\\PythonSpace\\FuturesPrice'],
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
          name='pricedelta',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
