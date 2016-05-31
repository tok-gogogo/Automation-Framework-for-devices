from distutils.core import setup
#import xlwt
import xlrd
import py2exe
import glob
from distutils.core import setup
import py2exe
import glob
import os
mfcdir = 'C:\\Python27\\Lib\\site-packages\\pythonwin'
mfcfiles = [os.path.join(mfcdir, i) for i in ["mfc90.dll", "mfc90u.dll", "mfcm90.dll", "mfcm90u.dll", 
                                              "Microsoft.VC90.MFC.manifest"]]

#setup(name        = 'script_check3',
setup(name        = 'simuTool_server',
      version     = '1.0',
      console     = ["session.py",{"script":"session.py","icon_resources":[(1, "simuTool.ico")]}],
      #console     = ["script_check3.py",{"script":"script_check3.py","icon_resources":[(1, "simuTool.ico")]}],
      options     = {'py2exe' : {'packages' : ['xlrd','pywinauto'],
                                'includes': ['xlrd','pywinauto'],
                                }
                    },
      description = "gaoruishixu",
      data_files  = [("image",glob.glob("image\\*")),
                    ("protocol",glob.glob("protocol\\*")),
                    ("testdata",glob.glob("testdata\\*")),
                    ("Microsoft.VC90.MFC", mfcfiles)
                    ]
                    )
