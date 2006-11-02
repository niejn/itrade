#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# ============================================================================
# Project Name : iTrade
# Module Name  : setup.py
#
# Description: Setup for py2exe
#
# The Original Code is iTrade code (http://itrade.sourceforge.net).
#
# The Initial Developer of the Original Code is	Gilles Dumortier.
#
# Portions created by the Initial Developer are Copyright (C) 2004-2006 the
# Initial Developer. All Rights Reserved.
#
# Contributor(s):
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see http://www.gnu.org/licenses/gpl.html
#
# History       Rev   Description
# 2005-10-15    dgil  Wrote it from scratch
# ============================================================================

# ============================================================================
# Imports
# ============================================================================

from distutils.core import setup
import glob
import py2exe

# ============================================================================

from distutils.filelist import findall
import os
import matplotlib
matplotlibdatadir = matplotlib.get_data_path()
matplotlibdata = findall(matplotlibdatadir)

matplotlibdata_files =[("cache",[]),
            ("alerts",[]),
            ("data",["data/quotes.txt","data/closed.txt","data/fr.messages.txt","data/us.messages.txt"]),
            ("images",glob.glob("images\\*.gif")),
            ("res",glob.glob("res\\*.*")),
            ("usrdata",["usrdata/portfolio.txt","usrdata/default.matrix.txt","usrdata/default.operations.txt","usrdata/default.stops.txt"]),
           ]


for f in matplotlibdata:
    dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
    matplotlibdata_files.append((os.path.split(dirname)[0], [f]))

# ============================================================================
# setup
#
# usage: python setup.py py2exe
# ============================================================================

setup(windows=["itrade.py"],
      data_files=matplotlibdata_files,
      options = {"py2exe":
                 {"packages": ['matplotlib','pytz'],
                  "excludes": ['_gtkagg', '_tkagg', '_svg','_ps',"Tkconstants","Tkinter","tcl"],
                  "dll_excludes": ['libgdk_pixbuf-2.0-0.dll','libgdk-win32-2.0-0.dll','libgobject-2.0-0.dll','wxmsw26uh_vc.dll','gdiplus.dll'],
                  "bundle_files": 2,
                  "optimize":2
                  }
                },
)


# ============================================================================
# That's all folks !
# ============================================================================
