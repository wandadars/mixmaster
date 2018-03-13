# This file is part of Cantera. See License.txt in the top-level directory or
# at http://www.cantera.org/license.txt for license and copyright information.

from cantera import *

import sys
if sys.version_info[0] == 3:
    from tkinter import *
else:
    from Tkinter import *

from .ControlPanel import ControlWindow
from .ControlPanel import make_menu, menuitem_state, add_menu_item
#from Cantera.Examples.Tk import _mechdir
import os

# automatically-loaded mechanisms
_autoload = [
    (' GRI-Mech 3.0', 'gri30.cti'),
    (' Air', 'air.cti'),
    (' H/O/Ar', 'h2o2.cti')
    ]


def testit():
    pass


class MechManager(Frame):

    def __init__(self, master, app):
        Frame.__init__(self, master)
        #self.config(relief=GROOVE, bd=4)
        self.app = app
        self.master = master
        self.mech_index = IntVar()
        self.mech_index.set(1)

        #m = Label(self, text = 'Loaded Mechanisms')
        #m.grid(column=0,row=0)
#         m.bind('<Double-1>',self.show)
#         self.mech_index.set(0)
        self.mechanisms = []
        self.mlist = [ [] ]
        i = 1
        #for m in self.mechanisms:
        #    self.mlist.append((m[0], self.set_mechanism, 'check', self.mech_index, i))
        #    i += 1
        #self.mlist.append([])

        self.mech_menu = make_menu('Mixtures', self, self.mlist)
        self.mech_menu.grid(row=0, column=0, sticky=W)

        self.mfr = None

    def add_mechanism(self, name, mech):
        self.mechanisms.append((name, mech))
        il = len(self.mechanisms)
        self.mlist[-1] = (name, self.set_mechanism, 'check', self.mech_index, il)
        add_menu_item(list(self.mech_menu.children.values())[0], self.mlist[-1])
        self.mlist.append([])

        self.mech_index.set(il)
        self.mech_menu.grid(row=0, column=0, sticky=W)


    def del_mechanism(self, mech):
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
##             Radiobutton(self.mfr, text=name, variable=self.mech_index,
##                         value = i,
##                         command=self.set_mechanism).grid(row=i,column=0)
##             i += 1
##         print 'end'


    def set_mechanism(self, event=None):
        i = self.mech_index.get()
        self.app.mech = self.mechanisms[i-1][1]
        self.app.make_mix()
        self.app.makeWindows()
