#############################################################################
#
#  MixMaster
#
#############################################################################

# This file is part of Cantera. See License.txt in the top-level directory or
# at http://www.cantera.org/license.txt for license and copyright information.

# functionality imports
import sys
if sys.version_info[0] == 3:
    from tkinter import *
    from tkinter import messagebox
    from tkinter.filedialog import askopenfilename
else:
    from Tkinter import *
    import tkMessageBox as messagebox
    from tkFileDialog import askopenfilename

import os
import string

# Cantera imports
import cantera as ct

from numpy import zeros
from . import utilities

# local imports
from .TransportFrame import TransportFrame
from .CompositionFrame import MixtureFrame
from .ThermoFrame import ThermoFrame
from .ImportFrame import ImportFrame
from .DataFrame import DataFrame
from .KineticsFrame import SpeciesKineticsFrame, ReactionKineticsFrame, ReactionPathFrame

#from Edit import EditFrame
from .MechManager import MechManager, _autoload

from .UnitChooser import UnitVar
from .ControlPanel import ControlWindow
from .ControlPanel import make_menu, menuitem_state
from .Mix import Mix, Species


# options
_app_title = 'MixMaster'
_app_version = '1.0'


def test_it():
    return


class MixMaster:
    def __init__(self, master=None):
        """
        Create a new Application instance.
        Usually this is only called once.
        """
        if master:
            self.master = master
        else:
            t = Tk()
            self.master = t

        self._windows = {}
        self._vis = {}
        self.windows = []

        self.cwin = ControlWindow(_app_title, self.master)
        self.cwin.master.resizable(FALSE, FALSE)

        self.menu_bar = Frame(self.cwin, relief=GROOVE, bd=2)
        self.menu_bar.grid(row=0, column=0, sticky=N + W + E)

        self.mix_frame = None
        self.thermo_frame = None
        self.transport = None
        self.kinetics_frame = None
        self.rxn_data = None
        self.rxn_paths = None
        self.edit = None
        self.file_name = None

        self.mech_frame = MechManager(self.cwin, self)
        self.mech_frame.grid(row=1, column=0, sticky=N + W)

        fileitems = [('Load Mixture...', self.open_mech),
                     ('Import Mechanism File...', self.import_file),
                     'separator',
                     ('Load Data File...', self.showdata),
                     'separator',
                     ('Exit', self.stop),
                     []
                     ]
        self.filemenu = make_menu('File', self.menu_bar, fileitems)

        self.vtherm = IntVar()
        self.vcomp = IntVar()
        self.vtran = IntVar()
        self.vkin = IntVar()
        self.vrxn = IntVar()
        self.vrxn.set(0)
        self.vtherm.set(1)
        self.vedit = IntVar()

        dataitems = [(' Import Flame Data', test_it),
                     (' Import CSV Data', test_it),
                     []]
        # self.datamenu = make_menu('Data', self.menu_bar, dataitems)


        # toolitems = [(' Convert...', self.import_file),
        #             []]
        # self.toolmenu = make_menu('Tools', self.menu_bar, toolitems)


        w = [(' Thermodynamic State', self.show_thermo, 'check', self.vtherm),
             (' Composition', self.show_comp, 'check', self.vcomp),
             'separator',
             (' Kinetics', self.show_kinetics, 'check', self.vkin),
             (' Reactions...', self.show_rxns),
             (' Reaction Paths...', self.show_rpaths),
             []]

        self.viewmenu = make_menu('Windows', self.menu_bar, w)

        self.helpmenu = make_menu('Help', self.menu_bar,
                                  [('About ' + _app_title + '...', self.about_mix),
                                   ('About Cantera...', test_it),
                                   []

                                   ])

        # load the preloaded mechanisms
        for m in _autoload:
            self.load_mech(m[0], m[1], 0)

        self.makeWindows()
        self.add_window('import', ImportFrame(self))

        self.vtherm.set(1)
        self.show_thermo()
        ##         self.vcomp.set(1)
        ##         self.show_comp()

        self.master.iconify()
        self.master.update()
        self.master.deiconify()
        self.cwin.mainloop()




    def stop(self):
        sys.exit(0)

    def open_mech(self):

        path_name = askopenfilename(filetypes=[("Cantera Input Files", "*.cti"),
                                              ("XML Files", "*.xml *.ctml"),
                                              ("All Files", "*.*")])
        if path_name:
            self.load_mech('', path_name)


    def load_mech(self, mech_name, path_name, mw=1):

        p = os.path.normpath(os.path.dirname(path_name))
        self.file_name = os.path.basename(path_name)
        ff = os.path.splitext(self.file_name)

        try:
            self.mech = ct.Solution(path_name)
            self.mechname = ff[0]

        except Exception as e:
            utilities.handleError('could not create gas mixture object: '
                                  +ff[0]+'\n'+str(e))
            self.mechname = 'Error'
            return

        self.make_mix()

        if not mech_name:
            mech_name = self.mechname

        self.mech_frame.add_mechanism(mech_name, self.mech)
        if mw == 1:
            self.makeWindows()


    def add_window(self, name, w):
        """Add a new window, or replace an existing one."""
        wstate = ''
        if name in self._windows:
            try:
                wstate = self._windows[name].master.state()
                self._windows[name].master.destroy()
            except:
                pass
        else:
            wstate = 'withdrawn'
        self._windows[name] = w
        self._vis[name] = IntVar()
        if wstate == 'withdrawn':
            self._windows[name].master.withdraw()
        else:
            self._windows[name].show()



    def update(self):
        """Update all windows to reflect the current mixture state."""
        for w in self._windows.keys():
            try:
                m = self._windows[w].master
                if m.state() != 'withdrawn':
                    self._windows[w].show()
            except:
                pass
        self.thermo_frame.showState()
        self.mix_frame.show()



    def make_mix(self):
        self.mix = Mix(self.mech)
        nsp = self.mech.n_species
        nm = self.mech.species_names

        self.species = []
        for k in range(nsp):
            self.species.append(Species(self.mech, nm[k]))

        x = self.mech.X
        self.mix.setMoles(x)
        self.mix.set(temperature = self.mech.T,
                     pressure = self.mech.P)



    def import_file(self):
        #self.vimport.set(1)
        w = self._windows['import']
        w.show()


    def makeWindows(self):
#        if self.mix_frame:
        for w in self.windows:
            try:
                w.destroy()
            except:
                pass

        fr = [MixtureFrame, ThermoFrame, TransportFrame]

        self.mix_frame = MixtureFrame(self.cwin, self)
        self.thermo_frame = ThermoFrame(self.cwin, self)

#        self.transport = TransportFrame(self.cwin, self)
        self.kinetics_frame = SpeciesKineticsFrame(self.cwin, self)

        self.add_window('rxn_data', ReactionKineticsFrame(self.vrxn, self))
        self.add_window('rxn_paths', ReactionPathFrame(self))
        self.add_window('dataset', DataFrame(None, self))


        #self.edit = EditFrame(t, self)

        self.windows = [self.mix_frame, self.thermo_frame, self.transport,
                        self.kinetics_frame]

        self.show_thermo()
        self.show_comp()
        #self.showtransport()
        self.show_kinetics()
        #self.show_rxns()
        #self.show_rpaths()
        #self.showdata()

        if self.mech:
            self.mech_frame.grid(row=1, column=0)
        else:
            self.mech_frame.grid_forget()
        #self.showedit()

    def show(self, frame, vis, row, col):
        if vis:
            frame.grid(row=row,column=col,sticky=N+E+S+W)
        else:
            frame.grid_forget()

    def show_thermo(self):
        if self.thermo_frame:
            self.show(self.thermo_frame, self.vtherm.get(), 7, 0)

    def show_comp(self):
        if self.mix_frame:
            self.show(self.mix_frame, self.vcomp.get(), 8, 0)

    def show_kinetics(self):
        if self.kinetics_frame:
            self.show(self.kinetics_frame, self.vkin.get(), 10, 0)

    def show_rxns(self):
        self._windows['rxn_data'].show()

    def show_rpaths(self):
        self._windows['rxn_paths'].show()

    def showdata(self):
        self._windows['dataset'].browseForDatafile()

    def about_mix(self):

        message = """
                     MixMaster

                    version """ + _app_version + """

                    written by:

                    Prof. David G. Goodwin
                    California Institute of Technology

                    copyright 2003
                    California Institute of Technology
                    """

        m = messagebox.showinfo(title='About MixMaster',
                                message=message)



if __name__ == "__main__":
    MixMaster()
