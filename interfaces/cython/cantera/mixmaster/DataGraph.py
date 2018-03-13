# This file is part of Cantera. See License.txt in the top-level directory or
# at http://www.cantera.org/license.txt for license and copyright information.

import sys
import math
import numpy as np


if sys.version_info[0] == 3:
    from tkinter import *
else:
    from Tkinter import *



def plotLimits(ypts, f=0.0, ndiv=5, logscale=0):
    """Return plot limits that"""
    if logscale:
        threshold = 1.0e-19
    else:
        threshold = -1.0e20
    ymax = -1.e20
    ymin = 1.e20
    for y in ypts:
        if y > ymax:
            ymax = y
        if y < ymin and y > threshold:
            ymin = y

    dy = abs(ymax - ymin)

    if logscale:
        ymin = math.floor(math.log10(ymin))
        ymax = math.floor(math.log10(ymax)) + 1
        fctr = 1.0

##         if dy < 0.2*ymin:
##             ymin = ymin*.9
##             ymax = ymax*1.1
##             dy = abs(ymax - ymin)
##         else:
    else:
        ymin -= f * dy
        ymax += f * dy
        dy = abs(ymax - ymin)

        try:
            p10 = math.floor(math.log10(0.1 * dy))
            fctr = math.pow(10.0, p10)
        except:
            return ymin - 1.0, ymax + 1.0, 1.0
        mm = [2.0, 2.5, 2.0]
        i = 0
        while dy / fctr > ndiv:
            fctr = mm[i % 3] * fctr
            i += 1
        ymin = fctr * math.floor(ymin / fctr)
        ymax = fctr * (math.floor(ymax / fctr + 0.999))

    return ymin, ymax, fctr


class DataGraph(Frame):
    def __init__(self, master, data, ix=0, iy=0, title='',
                 label=('x-axis', 'y-axis'), logscale=(0, 0),
                 pixelX=500, pixelY=500):

        self.logscale = logscale
        self.data = data
        self.ix = ix
        self.iy = iy
        self.minX, self.maxX, self.dx = plotLimits(data[ix, :],
                                                   logscale=self.logscale[0])
        self.minY, self.maxY, self.dy = plotLimits(data[iy, :],
                                                   logscale=self.logscale[1])

        Frame.__init__(self, master, relief=RIDGE, bd=2)
        self.title = Label(self, text=' ')
        self.title.grid(row=0, column=1, sticky=W+E)
        self.graph_w, self.graph_h = pixelX - 120, pixelY - 70
        self.origin = (100, 20)
        self.canvas = Canvas(self,
                             width=pixelX,
                             height=pixelY,
                             relief=SUNKEN, bd=1)
        id = self.canvas.create_rectangle(self.origin[0], self.origin[1],
                                          pixelX-20, pixelY-50)
        self.canvas.grid(row=1, column=1, rowspan=2, sticky=N+S+E+W)
        self.last_points = []
        self.ticks(self.minX, self.maxX, self.dx,
                   self.minY, self.maxY, self.dy, 10)
        self.screen_data()
        self.draw()
        self.canvas.create_text(self.origin[0] + self.graph_w/2,
                                self.origin[1] + self.graph_h + 30,
                                text=label[0], anchor=N)
        self.canvas.create_text(self.origin[0] - 50,
                                self.origin[1] + self.graph_h/2,
                                text=label[1], anchor=E)

        self.x_data = []
        self.y_data = []

    def write_value(self, y):
        y_val = '%15.4f' % y
        self.title.config(text=y_val)

    def delete(self, ids):
        for id_num in ids:
            self.canvas.delete(id_num)

    def screen_data(self):
        self.x_data = np.array(self.data[self.ix, :])
        self.y_data = np.array(self.data[self.iy, :])

        if self.logscale[0] > 0:
            self.x_data = np.log10(self.x_data)
        if self.logscale[1] > 0:
            self.y_data = np.log10(self.y_data)

        f = float(self.graph_w) / (self.maxX - self.minX)
        self.x_data = (self.x_data - self.minX) * f + self.origin[0]

        f = float(self.graph_h) / (self.maxY - self.minY)
        self.y_data = (self.maxY - self.y_data) * f + self.origin[1]

    def to_screen(self, x, y):
        if self.logscale[0] > 0:
            x = np.log10(x)
        if self.logscale[1] > 0:
            y = np.log10(y)

        f = float(self.graph_w) / (self.maxX - self.minX)
        xx = (x - self.minX) * f + self.origin[0]

        f = float(self.graph_h) / (self.maxY - self.minY)
        yy = (self.maxY - y) * f + self.origin[1]
        return xx, yy

    def move(self, id, new_pos, old_pos):
        dxpt = (new_pos[0] - old_pos[0]) / (self.maxX - self.minX) * self.graph_w
        dypt = -(new_pos[1] - old_pos[1]) / (self.maxY - self.minY) * self.graph_h

        self.canvas.move(id, dxpt, dypt)
        self.write_value(new_pos[1])

    def plot(self, n, color='black'):
        xpt, ypt = self.to_screen(self.data[self.ix, n], self.data[self.iy, n])
        #xpt = (x-self.minX)/(self.maxX-self.minX)*float(self.graph_w) + self.origin[0]
        #ypt = (self.maxY-y)/(self.maxY-self.minY)*float(self.graph_h) + self.origin[1]
        id_ycross = self.canvas.create_line(xpt, self.graph_h+self.origin[1], xpt, self.origin[1], fill='gray')
        id_xcross = self.canvas.create_line(self.origin[0], ypt, self.graph_w+self.origin[0], ypt, fill='gray')
        id = self.canvas.create_oval(xpt-2, ypt-2, xpt+2, ypt+2, fill=color)
        #self.write_value(y)
        s = '(%g, %g)' % (self.data[self.ix, n], self.data[self.iy, n])
        if n > 0 and self.data[self.iy, n] > self.data[self.iy, n-1]:
            idt = self.canvas.create_text(xpt+5, ypt+5, text=s, anchor=NW)
        else:
            idt = self.canvas.create_text(xpt+5, ypt-5, text=s, anchor=SW)

        return [id, id_xcross, id_ycross, idt]

    def draw(self, color='red'):
        npts = len(self.x_data)
        for n in range(1, npts):
            self.canvas.create_line(self.x_data[n - 1], self.y_data[n - 1],
                                    self.x_data[n], self.y_data[n], fill=color)

    def add_label(self, y, orient=0):
        if orient == 0:
            xpt, ypt = self.to_screen(y, 1.0)
            ypt = self.origin[1] + self.graph_h + 5
            self.canvas.create_text(xpt, ypt, text=y, anchor=N)
        else:
            xpt, ypt = self.to_screen(self.minX, y)
            xpt = self.origin[0] - 5
            self.canvas.create_text(xpt, ypt, text=y, anchor=E)

    def add_legend(self, text, color=None):
        m = Message(self, text=text, width=self.graph_w - 10)
        m.pack(side=BOTTOM)
        if color:
            m.config(fg=color)

    def pause_when_finished(self):
        self.wait_window()

    def minor_ticks(self, x0, x1, y, n, size, orient=0):
        x_tick = x0
        dx = (x1 - x0) / float(n)
        if orient == 0:
            while x_tick <= x1:
                xx, yy = self.to_screen(x_tick, y)
                self.canvas.create_line(xx, yy, xx, yy-size)
                x_tick += dx
        else:
            while x_tick <= x1:
                xx, yy = self.to_screen(y, x_tick)
                self.canvas.create_line(xx, yy, xx + size, yy)
                x_tick += dx

    def ticks(self, x_min, x_max, dx, y_min, y_max, dy, size):

        if self.logscale[0]:
            x_min = math.pow(10.0, x_min)
            x_max = math.pow(10.0, x_max)
        if self.logscale[1]:
            y_min = math.pow(10.0, y_min)
            y_max = math.pow(10.0, y_max)

        n = 5
        ytick = y_min
        while ytick <= y_max:
            xx, yy = self.to_screen(x_min, ytick)
            self.canvas.create_line(xx, yy, xx + size, yy)
            self.add_label(ytick, 1)

            xx, yy = self.to_screen(x_max, ytick)
            self.canvas.create_line(xx, yy, xx - size, yy)
            ytick0 = ytick
            if self.logscale[1]:
                ytick *= 10.0
                n = 10
            else: ytick += dy
            if ytick <= y_max:
                self.minor_ticks(ytick0, ytick, x_min, n, 5, 1)
                self.minor_ticks(ytick0, ytick, x_max, n, -5, 1)

        n = 5
        xtick = x_min
        while xtick <= x_max:
            xx, yy = self.to_screen(xtick, y_min)
            self.canvas.create_line(xx, yy, xx, yy - size)
            self.add_label(xtick, 0)
            xx, yy = self.to_screen(xtick, y_max)
            self.canvas.create_line(xx, yy, xx, yy + size)
            if self.logscale[0]:
                xtick *= 10.0
                n = 10
            else: xtick += dx
            if xtick <= x_max:
                self.minor_ticks(xtick - dx, xtick, y_min, n, 5, 0)
                self.minor_ticks(xtick - dx, xtick, y_max, n, -5, 0)
