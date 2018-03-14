#
#  function getElements displays a periodic table, and returns a list of
#  the selected elements
#

# This file is part of Cantera. See License.txt in the top-level directory or
# at http://www.cantera.org/license.txt for license and copyright information.

from element_frame import ElementPropertyFrame

import cantera as ct
import sys
if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk


class SpeciesFrame(tk.Frame):
    def __init__(self, master, speciesList=[], selected=[]):  # TODO: Possible mutable default argument
        tk.Frame.__init__(self, master)
        self.master = master
        self.control = tk.Frame(self)
        self.species = {}
        for species in speciesList:
            self.species[species.name] = species

        self.control.config(relief=tk.GROOVE, bd=4)
        tk.Button(self.control, text='Display', command=self.show).pack(fill=tk.X, pady=3, padx=10)
        tk.Button(self.control, text='Clear', command=self.clear).pack(fill=tk.X, pady=3, padx=10)
        tk.Button(self.control, text='  OK  ', command=self.get).pack(side=tk.BOTTOM, fill=tk.X, pady=3, padx=10)
        tk.Button(self.control, text = 'Cancel',command=self.master.quit).pack(side=BOTTOM, fill=tk.X, pady=3, padx=10)

        self.entries = tk.Frame(self)
        self.entries.pack(side=tk.LEFT)
        self.control.pack(side=tk.RIGHT, fill=tk.Y)
        self.c = {}
        self.selected = selected

        max_columns = 8
        row_num = 1
        column_num = 0
        species_list = self.species.values()
        species_list.sort()
        for species in species_list:
            element = species.name
            self.species[element] = tk.Frame(self.entries)
            self.species[element].config(relief=tk.GROOVE, bd=4, bg=self.color(element))
            self.c[element] = tk.Button(self.species[element], text=element,
                                        bg=self.color(element), width=6, relief=tk.FLAT)
            self.c[element].pack()
            self.c[element].bind("<Button-1>",self.setColors)
            self.species[element].grid(row=row_num, column=column_num, sticky=tk.W + tk.N + tk.E + tk.S)
            column_num += 1
            if column_num > max_columns:
                row_num += 1
                column_num = 0
        label_text = 'select the species to be included, and then press OK.\n' \
                     'To view the properties of the selected species, press Display '
        tk.Label(self.entries, text=label_text).grid(row=0, column=2, columnspan=10, sticky=tk.W)


    def select(self, element):
        self.c[element]['relief'] = tk.RAISED
        self.c[element]['bg'] = self.color(element, sel=1)

    def deselect(self, element):
        self.c[element]['relief'] = tk.FLAT
        self.c[element]['bg'] = self.color(element, sel=0)

    def selectSpecies(self, species_list):
        for species in species_list:
            self.select(species.name)

    def setColors(self, event):
        el = event.widget['text']
        if event.widget['relief'] == tk.RAISED:
            event.widget['relief'] = tk.FLAT
            back = self.color(el, sel=0)
            fore = '#ffffff'
        elif event.widget['relief'] == tk.FLAT:
            event.widget['relief'] = tk.RAISED
            fore = '#000000'
            back = self.color(el, sel=1)

        event.widget['bg'] = back
        event.widget['fg'] = fore

    def color(self, el, sel=0):
        _normal = ['#88dddd', '#005500', '#dd8888']
        _selected = ['#aaffff', '#88dd88', '#ffaaaa']
        #row, column = _pos[el]
        if sel:
            list = _selected
        else:
            list = _normal
        return list[1]
        #if column < 3:
        #    return list[0]
        #elif column > 12:
        #    return list[1]
        #else:
        #    return list[2]

    def show(self):
        selected = []
        for species in self.species.values():
            if self.c[species.name]['relief'] == tk.RAISED:
                selected.append(species)
        #showElementProperties(selected)

    def get(self):
        self.selected = []
        for species in self.species.values():
            if self.c[species.name]['relief'] == tk.RAISED:
                self.selected.append(species)
        #self.master.quit()'
        self.master.destroy()

    def clear(self):
        for species in self.species.values():
            self.c[species]['bg'] = self.color(species, sel=0)
            self.c[species]['relief'] = tk.FLAT


# utility functions
def getSpecies(splist=[], selected=[]):
    master = tk.Toplevel()
    master.title('Species')
    t = SpeciesFrame(master, splist, selected)
    if splist:
        t.selectSpecies(splist)
    t.pack()
    t.focus_set()
    t.grab_set()
    t.wait_window()
    try:
        master.destroy()
    except tk.TclError:
        pass
    return t.selected


# display table of selected element properties in a window
def showElementProperties(element_list):
    m = tk.Tk()
    m.title('Element Properties')
    ElementPropertyFrame(m, element_list).pack()


if __name__ == "__main__":
    print(getSpecies())
