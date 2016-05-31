from distutils.core import setup
from pywinauto import *
import py2exe
import glob

setup(name        = 'win_GUI.py',
      version     = '1.0',
      console     = ["win_GUI.py",{"script":"win_GUI.py","icon_resources":[(1, "simuTool.ico")]}],
      description = "zhongtai autoTool",
      options     = {'py2exe' : {'packages' : ['xlrd','pywinauto'],
                                'includes': ['xlrd','pywinauto'],
                                }
                     },
      data_files  = [("image",glob.glob("image\\*")),
                    ("protocol",glob.glob("protocol\\*")),
                    ("testdata",glob.glob("testdata\\*")),])

