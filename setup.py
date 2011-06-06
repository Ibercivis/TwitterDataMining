#!/usr/bin/env python
# Got from Digenpy's setup.py (http://github.com/XayOn/Digenpy)
from distutils.core import setup
import sys, os, shutil

scripts=['RealLifeTwitter']
if os.name is not "posix":
    if os.name is "nt":
        import py2exe
    shutil.copyfile('RealLifeTwitter','RealLifeTwitter.py')
    scripts=['RealLifeTwitter']

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

setup(name='RealLifeTwitter',
      version='0.1.1',
      download_url='https://github.com/XayOn/RealLifeTwitter/downloads',
      requires=['MySQL_python','argparse', 'python_twitter'],
      platforms=['all'],
      long_description='Generate stickers from twitter data. Able to save and read it from multiple sources',
      license='GPL2+',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
      ],
      mantainer='David Francos Cuartero (XayOn)',
      mantainer_email='xayon@xayon.net',
      description='Twitter stickers generator ',
      author='David Francos Cuartero (XayOn)',
      console = [{"script": "TwitterDataMiner" }],
      author_email='xayon@xayon.net',
      url='http://github.com/Ibercivis/TwitterDataMining',
      packages=['RLT'],
      scripts=scripts,
      options=opts,
     )


