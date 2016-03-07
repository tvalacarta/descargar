from kivy.deps import sdl2, glew
# -*- mode: python -*-

block_cipher = None


a = Analysis(['c:\\Users\\Jesus\\Downloads\\descargar-master\\aragontv\\main.py'],
             pathex=['C:\\Users\\Jesus\\Downloads\\descargar-master\\dist'],
             binaries=None,
             datas=None,
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
          exclude_binaries=True,
          name='Descargar_de_Aragon_TV',
          debug=False,
          strip=False,
          upx=True,
          console=True , manifest='data\\icon.ico')
coll = COLLECT(exe, Tree('c:\\Users\\Jesus\\Downloads\\descargar-master\\aragontv\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Descargar_de_Aragon_TV')
