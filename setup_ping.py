from distutils.core import setup
import py2exe
import glob
import os
mfcdir = 'C:\\Python27\\Lib\\site-packages\\pythonwin'
mfcfiles = [os.path.join(mfcdir, i) for i in ["mfc90.dll", "mfc90u.dll", "mfcm90.dll", "mfcm90u.dll", 
                                              "Microsoft.VC90.MFC.manifest"]]
setup(name        = 'simuTool_server',
      version     = '1.0',
      console     = ["ping.py",{"script":"ping.py","icon_resources":[(1, "simuTool.ico")]}],
      description = "zhongtai autoTool",
      data_files  = [("image",glob.glob("image\\*")),
                    ("protocol",glob.glob("protocol\\*")),
                    ("testdata",glob.glob("testdata\\*")),])

