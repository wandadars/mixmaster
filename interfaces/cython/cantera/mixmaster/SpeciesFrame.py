#
#  function getElements displays a periodic table, and returns a list of
#  the selected elements
#

# This file is part of Cantera. See License.txt in the top-level directory or
# at http://www.cantera.org/license.txt for license and copyright information.

import sys

import cantera as ct


if sys.version_info[0] == 3:
    import tkinter as tk
else:
    import Tkinter as tk


class SpeciesFrame(tk.Frame):
    def __init__(self, master, speciesList=[], selected=[]):
        tk.Frame.__init__(self, master)
        self.master = master
        self.control = tk.Frame(self)
        self.species = {}
        for sp in speciesList:
            self.species[sp.name] = sp

        self.control.config(relief=tk.GROOVE, bd=4)
        tk.Button(self.control, text='Display', command=self.show).pack(fill=tk.X,
                                                                        pady=3,
                                                                        padx=10)
        tk.Button(self.control, text='Clear', command=self.clear).pack(fill=tk.X,
                                                                       pady=3,
                                                                       padx=10)
        tk.Button(self.control, text='  OK  ', command=self.get).pack(side=tk.BOTTOM,
                                                                      fill=tk.X,
                                                                      pady=3,
                                                                      padx=10)
        tk.Button(self.control, text='Cancel', command=self.master.quit).pack(side=tk.BOTTOM,
                                                                              fill=tk.X,
                                                                              pady=3,
                                                                              padx=10)
        self.entries = tk.Frame(self)
        self.entries.pack(side=tk.LEFT)
        self.control.pack(side=tk.RIGHT, fill=tk.Y)
        self.c = {}
        self.selected = selected
        n = 0
        ncol = 8
        rw = 1
        col = 0
        list = self.species.values()
        list.sort()
        for sp in list:
            el = sp.name
            self.species[el] = tk.Frame(self.entries)
            self.species[el].config(relief=tk.GROOVE, bd=4, bg=self.color(el))
            self.c[el] = tk.Button(self.species[el], text=el, bg=self.color(el), width=6, relief=tk.FLAT)
            self.c[el].pack()
            self.c[el].bind("<Button-1>", self.setColors)
            self.species[el].grid(row=rw, column=col, sticky=tk.W + tk.N + tk.E + tk.S)
            col += 1
            if col > ncol:
                rw += 1
                col = 0
        label_message = 'select the species to be included, and then press OK.\n' \
                        'To view the properties of the selected species, press Display '
        tk.Label(self.entries, text=label_message).grid(row=0, column=2, columnspan=10, sticky=tk.W)

    def select(self, el):
        self.c[el]['relief'] = tk.RAISED
        self.c[el]['bg'] = self.color(el, sel=1)

    def deselect(self, el):
        self.c[el]['relief'] = tk.FLAT
        self.c[el]['bg'] = self.color(el, sel=0)

    def selectSpecies(self, splist):
        for sp in splist:
            spname = sp.name
            self.select(spname)

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
        for sp in self.species.values():
            if self.c[sp.name]['relief'] == tk.RAISED:
                selected.append(sp)
        #showElementProperties(selected)

    def get(self):
        self.selected = []
        for sp in self.species.values():
            if self.c[sp.name]['relief'] == tk.RAISED:
                self.selected.append(sp)
        #self.master.quit()'
        self.master.destroy()

    def clear(self):
        for sp in self.species.values():
            self.c[sp]['bg'] = self.color(sp, sel=0)
            self.c[sp]['relief'] = tk.FLAT

## class ElementPropertyFrame(Frame):
##     def __init__(self,master,ellist):
##         Frame.__init__(self,master)
##         n = 1
##         ellist.sort()
##         Label(self,text='Name').grid(column=0,row=0,sticky=W+S,padx=10,pady=10)
##         Label(self,text='Atomic \nNumber').grid(column=1,row=0,sticky=W+S,padx=10,pady=10)
##         Label(self,
##               text='Atomic \nWeight').grid(column=2,
##                                            row=0,
##                                            sticky=W+S,
##                                            padx=10,
##                                            pady=10)
##         for el in ellist:
##             Label(self,
##                   text=el.name).grid(column=0,
##                                      row=n,
##                                      sticky=W,
##                                      padx=10)
##             Label(self,
##                   text=`el.atomicNumber`).grid(column=1,
##                                                row=n,
##                                                sticky=W,
##                                                padx=10)
##             Label(self,
##                   text=`el.atomicWeight`).grid(column=2,
##                                                row=n,
##                                                sticky=W,
##                                                padx=10)
##             n += 1


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
def showElementProperties(ellist):
    m = tk.Tk()
    m.title('Element Properties')
    elem = []
    tk.ElementPropertyFrame(m, ellist).pack()


if __name__ == "__main__":
    print(getSpecies())
