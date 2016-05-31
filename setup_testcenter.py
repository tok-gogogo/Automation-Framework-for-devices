from distutils.core import setup
#import xlwt
import xlrd
import py2exe
import glob

#setup(name        = 'script_check3',
setup(name        = 'testcenter',
      version     = '1.0',
      console     = ["stc_load_op.py",{"script":"stc_load_op.py","icon_resources":[(1, "simuTool.ico")]}],
      #console     = ["script_check3.py",{"script":"script_check3.py","icon_resources":[(1, "simuTool.ico")]}],
      options     = {'py2exe' : {'packages' : ['xlrd','pywinauto'],
                                'includes': ['xlrd','pywinauto'],
                                }
                    },
      description = "cykj autoTool",
      data_files  = [("image",glob.glob("image\\*")),
                    ("protocol",glob.glob("protocol\\*")),
                    ("testdata",glob.glob("testdata\\*"))
                    ]
                    )
