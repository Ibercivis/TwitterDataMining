#!/usr/bin/env python
# Got from Digenpy's setup.py (http://github.com/XayOn/Digenpy)
from distutils.core import setup
import os, shutil

scripts=['TwitterDataMiner', 'TwitterDataMinerHelper' ]
if os.name is not "posix":
    if os.name is "nt":
        import py2exe
    shutil.copyfile('TwitterDataMiner','TwitterDataMiner.py')
    scripts=['TwitterDataMiner.py', 'TwitterDataMinerHelper.py']

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
            'packages': ['RLT', 'twitter'],
            }
        }

setup(name='TwitterDataMiner',
      version='0.3',
      download_url='https://github.com/Ibercivis/TwitterDataMining/downloads',
      requires=['MySQL_python', 'argparse', 'python_twitter'],
      platforms=['all'],
      long_description='Twitter data mining scripts, able to save into mysql, sqlite, or json format',
      license='GPL2+',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
      ],
      mantainer='David Francos Cuartero (XayOn)',
      mantainer_email='xayon@xayon.net',
      description='Twitter data mining scripts ',
      author='David Francos Cuartero (XayOn)',
      console = [{"script": "TwitterDataMiner" }],
      author_email='xayon@xayon.net',
      url='http://github.com/Ibercivis/TwitterDataMining',
      packages=['RLT'],
      scripts=scripts,
      options=opts,
     )

