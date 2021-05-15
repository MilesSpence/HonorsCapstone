#!/usr/bin/env python
import tkinter as tk
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# This is a very basic epidemiological model that can take user input from a GUI.

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.label = tk.Label(self, text="Enter inputs below...", width=55, pady=10)
        self.label.pack()
        self.label = tk.Label(self, text="Population: ", width=55)
        self.label.pack()
        self.entryN = tk.Entry(self)
        self.entryN.pack()
        self.label = tk.Label(self, text="Initial Infected Population: ", width=55)
        self.label.pack()
        self.entryIo = tk.Entry(self)
        self.entryIo.pack()
        self.label = tk.Label(self, text="Initial Removed Population: ", width=55)
        self.label.pack()
        self.entryRo = tk.Entry(self)
        self.entryRo.pack()
        self.label = tk.Label(self, text="Infection rate: ", width=55)
        self.label.pack()
        self.entryr = tk.Entry(self)
        self.entryr.pack()
        self.label = tk.Label(self, text="Removal rate: ", width=55)
        self.label.pack()
        self.entryy = tk.Entry(self)
        self.entryy.pack()
        
        self.button = tk.Button(self, text="Get", command=self.on_button)
        self.button.pack()        
        
    def on_button(self):
        N = self.entryN.get()
        Io = self.entryIo.get()
        Ro = self.entryRo.get()
        r = self.entryr.get()
        y = self.entryr.get()
        
        if(N.isnumeric() & Io.isnumeric() & Ro.isnumeric() & int(Io)+int(Ro) <= int(N)):
            def sirmodel(initials, time, pop, infect_rate, remove_rate):
                S, I, R = initials
                dSdt = -(infect_rate*S*I)
                dIdt = (infect_rate*S*I)-(remove_rate*I)
                dRdt = (remove_rate*I)
                return dSdt, dIdt, dRdt
            
            So = int(N) - int(Io) - int(Ro)
            initials = int(So), int(Io), int(Ro)
            t = np.linspace(0, 50, 51)
            
            ret = odeint(sirmodel, initials, t, args=(int(N), float(r), float(y)))
            S, I, R = ret.T
    
            print("S: " + str(S))
            print("I: " + str(I))
            print("R: " + str(R))
            print()
            
            fig = plt.figure(facecolor='w')
            ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
            ax.plot(t, S/100, 'b', alpha=0.5, lw=2, label='Susceptible')
            ax.plot(t, I/100, 'r', alpha=0.5, lw=2, label='Infected')
            ax.plot(t, R/100, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
            ax.set_xlabel('Time (days)')
            ax.set_ylabel('Number (100s)')
            ax.set_ylim(0,1.2)
            ax.yaxis.set_tick_params(length=0)
            ax.xaxis.set_tick_params(length=0)
            ax.grid(b=True, which='major', c='w', lw=2, ls='-')
            legend = ax.legend()
            legend.get_frame().set_alpha(0.5)
            for spine in ('top', 'right', 'bottom', 'left'):
                ax.spines[spine].set_visible(False)
            plt.show()
        else:
            print("Input error")

app = SampleApp()

app.mainloop()
