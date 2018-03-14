# This file is part of Cantera. See License.txt in the top-level directory or
# at http://www.cantera.org/license.txt for license and copyright information.

import string
import os, sys
import types, traceback

try:
    if sys.version_info[0] == 3:
        import tkinter as tk
        from tkinter import messagebox
    else:
        import Tkinter as tk
        import tkMessageBox as messagebox
    _hasTk = 1
except:
    _hasTk = 0


def write_CSV(f, x):
    """write list x to file f in comma-separated-value format."""
    for e in x:
        f.write(repr(e) + ',')
    f.write('\n')


def _print_value(name, value, unitstr):
    print(string.rjust(name, 15) + string.rjust('%10.5e' % value, 15) + ' ' +
          string.ljust(unitstr, 5))

def handleError(message = '<error>', window=None, fatal=0, warning=0, options=None):
    """
    Print the message to the terminal, since this can at least be copied and
    pasted, unlike the contents of the dialog box.
    """
    print(message)
    if warning:
        messagebox.showwarning(title='Warning', message=message, parent=window)
    else:
        messagebox.showerror(title='Error', message=message, parent=window)
