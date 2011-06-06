#!/usr/bin/env python
# Got from Digenpy's setup.py (http://github.com/XayOn/Digenpy)
from distutils.core import setup
import sys, os, shutil

scripts=['TwitterDataMiner']
if os.name is not "posix":
    if os.name is "nt":
        import py2exe
    shutil.copyfile('digenpy','digenpy.py')
    shutil.copyfile('digenpy-gtk','digenpy-gtk.py')
    shutil.copyfile('digenpy-gtk','digenpy-gtk.py')
    scripts=['digenpy.py', 'digenpy-gtk.py']

opts = {
    "py2exe": {
        'includes': '',
        "excludes": "cairo, gtk,atk,gdk",
        "dll_excludes": [
        "iconv.dll","intl.dll","libatk-1.0-0.dll",
        "libgdk_pixbuf-2.0-0.dll","libgdk-win32-2.0-0.dll",
        "libglib-2.0-0.dll","libgmodule-2.0-0.dll",
        "libgtk-win32-2.0-0.dll","libpango-1.0-0.dll",
        "libpangowin32-1.0-0.dll"],
        'packages': ['RLT'],
        }
    }

setup(name='TwitterDataMiner',
      version='0.1',
      description='Twitter data mining scripts ',
      author='David Francos Cuartero (XayOn)',
      console = [{"script": "TwitterDataMiner" }],
      author_email='xayon@xayon.net',
      url='http://github.com/Ibercivis/TwitterDataMiner',
      packages=['RLT'],
      scripts=scripts,
      options=opts,
     )


