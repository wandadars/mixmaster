# This file is part of Cantera. See License.txt in the top-level directory or
# at http://www.cantera.org/license.txt for license and copyright information.

import os
import math
import sys

if sys.version_info[0] == 3:
    import tkinter  as tk
    from tkinter.filedialog import askopenfilename
else:
    import Tkinter as tk
    from tkFileDialog import askopenfilename

import cantera as ct

#from Cantera.ck2ctml import ck2ctml

class ImportFrame(tk.Frame):
    def __init__(self, top):
        self.master = tk.Toplevel()
        self.master.title('Convert and Import CK File')
        self.master.protocol('WM_DELETE_WINDOW', self.hide)

        tk.Frame.__init__(self, self.master)
        self.config(relief=tk.GROOVE, bd=4)
        self.top = top
        self.infile = tk.StringVar()

        tk.Label(self, text='Input File').grid(row=0, column=0)
        tk.Entry(self, width=40, textvariable=self.infile).grid(column=1, row=0)
        tk.Button(self, text='Browse', command=self.browseForInput).grid(row=0, column=2)

        self.thermo = tk.StringVar()
        tk.Label(self, text='Thermodynamic Database').grid(row=1, column=0)
        tk.Entry(self, width=40, textvariable=self.thermo).grid(column=1, row=1)
        tk.Button(self, text='Browse', command=self.browseForThermo).grid(row=1, column=2)

        self.transport = tk.StringVar()
        tk.Label(self, text="Transport Database").grid(row=2, column=0)
        tk.Entry(self, width=40, textvariable=self.transport).grid(column=1, row=2)
        tk.Button(self, text='Browse', command=self.browseForTransport).grid(row=2, column=2)

        bframe = tk.Frame(self)
        bframe.config(relief=tk.GROOVE, bd=1)
        bframe.grid(row=100, column=0)
        tk.Button(bframe, text='OK', width=8, command=self.importfile).grid(row=0, column=0)
        self.grid(column=0, row=0)
        tk.Button(bframe, text='Cancel', width=8, command=self.hide).grid(row=0, column=1)
        self.grid(column=0, row=0)
        self.hide()

    def browseForInput(self, e=None):
        file_types = [("Reaction Mechanism Files",
                      ("*.inp", "*.mech", "*.ck2")),
                      ("All Files", "*.*")]
        pathname = askopenfilename(filetypes=file_types)
        if pathname:
            self.infile.set(pathname)
        self.show()

    def browseForThermo(self, e=None):
        file_types = [('Thermodynamic Databases',
                      ('*.dat', '*.inp', '*.therm')),
                      ('All Files', '*.*')]
        pathname = askopenfilename(filetypes=file_types)
        if pathname:
            self.thermo.set(pathname)
        self.show()

    def browseForTransport(self, e=None):
        file_types = [("Transport Databases", "*.dat"),
                      ("All Files", "*.*")]
        pathname = askopenfilename(filetypes=file_types)
        if pathname:
            self.transport.set(pathname)
        self.show()


    def importfile(self):
        ckfile = self.infile.get()
        thermdb = self.thermo.get()
        trandb = self.transport.get()
        p = os.path.normpath(os.path.dirname(ckfile))
        file_name = os.path.basename(ckfile)
        ff = os.path.splitext(file_name)
        nm = ""
        if len(ff) > 1:
            nm = ff[0]
        else: nm = ff
        outfile = p + os.sep + nm + '.xml'
        try:
            print('not supported.')
            #ct.ck2ctml(infile = ckfile, thermo_frame = thermdb,
            #       transport = trandb, outfile = outfile,
            #       id = nm)
            self.hide()
            return

        except:
            print('Errors were encountered. See log file ck2ctml.log')
            self.hide()
            return

        self.top.load_mech(nm, outfile, 1)
        self.hide()

##              cmd = 'ck2ctml -i '+ckfile+' -o '+outfile
##              if thermdb <> "":
##                      cmd += ' -t '+thermdb
##              if trandb <> "":
##                      cmd += ' -tr '+trandb
##              cmd += ' -id '+nm
##              ok = os.system(cmd)
##              if ok == 0:
##                      self.top.load_mech(nm,outfile,1)

    def hide(self):
        #self.vis.set(0)
        self.master.withdraw()

    def show(self):
        #v = self.vis.get()
        #if v == 0:
        #       self.hide()
        #       return

        self.master.deiconify()
