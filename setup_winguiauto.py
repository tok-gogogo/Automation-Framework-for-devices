from distutils.core import setup
#import xlwt
import xlrd
import py2exe
import glob

#setup(name        = 'rssid',
setup(name        = 'winGuiAuto.py',
      version     = '1.0',
      console     = ["winGuiAuto.py",{"script":"winGuiAuto.py","icon_resources":[(1, "simuTool.ico")]}],
      #console     = ["rssid.py",{"script":"rssid.py","icon_resources":[(1, "simuTool.ico")]}],
      options     = {'py2exe' : {'packages' : ['xlrd','pywinauto'],
                                'includes': ['xlrd','pywinauto'],
                                }
                    },
      description = "zhongtai autoTool",
      data_files  = [("image",glob.glob("image\\*")),
                    ("protocol",glob.glob("protocol\\*")),
                    ("testdata",glob.glob("testdata\\*"))
                    ]
                    )