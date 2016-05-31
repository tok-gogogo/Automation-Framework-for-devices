from distutils.core import setup
import py2exe
import glob

setup(name        = 'rssid.py',
      version     = '1.0',
      console     = ["rssid.py",{"script":"rssid.py","icon_resources":[(1, "simuTool.ico")]}],
      description = "zhongtai autoTool",
      options     = {'py2exe' : {'packages' : ['xlrd','pywinauto'],
                                'includes': ['xlrd','pywinauto'],
                                }
                    },
      data_files  = [("image",glob.glob("image\\*")),
                    ("protocol",glob.glob("protocol\\*")),
                    ("testdata",glob.glob("testdata\\*")),])

