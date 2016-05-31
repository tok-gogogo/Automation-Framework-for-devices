from distutils.core import setup
import py2exe
import glob

setup(name        = 'ping.py',
      version     = '1.0',
      console     = ["rw_Excel_FLOW.py",{"script":"rw_Excel_FLOW.py","icon_resources":[(1, "simuTool.ico")]}],
      description = "zhongtai autoTool",
      data_files  = [("image",glob.glob("image\\*")),
                    ("protocol",glob.glob("protocol\\*")),
                    ("testdata",glob.glob("testdata\\*")),])

