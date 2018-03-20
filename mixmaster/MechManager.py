# This file is part of Cantera. See License.txt in the top-level directory or
# at http://www.cantera.org/license.txt for license and copyright information.

import os
import sys

import cantera as ct
from ControlPanel import ControlWindow
from ControlPanel import make_menu, menuitem_state, add_menu_item
#from Cantera.Examples.Tk import _mechdir

if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk

# automatically-loaded mechanisms
_autoload = [
    (' GRI-Mech 3.0', 'default_data/gri30.cti'),
    (' Air', 'default_data/air.cti'),
    (' H/O/Ar', 'default_data/h2o2.cti')
    ]


def testit():
    pass


class MechManager(tk.Frame):
    def __init__(self, master, app):
        tk.Frame.__init__(self, master)
        #self.config(relief=GROOVE, bd=4)
        self.app = app
        self.master = master
        self.mechindx = tk.IntVar()
        self.mechindx.set(1)

        #m = Label(self, text = 'Loaded Mechanisms')
        #m.grid(column=0,row=0)
        #m.bind('<Double-1>',self.show)
        #self.mechindx.set(0)
        self.mechanisms = []
        self.mlist = [[]]
        i = 1
        #for m in self.mechanisms:
        #    self.mlist.append((m[0], self.setMechanism, 'check', self.mechindx, i))
        #    i += 1
        #self.mlist.append([])

        self.mechmenu = make_menu('Mixtures', self, self.mlist)
        self.mechmenu.grid(row=0, column=0, sticky=tk.W)

        self.mfr = None

    def addMechanism(self, name, mech):
        self.mechanisms.append((name, mech))
        il = len(self.mechanisms)
        self.mlist[-1] = (name, self.setMechanism, 'check', self.mechindx, il)
        add_menu_item(list(self.mechmenu.children.values())[0], self.mlist[-1])
        self.mlist.append([])

        self.mechindx.set(il)
        self.mechmenu.grid(row=0, column=0, sticky=tk.W)

    def delMechanism(self, mech):
        self.mechanisms.remove(mech)
        self.show()

##     def show(self,event=None):
##         print 'show'
##         if self.mfr:
##             self.mfr.destroy()
##         self.mfr = Frame(self)
##         self.mfr.grid(row=1,column=0)
##         self.mfr.config(relief=GROOVE, bd=4)
##         Label(self.mfr,text='jkl').grid(row=0,column=0)
##         i = 0
##         for name, mech in self.mechanisms:
##             Radiobutton(self.mfr, text=name, variable=self.mechindx,
##                         value = i,
##                         command=self.setMechanism).grid(row=i,column=0)
##             i += 1
##         print 'end'

    def setMechanism(self, event=None):
        i = self.mechindx.get()
        self.app.mech = self.mechanisms[i - 1][1]
        self.app.makeMix()
        self.app.makeWindows()
