#############################################################################
#
#  MixMaster
#
#############################################################################

# This file is part of Cantera. See License.txt in the top-level directory or
# at http://www.cantera.org/license.txt for license and copyright information.

# functionality imports
import logging
import os
import sys
import numpy as np

# Cantera imports
import cantera as ct

# local imports
import utilities
from transport_frame import TransportFrame
from composition_frame import MixtureFrame
from thermo_frame import ThermoFrame
from import_frame import ImportFrame
from data_frame import DataFrame
from kinetics_frame import SpeciesKineticsFrame, ReactionKineticsFrame, ReactionPathFrame

#from Edit import EditFrame
from mech_manager import MechManager, _autoload

from unit_chooser import UnitVar
from control_panel import ControlWindow, make_menu, menuitem_state
from mix import Mix, Species

#Backward compatibility of tkinter
if sys.version_info[0] == 3:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter.filedialog import askopenfilename
else:
    import Tkinter as tk
    import tkMessageBox as messagebox
    from tkFileDialog import askopenfilename


logger = logging.getLogger(__name__)

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
            t = tk.Tk()
            self.master = t

        self._windows = {}
        self._vis = {}
        self.windows = []

        self.control_window = ControlWindow(_app_title, self.master)
        self.control_window.master.resizable(tk.FALSE, tk.FALSE)

        self.menu_bar = tk.Frame(self.control_window, relief=tk.GROOVE, bd=2)
        self.menu_bar.grid(row=0, column=0, sticky=tk.N + tk.W + tk.E)

        self.mix_frame = None
        self.thermo_frame = None
        self.transport = None
        self.kinetics_frame = None
        self.rxn_data = None
        self.rxn_paths = None
        self.edit = None
        self.file_name = None

        self.mech_frame = MechManager(self.control_window, self)
        self.mech_frame.grid(row=1, column=0, sticky=tk.N + tk.W)

        file_items = [('Load Mixture...', self.open_mech),
                     ('Import Mechanism File...', self.import_file),
                     'separator',
                     ('Load Data File...', self.show_data),
                     'separator',
                     ('Exit', self.stop),
                     []
                     ]
        self.file_menu = make_menu('File', self.menu_bar, file_items)

        self.vtherm = tk.IntVar()
        self.vcomp = tk.IntVar()
        self.vtran = tk.IntVar()
        self.vkin = tk.IntVar()
        self.vrxn = tk.IntVar()
        self.vrxn.set(0)
        self.vtherm.set(1)
        self.vedit = tk.IntVar()

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
             (' Reactions...', self.show_reactions),
             (' Reaction Paths...', self.show_reaction_paths),
             []]

        self.view_menu = make_menu('Windows', self.menu_bar, w)

        self.help_menu = make_menu('Help', self.menu_bar,
                                   [('About ' + _app_title + '...', self.about_mix),
                                   ('About Cantera...', test_it),
                                   []

                                   ])

        # load the pre-loaded mechanisms
        for mechanism in _autoload:
            self.load_mech(mechanism[0], mechanism[1], 0)

        self.make_windows()
        self.add_window('import', ImportFrame(self))

        self.vtherm.set(1)
        self.show_thermo()
        ##         self.vcomp.set(1)
        ##         self.show_comp()

        self.master.iconify()
        self.master.update()
        self.master.deiconify()
        self.control_window.mainloop()

    def stop(self):
        sys.exit(0)

    def open_mech(self):
        file_types = [("Cantera Input Files", "*.cti"),
                      ("XML Files", "*.xml *.ctml"),
                      ("All Files", "*.*")]
        path_name = askopenfilename(filetypes=file_types)
        if path_name:
            self.load_mech('', path_name)

    def load_mech(self, mech_name, path_name, make_window=1):
        p = os.path.normpath(os.path.dirname(path_name))
        self.file_name = os.path.basename(path_name)
        ff = os.path.splitext(self.file_name)

        try:
            self.mech = ct.Solution(path_name)
            self.mech_name = ff[0]

        except Exception as e:
            utilities.handleError('could not create gas mixture object: ' +
                                  ff[0] + '\n' + str(e))
            self.mech_name = 'Error'
            return

        self.make_mix()

        if not mech_name:
            mech_name = self.mech_name

        self.mech_frame.add_mechanism(mech_name, self.mech)
        if make_window == 1:
            self.make_windows()

    def add_window(self, name, w):
        """Add a new window, or replace an existing one."""
        window_state = ''
        if name in self._windows:
            try:
                window_state = self._windows[name].master.state()
                self._windows[name].master.destroy()
            except:
                pass
        else:
            window_state = 'withdrawn'
        self._windows[name] = w
        self._vis[name] = tk.IntVar()
        if window_state == 'withdrawn':
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
        self.species = []
        for species_name in self.mech.species_names:
            self.species.append(Species(self.mech, species_name))

        x = self.mech.X
        self.mix.setMoles(x)
        self.mix.set(temperature=self.mech.T, pressure=self.mech.P)

    def import_file(self):
        #self.vimport.set(1)
        w = self._windows['import']
        w.show()

    def make_windows(self):
        #if self.mix_frame:
        for w in self.windows:
            try:
                w.destroy()
            except:
                pass

        fr = [MixtureFrame, ThermoFrame, TransportFrame]

        self.mix_frame = MixtureFrame(self.control_window, self)
        self.thermo_frame = ThermoFrame(self.control_window, self)

        #self.transport = TransportFrame(self.control_window, self)
        self.kinetics_frame = SpeciesKineticsFrame(self.control_window, self)

        self.add_window('reaction_data', ReactionKineticsFrame(self.vrxn, self))
        self.add_window('reaction_paths', ReactionPathFrame(self))
        self.add_window('dataset', DataFrame(None, self))


        #self.edit = EditFrame(t, self)

        self.windows = [self.mix_frame, self.thermo_frame, self.transport,
                        self.kinetics_frame]

        self.show_thermo()
        self.show_comp()
        #self.showtransport()
        self.show_kinetics()
        #self.show_reactions()
        #self.show_reaction_paths()
        #self.show_data()

        if self.mech:
            self.mech_frame.grid(row=1, column=0)
        else:
            self.mech_frame.grid_forget()
        #self.showedit()

    def show(self, frame, vis, row, col):
        if vis:
            frame.grid(row=row, column=col, sticky=tk.N + tk.E + tk.S + tk.W)
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

    def show_reactions(self):
        self._windows['reaction_data'].show()

    def show_reaction_paths(self):
        self._windows['reaction_paths'].show()

    def show_data(self):
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

        m = messagebox.showinfo(title='About MixMaster', message=message)


if __name__ == "__main__":
    MixMaster()
