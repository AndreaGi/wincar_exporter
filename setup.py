from distutils.core import setup

import os

# Specifiy your ctree root if auto-find doesn't work, for example:
# ctree_ROOT = "/opt/IBM/ctree/V8.1/"
ctreerootdir = "."

def find_ctreelibdir():
    for path in ['lib', 'lib32', 'lib64']:
        if os.path.exists(os.path.join(ctreerootdir, path)):
            return os.path.join(ctreerootdir, path)
    # Give up noisily
    raise Exception('Unable to locate ctsqlapi lib directory')



setup(
    name="pyctree",
    version="0.0.2",
    description = "DB API Module for c-tree ACE SQL",

    long_description = ('A Python DB API 2 module for c-tree ACE SQL. This project provides an interface '
                        'to c-tree ACE SQL.'),
							   
    #author="",
    #author_email="",
    url="http://www.faircom.com",
    #maintainer="",
    #maintainer_email="",
    #license="LGPL",
    package_dir={'pyctree': os.curdir},
    py_modules=['pyctree', 'pyctsqlapi'],
    )

# FIN

