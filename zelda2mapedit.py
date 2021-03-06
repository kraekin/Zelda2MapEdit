#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
A simple overworld-editor for Zelda 2 - The Adventure of Link

Author: Johan Björnell <johan@bjornell.se>

"""

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfile
import sys, tkMessageBox


class Zelda2MapEdit:

    def __init__(self, master):
        
        ###  User interface
        self.master = master
        self.master.title("Zelda2MapEdit")
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        maxw = 1040
        maxh = 1260
        self.master.maxsize(width=maxw, height=maxh)

        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        if sh > maxh:
            sh = maxh
        if sw > maxw:
            sw = maxw

        self.master.geometry('%dx%d+%d+%d' % (sw, sh-100, 100, 0))

        # Canvas to draw the map on
        self.canvas = Canvas(master)
        self.hsb = Scrollbar(master, orient="h", command=self.canvas.xview)
        self.vsb = Scrollbar(master, orient="v", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.canvas.grid(row=1, column=0, sticky="nsew")
        self.hsb.grid(row=2, column=0, stick="ew")
        self.vsb.grid(row=1, column=1, sticky="ns")
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.canvas.configure(scrollregion = (0, 0, 1024, 1200))

        # Bind mouse actions to functions
        self.canvas.bind("<ButtonPress-1>", self.leftpress)
        self.canvas.bind("<B1-Motion>", self.leftmotion)
        self.canvas.bind("<ButtonRelease-1>", self.leftrelease)
        self.canvas.bind("<ButtonPress-3>", self.rightpress)
        self.canvas.bind("<B3-Motion>", self.rightmotion)
        self.canvas.bind("<ButtonRelease-3>", self.rightrelease)
        self.canvas.bind("<Motion>", self.mousemove)

        # Terrain images 
        self.img_0 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAYCAgICAgICAgP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAYCAgICAgICAgICAgICAgP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQICAgICAgICAgICAgICAgICAgICAgP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v/AQP/AQAEBAYCAgICAgICAgICAgP7+/v/AQP/AQP/AQP7+/v7+/gEBAQEBAf7+/v/AQAEBAYCAgICAgICAgICAgICAgICAgP7+/v/AQP/AQP7+/v7+/gEBAQEBAf7+/gEBAYCAgICAgICAgICAgICAgICAgICAgICAgP7+/v/AQP/AQP/AQP/AQP/AQP/AQAEBAYCAgICAgICAgICAgICAgICAgICAgICAgP7+/v/AQP/AQP/AQAEBAYCAgICAgP7+/gEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQAEBAYCAgICAgP7+/oCAgP7+/gEBAQEBAf7+/v7+/v7+/v7+/v7+/v/AQP/AQAEBAYCAgICAgP7+/v7+/v7+/oCAgP7+/gEBAQEBAQEBAQEBAf7+/v7+/v/AQAEBAYCAgICAgICAgP7+/v7+/v7+/oCAgICAgP7+/gEBAQEBAQEBAf7+/v7+/v/AQAEBAYCAgICAgICAgICAgICAgICAgICAgICAgP7+/gEBAf7+/v7+/v7+/v7+/v/AQP/AQAEBAf7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAQEBAf7+/v7+/v7+/v7+/v/AQP/AQAEBAf7+/v7+/v7+/gEBAf7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf7+/v7+/v7+/gEBAf7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_1 = PhotoImage(data = "R0lGODlhEAAQAPAAAAEBAQAAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAAAg6Ej6nL7Q+jnLTai7M+BQA7")
        self.img_2 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAf/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAf7+/gEBAf7+/gEBAf7+/gEBAf7+/gEBAf7+/gEBAf7+/gEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQP/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP7+/gEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/v7+/gEBAf/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_3 = PhotoImage(data = "R0lGODlhEAAQAPcAAP7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBAf7+/v/AQP/AQAEBASH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_4 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgP7+/v/AgP/AgP/AgP/AgP/AgP/AgP/AgCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_5 = PhotoImage(data = "R0lGODlhEAAQAPcAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAACgAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAACgAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAAIDAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_6 = PhotoImage(data = "R0lGODlhEAAQAPcAAIDAAAEBAQCgAIDAAIDAAACgAIDAAAEBAQCgAIDAAIDAAIDAAAEBAQCgAIDAAIDAAAEBAQEBAQCgAACgAAEBAYDAAAEBAQEBAQCgAAEBAYDAAAEBAQCgAACgAACgAIDAAAEBAQCgAACgAAEBAQCgAAEBAQEBAQCgAACgAACgAIDAAAEBAQCgAACgAACgAIDAAAEBAQCgAAEBAQEBAQCgAACgAAEBAQCgAACgAACgAAEBAQEBAQEBAQCgAACgAACgAAEBAQCgAAEBAQCgAACgAACgAAEBAQEBAQCgAACgAACgAAEBAQCgAAEBAQCgAAEBAQCgAAEBAQEBAQCgAACgAACgAAEBAQEBAQEBAQCgAAEBAQCgAACgAAEBAQEBAYDAAAEBAQCgAAEBAQEBAQCgAACgAACgAAEBAQCgAACgAAEBAQCgAACgAACgAIDAAIDAAIDAAAEBAQEBAQCgAACgAACgAAEBAQEBAQCgAAEBAQEBAQEBAQCgAACgAACgAIDAAIDAAAEBAQEBAQCgAACgAACgAACgAACgAAEBAQEBAQEBAQCgAACgAACgAACgAIDAAAEBAQEBAQCgAAEBAQCgAACgAACgAACgAAEBAQEBAQCgAACgAACgAACgAACgAAEBAQEBAQEBAQEBAQCgAACgAACgAACgAAEBAQEBAQCgAAEBAQCgAACgAACgAACgAACgAAEBAQEBAQCgAAEBAQCgAACgAACgAIDAAAEBAQEBAQCgAACgAACgAACgAACgAAEBAYDAAAEBAQEBAQCgAAEBAQCgAAEBAQEBAYDAAAEBAQCgAAEBAQCgAACgAAEBAQCgAAEBAYDAAAEBAQEBAQEBAQEBAYDAAAEBAQEBAQEBAQEBAQCgAAEBAQEBAYDAAIDAAAEBAQCgAACgAAEBAQEBAYDAAAEBAQEBAQCgAAEBAYDAAAEBAQEBAYDAAIDAAIDAAIDAAAEBAQEBAQCgAIDAAIDAAAEBAQCgAACgAACgAIDAAAEBAQEBAYDAAACgAIDAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_7 = PhotoImage(data = "R0lGODlhEAAQAPcAAAEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAAEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAIDAAAEBAQCgAAEBAQCgAACgAACgAAEBAYDAAAEBAQCgAAEBAQCgAACgAACgAAEBAQEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAACgAACgAACgAAEBAYDAAAEBAYDAAAEBAQCgAACgAACgAAEBAYDAAAEBAYDAAAEBAQEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gEBAf7+/gEBAf7+/gEBAQCgAAEBAf7+/gCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAAEBAf7+/gEBAQCgAACgAACgAAEBAQCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAACgAAEBAf7+/gEBAf7+/gEBAf7+/gCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQCgAAEBAf7+/gEBAf7+/gEBAYDAAAEBAQEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAAEBAQCgAAEBAQCgAAEBAYDAAAEBAYDAAIDAAAEBAQCgAAEBAQCgAACgAACgAAEBAYDAAAEBAQCgAAEBAQCgAACgAACgAAEBAQEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAAEBAQCgAAEBAYDAAACgAACgAACgAAEBAYDAAAEBAYDAAAEBAQCgAACgAACgAAEBAYDAAAEBAYDAAAEBASH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_8 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v7+/v7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v7+/v7+/v7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQMBAAP7+/v7+/v/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAcBAAMBAAP/AQMBAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAcBAAP/AQMBAAP/AQP/AQMBAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_9 = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_a = PhotoImage(data = "R0lGODlhEAAQAPcAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAP7+/sBAAMBAAMBAAMBAAMBAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_b = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQAEBAQEBAQEBAQEBAQEBAQEBAcBAAP/AQMBAAMBAAAEBAQEBAQEBAcBAAP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAcBAAAEBAQEBAQEBAcBAAP7+/gEBAcBAAAEBAQEBAQEBAQEBAQEBAf7+/sBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAP7+/gEBAQEBAcBAAAEBAQEBAf7+/sBAAMBAAAEBAQEBAcBAAMBAAAEBAQEBAQEBAcBAAAEBAcBAAAEBAQEBAcBAAMBAAP7+/sBAAAEBAcBAAMBAAAEBAQEBAcBAAMBAAP7+/gEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAAEBAcBAAAEBAQEBAQEBAQEBAcBAAMBAAP7+/gEBAcBAAMBAAMBAAMBAAAEBAQEBAQEBAcBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAP7+/gEBAcBAAAEBAQEBAQEBAQEBAcBAAMBAAAEBAQEBAcBAAMBAAMBAAP7+/sBAAMBAAAEBAQEBAQEBAQEBAcBAAAEBAcBAAAEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAP7+/gEBAQEBAQEBAcBAAMBAAP7+/sBAAAEBAQEBAcBAAMBAAAEBAQEBAcBAAMBAAMBAAP7+/gEBAcBAAMBAAAEBAcBAAAEBAQEBAQEBAcBAAAEBAQEBAcBAAMBAAP7+/sBAAP7+/v7+/gEBAcBAAAEBAcBAAAEBAQEBAQEBAQEBAQEBAcBAAMBAAAEBAcBAAP7+/sBAAP7+/gEBAQEBAcBAAMBAAAEBAQEBAcBAAAEBAQEBAcBAAMBAAAEBAcBAAMBAAMBAAMBAAP7+/gEBAcBAAMBAAAEBAcBAAMBAAAEBAcBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAP/AQAEBAcBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAf/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_c = PhotoImage(data = "R0lGODlhEQAQAPEAAAEBAUDA/8DAwP7+/iH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABEAEAAAAi5cjmF5gsAORC7apuxK9caObIkBPhZQiSEjqIcbdBMzx57lwG5524zuo51SGlYBADs=")
        self.img_d = PhotoImage(data = "R0lGODlhEQAQAPEAAAEBAZnZ6sDAwP7+/iH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABEAEAAAAi5cjmF5gsAORC7apuxK9caObIkBPhZQiSEjqIcbdBMzx57lwG5524zuo51SGlYBADs=")
        self.img_e = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP7+/v7+/v7+/v7+/v7+/v7+/sBAAMBAAP/AQP/AQP/AQP/AQP/AQP/AQP7+/v7+/v7+/sBAAMBAAP7+/v7+/sBAAP7+/v7+/sBAAAEBAf/AQP/AQP/AQP7+/v7+/sBAAMBAAP7+/v7+/sBAAMBAAMBAAMBAAMBAAP7+/sBAAAEBAf/AQP/AQP7+/sBAAP7+/v7+/sBAAP7+/v7+/v7+/sBAAMBAAMBAAMBAAMBAAAEBAf/AQP7+/v7+/sBAAP7+/sBAAMBAAMBAAMBAAP7+/v7+/sBAAMBAAMBAAAEBAQEBAQEBAf/AQP7+/v7+/sBAAP7+/sBAAMBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAAEBAQEBAf7+/v7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAAEBAQEBAQEBAf/AQP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAAEBAQEBAQEBAf/AQP7+/sBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAMBAAAEBAcBAAMBAAAEBAQEBAf/AQMBAAMBAAMBAAAEBAcBAAMBAAMBAAMBAAMBAAAEBAcBAAAEBAQEBAQEBAQEBAcBAAMBAAMBAAMBAAMBAAAEBAQEBAcBAAMBAAAEBAcBAAAEBAQEBAcBAAAEBAQEBAQEBAcBAAMBAAAEBAcBAAMBAAMBAAAEBAQEBAQEBAQEBAQEBAcBAAMBAAAEBAQEBAQEBAcBAAMBAAMBAAAEBAQEBAQEBAcBAAAEBAQEBAcBAAMBAAAEBAQEBAQEBAf/AQP/AQAEBAQEBAQEBAQEBAcBAAAEBAQEBAcBAAAEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAf/AQP/AQAEBAQEBAQEBAQEBAf/AQP/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.img_f = PhotoImage(data = "R0lGODlhEAAQAPcAAP/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAf/AQAEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf7+/v7+/gEBAf7+/v7+/gEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf7+/gEBAQEBAQEBAf7+/gEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAcBAAAEBAcBAAAEBAQEBAQEBAQEBAQEBAQEBAf/AQAEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQP/AQAEBAQEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAQEBAf/AQP/AQAEBAf/AQP/AQAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAf/AQP/AQAEBAf/AQP/AQAEBAf/AQAEBAQEBAQEBAf/AQP/AQP/AQP/AQAEBAQEBAf/AQP/AQAEBAf/AQP/AQAEBAf/AQAEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAQEBAf/AQP/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQP/AQP/AQP/AQP/AQP/AQP/AQAEBAf/AQP/AQCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAACP4AAQQQMIBAAQMHECRQsIBBAwcPIESQMIFCBQsXMGTQsIFDBw8fQIQQMYJECRMnUKRQsYJFCxcvYMSQMYNGDRs3cOTQsYNHDx8/gAQRMoRIESNHkCRRsoRJEydPoESRMoVKFStXsGTRsoVLFy9fwIQRM4ZMGTNn0KRRs4ZNGzdv4MSRM4dOHTt38OTRs4dPHz9/AAUSNIhQIUOHECVStIhRI0ePIEWSNIlSJUuXMGXStIlTJ0+fQIUSNYpUKVOnUKVStYpVK1evYMWSNYtWLVu3cOXStYtXL1+/gAUTNoxYMWPHkCVTtoxZM2fPoEWTNo1aNWvXsGXTto1bN2/fwCWFEzeOXDlz59ClU7eOXTt37+DFkzePXj179/Dl07ePXz9//wQEADs=")
        self.error_img = PhotoImage(data = "R0lGODlhEAAQAPAAAAEBAe0cJCH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sNZ2FtbWE9MC40NTQ1NQAsAAAAABAAEAAAAiKMA6l5bcucW7LGWe3NiHK4NWB4jFynnA+ZAZq6siL0mUcBADs=")
        self.img_bracket = PhotoImage(data = "R0lGODlhEAAQAHAAACH/C0ltYWdlTWFnaWNrDWdhbW1hPTAuNDU0NTUAIfkEAAAAAAAsAAAAABAAEACHAAAAAAAzAABmAACZAADMAAD/ACsAACszACtmACuZACvMACv/AFUAAFUzAFVmAFWZAFXMAFX/AIAAAIAzAIBmAICZAIDMAID/AKoAAKozAKpmAKqZAKrMAKr/ANUAANUzANVmANWZANXMANX/AP8AAP8zAP9mAP+ZAP/MAP//MwAAMwAzMwBmMwCZMwDMMwD/MysAMyszMytmMyuZMyvMMyv/M1UAM1UzM1VmM1WZM1XMM1X/M4AAM4AzM4BmM4CZM4DMM4D/M6oAM6ozM6pmM6qZM6rMM6r/M9UAM9UzM9VmM9WZM9XMM9X/M/8AM/8zM/9mM/+ZM//MM///ZgAAZgAzZgBmZgCZZgDMZgD/ZisAZiszZitmZiuZZivMZiv/ZlUAZlUzZlVmZlWZZlXMZlX/ZoAAZoAzZoBmZoCZZoDMZoD/ZqoAZqozZqpmZqqZZqrMZqr/ZtUAZtUzZtVmZtWZZtXMZtX/Zv8AZv8zZv9mZv+ZZv/MZv//mQAAmQAzmQBmmQCZmQDMmQD/mSsAmSszmStmmSuZmSvMmSv/mVUAmVUzmVVmmVWZmVXMmVX/mYAAmYAzmYBmmYCZmYDMmYD/maoAmaozmapmmaqZmarMmar/mdUAmdUzmdVmmdWZmdXMmdX/mf8Amf8zmf9mmf+Zmf/Mmf//zAAAzAAzzABmzACZzADMzAD/zCsAzCszzCtmzCuZzCvMzCv/zFUAzFUzzFVmzFWZzFXMzFX/zIAAzIAzzIBmzICZzIDMzID/zKoAzKozzKpmzKqZzKrMzKr/zNUAzNUzzNVmzNWZzNXMzNX/zP8AzP8zzP9mzP+ZzP/MzP///wAA/wAz/wBm/wCZ/wDM/wD//ysA/ysz/ytm/yuZ/yvM/yv//1UA/1Uz/1Vm/1WZ/1XM/1X//4AA/4Az/4Bm/4CZ/4DM/4D//6oA/6oz/6pm/6qZ/6rM/6r//9UA/9Uz/9Vm/9WZ/9XM/9X///8A//8z//9m//+Z///M////AAAAAAAAAAAAAAAACGYAlQkcSLDgwHoHEwpEaLChwXrSIipDGFEaQYYCLWYUSG+ZwWUalUnz2JCeSGUeQw4kudGkxY7KTCpzh/LkRocuSY4kKFOnzJAMWdoEGZNYwZ8DLQoVCDLiMpcSeTpUyBKjR5kCAwIAOw==")

        # Set window icon
        self.master.tk.call('wm', 'iconphoto', root._w, self.img_2)

        # Frame with labelframes
        self.btnFrame = Frame(root, height=60)
        self.btnFrame.grid(row=0, column=0)

        # Labelframes
        self.terrainFrame = LabelFrame(self.btnFrame, text="Terrain", padx=5, pady=5)
        self.terrainFrame.grid(row=0, column=0)
        self.toolFrame = LabelFrame(self.btnFrame, text="Tools", padx=5, pady=5)
        self.toolFrame.grid(row=0, column=1)
        self.coordFrame = LabelFrame(self.btnFrame, text="Coordinates", padx=5, pady=5, width=70)
        self.coordFrame.grid(row=0, column=2)
        #self.coordFrame.grid_propagate(0)
        self.sizeFrame = LabelFrame(self.btnFrame, text="Size", padx=5, pady=5)
        self.sizeFrame.grid(row=0, column=3)

        # Buttons
        self.tile_0_btn = Button(self.terrainFrame, image=self.img_0, command=lambda: self.selectterrain("0"))
        self.tile_0_btn.grid(row=0, column=0)
        self.tile_1_btn = Button(self.terrainFrame, image=self.img_1, command=lambda: self.selectterrain("1"))
        self.tile_1_btn.grid(row=0, column=1)
        self.tile_2_btn = Button(self.terrainFrame, image=self.img_2, command=lambda: self.selectterrain("2"))
        self.tile_2_btn.grid(row=0, column=2)
        self.tile_3_btn = Button(self.terrainFrame, image=self.img_3, command=lambda: self.selectterrain("3"))
        self.tile_3_btn.grid(row=0, column=3)
        self.tile_4_btn = Button(self.terrainFrame, image=self.img_4, command=lambda: self.selectterrain("4"))
        self.tile_4_btn.grid(row=0, column=4)
        self.tile_5_btn = Button(self.terrainFrame, image=self.img_5, command=lambda: self.selectterrain("5"))
        self.tile_5_btn.grid(row=0, column=5)
        self.tile_6_btn = Button(self.terrainFrame, image=self.img_6, command=lambda: self.selectterrain("6"))
        self.tile_6_btn.grid(row=0, column=6)
        self.tile_7_btn = Button(self.terrainFrame, image=self.img_7, command=lambda: self.selectterrain("7"))
        self.tile_7_btn.grid(row=0, column=7)
        self.tile_8_btn = Button(self.terrainFrame, image=self.img_8, command=lambda: self.selectterrain("8"))
        self.tile_8_btn.grid(row=0, column=8)
        self.tile_9_btn = Button(self.terrainFrame, image=self.img_9, command=lambda: self.selectterrain("9"))
        self.tile_9_btn.grid(row=0, column=9)
        self.tile_a_btn = Button(self.terrainFrame, image=self.img_a, command=lambda: self.selectterrain("a"))
        self.tile_a_btn.grid(row=0, column=10)
        self.tile_b_btn = Button(self.terrainFrame, image=self.img_b, command=lambda: self.selectterrain("b"))
        self.tile_b_btn.grid(row=0, column=11)
        self.tile_c_btn = Button(self.terrainFrame, image=self.img_c, command=lambda: self.selectterrain("c"))
        self.tile_c_btn.grid(row=0, column=12)
        self.tile_d_btn = Button(self.terrainFrame, image=self.img_d, command=lambda: self.selectterrain("d"))
        self.tile_d_btn.grid(row=0, column=13)
        self.tile_e_btn = Button(self.terrainFrame, image=self.img_e, command=lambda: self.selectterrain("e"))
        self.tile_e_btn.grid(row=0, column=14)
        self.tile_f_btn = Button(self.terrainFrame, image=self.img_f, command=lambda: self.selectterrain("f"))
        self.tile_f_btn.grid(row=0, column=15)
        
        self.bracketbtn = Button(self.toolFrame, image=self.img_bracket, command=lambda: self.selectterrain("x"))
        self.bracketbtn.grid(row=0, column=0)

        # Labels 
        self.coordlabeltext = StringVar()
        #self.coordlabeltext.set("(0, 0)")
        self.coordlabeltext.set("'0' (0, 0)")
        self.coordlabel = Label(self.coordFrame, textvariable=self.coordlabeltext)
        self.coordlabel.grid(row=0, column=0, pady=2)

        self.mapsizelabeltext = StringVar()
        self.mapsizelabeltext.set("000 / 000")
        self.mapsizelabel = Label(self.sizeFrame, textvariable=self.mapsizelabeltext)
        self.mapsizelabel.grid(row=0, column=0, pady=2)

        # Frame for label in the bottom
        self.labelFrame = Frame(root, height=60)
        self.labelFrame.grid(row=3, column=0)

        self.locationlabeltext = StringVar()
        self.locationlabeltext.set("")
        self.locationlabel = Label(self.labelFrame, textvariable=self.locationlabeltext)
        self.locationlabel.grid(row=0, column=0)
        
        # Menu
        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open..", command=self.openromfile)
        self.filemenu.add_command(label="Save", command=self.saveromfile)
        self.filemenu.entryconfig("Save", state="disabled")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.mapmenu = Menu(self.menubar, tearoff=0)
        self.mapmenu.add_command(label="West Hyrule", command=lambda: self.changemap(0))
        self.mapmenu.entryconfig("West Hyrule", state="disabled")
        self.mapmenu.add_command(label="Death Mountain", command=lambda: self.changemap(1))
        self.mapmenu.entryconfig("Death Mountain", state="disabled")
        self.mapmenu.add_command(label="East Hyrule", command=lambda: self.changemap(2))
        self.mapmenu.entryconfig("East Hyrule", state="disabled")
        self.mapmenu.add_command(label="Maze Island", command=lambda: self.changemap(3))
        self.mapmenu.entryconfig("Maze Island", state="disabled")
        self.menubar.add_cascade(label="Map", menu=self.mapmenu)

        self.settingsmenu = Menu(self.menubar, tearoff=0)
        self.settingsmenu.add_command(label="Preferences..", command=self.preferences)
        self.menubar.add_cascade(label="Settings", menu=self.settingsmenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About..", command=self.about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

        ### Variables
        # Map size
        self.mapsizex = 64
        self.mapsizey = 75

        # Original mapsizes
        self.origmapsizes = [ 801, 803, 794, 803 ]

        # Selected terrain to draw on map (0-f)
        self.selectedterrain = "c"
        self.tile_c_btn.config(relief=SUNKEN)

        # Array to contain decoded mapstrings
        self.maparray = [[0 for y in range(self.mapsizey * 4)] for x in range(self.mapsizex)]

        # Map data locations in ROM
        self.mapstartlocations = [ int("506C", 16),  # West Hyrule
                                   int("665C", 16),  # Death Mountain
                                   int("9056", 16),  # East Hyrule
                                   int("A65C", 16) ] # Maze Island

        # Keep track of active map
        # 0 = West Hyrule, 3 = Maze Island etc.
        self.activemap = 0

        # Filename
        self.filename = ""

        # Enable edit after file open
        self.editenabled = 0
        # Ask to save if edited
        self.edited = 0

        # List of list of breakpoints
        self.breakpoints = [ [], [], [], [] ]

        # Palace 2 and 6 hidden or visible
        # (not implemented yet)
        self.palace6hidden = 1
        # New Kasuto hidden
        self.newkasutohidden = 1

        # Locations on map
        # Name, x address, y address, x offset, y offset, palace pointer address
        # West Hyrule

        self.maplocations = [[[ "North Castle", "466E", "462F", 0, 0, 0, 0, 0 ],
                             [ "Trophy cave", "466F", "4630", 0, 0, 0, 0, 0 ],
                             [ "Forest with 50 exp. bag and Aches", "4670", "4631", 0, 0, 0, 0, 0 ],
                             [ "1st Magic Container cave", "4671", "4632", 0, 0, 0, 0, 0 ],
                             [ "Forest with 100 exp. bag and Megmets", "4672", "4633", 0, 0, 0, 0, 0 ],
                             [ "1st Heart Container area", "4673", "4634", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "4674", "4635", 0, 0, 0, 0, 0 ],
                             [ "Bubble path to 1st Heart Container", "4675", "4636", 0, 0, 0, 0, 0 ],
                             [ "Life doll in swamp", "4676", "4637", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar in graveyard", "4677", "4638", 0, 0, 0, 0, 0 ],
                             [ "Northern exit of cave to Palace 1", "4678", "4639", 0, 0, 0, 0, 0 ],
                             [ "Southern exit of cave to Palace 1", "4679", "463A", 0, 0, 64, 0, 0 ],
                             [ "Northern exit of Western Mt. caves", "467A", "463B", 0, 0, 0, 0, 0 ],
                             [ "Southern exit of Western Mt. caves", "467B", "463C", 0, 0, 64, 0, 0 ],
                             [ "Megmet cave and 200 exp. bag", "467C", "463D", 0, 0, 0, 0, 0 ],
                             [ "Water of Life cave", "467D", "463E", 0, 0, 0, 0, 0 ],
                             [ "2nd Heart Container cave", "467E", "463F", 0, 0, 0, 0, 0 ],
                             [ "Hole to Palace 3 cave", "467F", "4640", 0, 0, 0, 0, 0 ],
                             [ "Caves on Palace 3's island", "4680", "4641", 0, 0, 64, 0, 0 ],
                             [ "North and South bridge to island before Death Mt.", "4681", "4642", 0, 0, 0, 0, 0 ],
                             [ "East and West bridge to island before Death Mt.", "4682", "4643", 0, 0, 0, 0, 0 ],
                             [ "West exit of bridge after Death Mt.", "4683", "4644", 0, 0, 0, 0, 0 ],
                             [ "East exit of bridge after Death Mt.", "4684", "4645", 0, 0, 64, 0, 0 ],
                             [ "Forest with Fairy after Western Mt. cave", "4685", "4646", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar in swamp", "4686", "4647", 0, 0, 0, 0, 0 ],
                             [ "forest with Fairy East of island before Death Mt.", "4687", "4648", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "4688", "4649", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "4689", "464A", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "468A", "464B", 0, 0, 0, 0, 0 ],
                             [ "Lost Woods", "468B", "464C", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar on trail in swamp", "468C", "464D", 0, 0, 0, 0, 0 ],
                             [ "Extra Red Magic Jar on beach (not used in original game)", "468D", "464E", 0, 0, 0, 0, 0 ],
                             [ "Life doll on beach", "468E", "464F", 0, 0, 0, 0, 0 ],
                             [ "Raft Dock to East Hyrule", "4697", "4658", 0, 0, 0, 128, 0 ],
                             [ "Cave entrance to Death Mountain", "4698", "4659", 0, 0, 0, 128, 0 ],
                             [ "Cave exit to Death Mountain", "4699", "465A", 0, 0, 0, 128, 0 ],
                             [ "King's Tomb", "469A", "465B", 0, 0, 0, 128, 0 ],
                             [ "Rauru", "469B", "465C", 0, 0, 64, 128, 0 ],
                             [ "Ruto", "469D", "465E", 0, 0, 64, 128, 0 ],
                             [ "Southern Saria", "469E", "465F", 0, 0, 0, 128, 0 ],
                             [ "Northern Saria", "469F", "4660", 0, 0, 64, 128, 0 ],
                             [ "Bagu's Cabin", "46A0", "4661", 0, 0, 0, 128, 0 ],
                             [ "Mido", "46A1", "4662", 0, 0, 64, 128, 0 ],
                             [ "Parapa Palace", "46A2", "4663", 0, 0, 0, 128, 0 ],
                             [ "Midoro Swamp Palace", "46A3", "4664", 0, 0, 0, 128, 0 ]],
                             [[ "Island Palace", "46A4", "4665", 0, 0, 0, 128, 0 ],
                             [ "Cave B West Exit", "614B", "610C", 0, 0, 0, 0, 0 ],
                             [ "Cave B East Exit", "614C", "610D", 0, 0, 64, 0, 0 ],
                             [ "Cave C West Exit", "614D", "610E", 0, 0, 0, 0, 0 ],
                             [ "Cave C East Exit", "614E", "610F", 0, 0, 64, 0, 0 ],
                             [ "Cave E South Exit", "614F", "6110", 0, 0, 0, 0, 0 ],
                             [ "Cave E North Exit", "6150", "6111", 0, 0, 64, 0, 0 ],
                             [ "Cave D West Exit", "6151", "6112", 0, 0, 0, 0, 0 ],
                             [ "Cave D East Exit", "6152", "6113", 0, 0, 64, 0, 0 ],
                             [ "Cave F West Exit", "6153", "6114", 0, 0, 0, 0, 0 ],
                             [ "Cave F East Exit", "6154", "6115", 0, 0, 64, 0, 0 ],
                             [ "Cave J West Exit", "6155", "6116", 0, 0, 0, 0, 0 ],
                             [ "Cave J East Exit", "6156", "6117", 0, 0, 64, 0, 0 ],
                             [ "Cave I North Exit", "6157", "6118", 0, 0, 0, 0, 0 ],
                             [ "Cave I South Exit", "6158", "6119", 0, 0, 64, 0, 0 ],
                             [ "Cave L North Exit", "6159", "611A", 0, 0, 0, 0, 0 ],
                             [ "Cave L South Exit", "615A", "611B", 0, 0, 64, 0, 0 ],
                             [ "Cave O North Exit", "615B", "611C", 0, 0, 0, 0, 0 ],
                             [ "Cave O South Exit", "615C", "611D", 0, 0, 64, 0, 0 ],
                             [ "Cave M West Exit", "615D", "611E", 0, 0, 0, 0, 0 ],
                             [ "Cave M East Exit", "615E", "611F", 0, 0, 64, 0, 0 ],
                             [ "Cave P West Exit", "615F", "6120", 0, 0, 0, 0, 0 ],
                             [ "Cave P East Exit", "6160", "6121", 0, 0, 64, 0, 0 ],
                             [ "Cave Q West Exit", "6161", "6122", 0, 0, 0, 0, 0 ],
                             [ "Cave Q East Exit", "6162", "6123", 0, 0, 64, 0, 0 ],
                             [ "Cave R South Exit", "6163", "6124", 0, 0, 0, 0, 0 ],
                             [ "Cave R North Exit", "6164", "6125", 0, 0, 64, 0, 0 ],
                             [ "Cave N South Exit", "6165", "6126", 0, 0, 0, 0, 0 ],
                             [ "Cave N North Exit", "6166", "6127", 0, 0, 64, 0, 0 ],
                             [ "Hammer Cave", "6167", "6128", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave G West Exit (Bottom left)", "6168", "6129", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave G East Exit (Bottom right)", "6169", "612A", 0, 0, 64, 0, 0 ],
                             [ "Elevator Cave G West Exit (Top left)", "616A", "612B", 0, 0, 128, 0, 0 ],
                             [ "Elevator Cave G East Exit (Top Right)", "616B", "612C", 0, 0, 192, 0, 0 ],
                             [ "Elevator Cave H West Exit (Top left)", "616C", "612D", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave H East Exit (Top Right)", "616D", "612E", 0, 0, 64, 0, 0 ],
                             [ "Elevator Cave H North Exit (Bottom left)", "616E", "612F", 0, 0, 128, 0, 0 ],
                             [ "Elevator Cave H South Exit (Bottom right)", "616F", "6130", 0, 0, 192, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 2", "6170", "6131", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 1", "6171", "6132", 0, 0, 0, 0, 0 ],
                             [ "Maze Island's Magic Container", "6172", "6133", 0, 0, 0, 0, 0 ],
                             [ "Bridge back to East Hyrule", "6173", "6134", 0, 0, 0, 128, 0 ],
                             [ "Cave A back to West Hyrule", "6175", "6136", 0, 0, 0, 128, 0 ],
                             [ "Cave K back to West Hyrule", "6176", "6137", 0, 0, 0, 128, 0 ],
                             [ "Maze Palace", "617F", "6140", 0, 0, 0, 128, 0 ],
                             [ "Maze Island Child", "6182", "6143", 0, 0, 0, 0, 0 ],
                             [ "Death Mountain's Magic Container", "6183", "6144", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 3", "6184", "6145", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 7", "6185", "6146", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 4", "6186", "6147", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 5", "6187", "6148", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 6", "6188", "6149", 0, 0, 0, 0, 0 ]],
                             [[ "Forest with 500 Exp. bag west of Nabooru", "866E", "862F", 0, 0, 0, 0, 0 ],
                             [ "Forest with 500 Exp. bag north of 3-Eye Rock", "866F", "8630", 0, 0, 0, 0, 0 ],
                             [ "1st Forced battle scene after River Devil", "8670", "8631", 0, 0, 0, 0, 0 ],
                             [ "2nd Forced battle scene after River Devil", "8671", "8632", 0, 0, 0, 0, 0 ],
                             [ "3rd Forced battle scene after River Devil", "8672", "8633", 0, 0, 0, 0, 0 ],
                             [ "Forced battle scene entering Path of Fire", "8673", "8634", 0, 0, 0, 0, 0 ],
                             [ "Bridge North of Old Kasuto", "8674", "8635", 0, 0, 0, 0, 0 ],
                             [ "Bridge East of Old Kasuto", "8675", "8636", 0, 0, 0, 0, 0 ],
                             [ "2nd battle scene before Darunia", "8676", "8637", 0, 0, 0, 0, 0 ],
                             [ "1st battle scene before Darunia", "8677", "8638", 0, 0, 0, 0, 0 ],
                             [ "Heart Container in Ocean", "8678", "8639", 0, 0, 0, 0, 0 ],
                             [ "South cave north of Nabooru", "8679", "863A", 0, 0, 0, 0, 0 ],
                             [ "North cave north of Nabooru", "867A", "863B", 0, 0, 64, 0, 0 ],
                             [ "Cave with 500 exp. bag south of Nabooru", "867B", "863C", 0, 0, 0, 0, 0 ],
                             [ "Cave with 500 exp. bag North of Old Kasuto", "867C", "863D", 0, 0, 0, 0, 0 ],
                             [ "West cave near New Kasuto", "867D", "863E", 0, 0, 0, 0, 0 ],
                             [ "East cave near New Kasuto", "867E", "863F", 0, 0, 64, 0, 0 ],
                             [ "Cave C on the way to Great Palace", "867F", "8640", 0, 0, 0, 0, 0 ],
                             [ "Cave D on the way to Great Palace", "8680", "8641", 0, 0, 64, 0, 0 ],
                             [ "Cave B on the way to Great Palace", "8681", "8642", 0, 0, 0, 0, 0 ],
                             [ "Cave A on the way to Great Palace", "8682", "8643", 0, 0, 64, 0, 0 ],
                             [ "Life doll in swamp", "8683", "8644", 0, 0, 0, 0, 0 ],
                             [ "Extra battle scene (same spot as 864B)", "8684", "8645", 0, 0, 0, 0, 0 ],
                             [ "500 exp. bag on beach near OceanPalace", "8685", "8646", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar on beach near Nabooru", "8686", "8647", 0, 0, 0, 0, 0 ],
                             [ "Life doll on beach", "8687", "8648", 0, 0, 0, 0, 0 ],
                             [ "Heart Container on beach east of 3-Eye Rock", "8688", "8649", 0, 0, 0, 0, 0 ],
                             [ "Forest with fairy southwest of Nabooru", "8689", "864A", 0, 0, 0, 0, 0 ],
                             [ "500 exp. bag in Path of Fire", "868A", "864B", 0, 0, 0, 0, 0 ],
                             [ "Red Magic Jar in Path of Fire", "868B", "864C", 0, 0, 0, 0, 0 ],
                             [ "3rd Forced Battle scene in the Path of Fire", "868C", "864D", 0, 0, 0, 0, 0 ],
                             [ "2nd Forced Battle scene in the Path of Fire", "868D", "864E", 0, 0, 0, 0, 0 ],
                             [ "1st Forced Battle scene in the Path of Fire", "868E", "864F", 0, 0, 0, 0, 0 ],
                             [ "Bridge to Maze Island", "8696", "8657", 0, 0, 0, 128, 0 ],
                             [ "Raft dock back to West Hyrule", "8697", "8658", 0, 0, 0, 128, 0 ],
                             [ "Nabooru", "869B", "865C", 0, 0, 64, 128, 0 ],
                             [ "Darunia", "869D", "865E", 0, 0, 64, 128, 0 ],
                             [ "New Kasuto *", "869F", "8660", 0, 0, 0, 0, 0 ],
                             [ "Old Kasuto", "86A1", "8662", 0, 0, 64, 128, 0 ],
                             [ "Ocean Palace", "86A2", "8663", 0, 0, 0, 128, 0 ],
                             [ "Call location for Hidden Palace", "8388", "8382", 0, 0, 0, 0, 0 ],
                             [ "Hidden Palace", "86A3", "8664", 0, 0, 0, 0, 0 ],
                             [ "Great Palace", "86A4", "8665", 0, 0, 0, 128, 0 ]],
                             [[ "Cave B West Exit", "A14B", "A10C", 0, 0, 0, 0, 0 ],
                             [ "Cave B East Exit", "A14C", "A10D", 0, 0, 64, 0, 0 ],
                             [ "Cave C West Exit", "A14D", "A10E", 0, 0, 0, 0, 0 ],
                             [ "Cave C East Exit", "A14E", "A10F", 0, 0, 64, 0, 0 ],
                             [ "Cave E South Exit", "A14F", "A110", 0, 0, 0, 0, 0 ],
                             [ "Cave E North Exit", "A150", "A111", 0, 0, 64, 0, 0 ],
                             [ "Cave D West Exit", "A151", "A112", 0, 0, 0, 0, 0 ],
                             [ "Cave D East Exit", "A152", "A113", 0, 0, 64, 0, 0 ],
                             [ "Cave F West Exit", "A153", "A114", 0, 0, 0, 0, 0 ],
                             [ "Cave F East Exit", "A154", "A115", 0, 0, 64, 0, 0 ],
                             [ "Cave J West Exit", "A155", "A116", 0, 0, 0, 0, 0 ],
                             [ "Cave J East Exit", "A156", "A117", 0, 0, 64, 0, 0 ],
                             [ "Cave I North Exit", "A157", "A118", 0, 0, 0, 0, 0 ],
                             [ "Cave I South Exit", "A158", "A119", 0, 0, 64, 0, 0 ],
                             [ "Cave L North Exit", "A159", "A11A", 0, 0, 0, 0, 0 ],
                             [ "Cave L South Exit", "A15A", "A11B", 0, 0, 64, 0, 0 ],
                             [ "Cave O North Exit", "A15B", "A11C", 0, 0, 0, 0, 0 ],
                             [ "Cave O South Exit", "A15C", "A11D", 0, 0, 64, 0, 0 ],
                             [ "Cave M West Exit", "A15D", "A11E", 0, 0, 0, 0, 0 ],
                             [ "Cave M East Exit", "A15E", "A11F", 0, 0, 64, 0, 0 ],
                             [ "Cave P West Exit", "A15F", "A120", 0, 0, 0, 0, 0 ],
                             [ "Cave P East Exit", "A160", "A121", 0, 0, 64, 0, 0 ],
                             [ "Cave Q West Exit", "A161", "A122", 0, 0, 0, 0, 0 ],
                             [ "Cave Q East Exit", "A162", "A123", 0, 0, 64, 0, 0 ],
                             [ "Cave R South Exit", "A163", "A124", 0, 0, 0, 0, 0 ],
                             [ "Cave R North Exit", "A164", "A125", 0, 0, 64, 0, 0 ],
                             [ "Cave N South Exit", "A165", "A126", 0, 0, 0, 0, 0 ],
                             [ "Cave N North Exit", "A166", "A127", 0, 0, 64, 0, 0 ],
                             [ "Hammer Cave", "A167", "A128", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave G West Exit (Bottom left)", "A168", "A129", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave G East Exit (Bottom right)", "A169", "A12A", 0, 0, 64, 0, 0 ],
                             [ "Elevator Cave G West Exit (Top left)", "A16A", "A12B", 0, 0, 128, 0, 0 ],
                             [ "Elevator Cave G East Exit (Top Right)", "A16B", "A12C", 0, 0, 192, 0, 0 ],
                             [ "Elevator Cave H West Exit (Top left)", "A16C", "A12D", 0, 0, 0, 0, 0 ],
                             [ "Elevator Cave H East Exit (Top Right)", "A16D", "A12E", 0, 0, 64, 0, 0 ],
                             [ "Elevator Cave H North Exit (Bottom left)", "A16E", "A12F", 0, 0, 128, 0, 0 ],
                             [ "Elevator Cave H South Exit (Bottom right)", "A16F", "A130", 0, 0, 192, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 2", "A170", "A131", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 1", "A171", "A132", 0, 0, 0, 0, 0 ],
                             [ "Maze Island's Magic Container", "A172", "A133", 0, 0, 0, 0, 0 ],
                             [ "Bridge back to East Hyrule", "A173", "A134", 0, 0, 0, 128, 0 ],
                             [ "Cave A back to West Hyrule", "A175", "A136", 0, 0, 0, 128, 0 ],
                             [ "Cave K back to West Hyrule", "A176", "A137", 0, 0, 0, 128, 0 ],
                             [ "Maze Palace", "A17F", "A140", 0, 0, 0, 128, 0 ],
                             [ "Maze Island Child", "A182", "A143", 0, 0, 0, 0, 0 ],
                             [ "Death Mountain's Magic Container", "A183", "A144", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 3", "A184", "A145", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 7", "A185", "A146", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 4", "A186", "A147", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 5", "A187", "A148", 0, 0, 0, 0, 0 ],
                             [ "Maze Island Forced Battle Scene 6", "A188", "A149", 0, 0, 0, 0, 0 ]]]

        # Keep track of location to move
        self.movelocation = -1
        self.movelocationprevx = -1
        self.movelocationprevy = -1
                            
    # End __init__

    def preferences(self):
        preferencesWindow = Toplevel(self.master)
        Button(preferencesWindow, text="Close", command=preferencesWindow.destroy).pack(pady=10)

    def about(self):
        aboutWindow = Toplevel(self.master)
        Label(aboutWindow, text="Zelda2MapEdit - by matal3a0\n\nLatest source available from:\nhttps://github.com/matal3a0/Zelda2MapEdit").pack(padx=10, pady=10)
        Button(aboutWindow, text="Close", command=aboutWindow.destroy).pack(pady=10)

    def selectterrain(self, terrain):
        # Raise buttons
        self.tile_0_btn.config(relief=RAISED)
        self.tile_1_btn.config(relief=RAISED)
        self.tile_2_btn.config(relief=RAISED)
        self.tile_3_btn.config(relief=RAISED)
        self.tile_4_btn.config(relief=RAISED)
        self.tile_5_btn.config(relief=RAISED)
        self.tile_6_btn.config(relief=RAISED)
        self.tile_7_btn.config(relief=RAISED)
        self.tile_8_btn.config(relief=RAISED)
        self.tile_9_btn.config(relief=RAISED)
        self.tile_a_btn.config(relief=RAISED)
        self.tile_b_btn.config(relief=RAISED)
        self.tile_c_btn.config(relief=RAISED)
        self.tile_d_btn.config(relief=RAISED)
        self.tile_e_btn.config(relief=RAISED)
        self.tile_f_btn.config(relief=RAISED)
        self.bracketbtn.config(relief=RAISED)

        # Set terrain and sink the button
        self.selectedterrain = terrain

        if terrain == "0":
            self.tile_0_btn.config(relief=SUNKEN)
        elif terrain == "1":
            self.tile_1_btn.config(relief=SUNKEN)
        elif terrain == "2":
            self.tile_2_btn.config(relief=SUNKEN)
        elif terrain == "3":
            self.tile_3_btn.config(relief=SUNKEN)
        elif terrain == "4":
            self.tile_4_btn.config(relief=SUNKEN)
        elif terrain == "5":
            self.tile_5_btn.config(relief=SUNKEN)
        elif terrain == "6":
            self.tile_6_btn.config(relief=SUNKEN)
        elif terrain == "7":
            self.tile_7_btn.config(relief=SUNKEN)
        elif terrain == "8":
            self.tile_8_btn.config(relief=SUNKEN)
        elif terrain == "9":
            self.tile_9_btn.config(relief=SUNKEN)
        elif terrain == "a":
            self.tile_a_btn.config(relief=SUNKEN)
        elif terrain == "b":
            self.tile_b_btn.config(relief=SUNKEN)
        elif terrain == "c":
            self.tile_c_btn.config(relief=SUNKEN)
        elif terrain == "d":
            self.tile_d_btn.config(relief=SUNKEN)
        elif terrain == "e":
            self.tile_e_btn.config(relief=SUNKEN)
        elif terrain == "f":
            self.tile_f_btn.config(relief=SUNKEN)
        elif terrain == "x":
            self.bracketbtn.config(relief=SUNKEN)

    def openromfile(self):
        # Save before?
        if self.edited != 0:
            result = tkMessageBox.askyesnocancel("Zelda2MapEdit", "Save before opening new file?") 
            if result is True:
                self.saveromfile()

        # Open file dialog
        options = {}
        options['defaultextension'] = '.nes'
        options['filetypes'] = [('Rom files', '.nes'), ('all files', '.*')]
        options['title'] = 'Open romfile'
        self.filename = askopenfilename(**options)
        
        # Open rom file
        if self.filename:
            try:
                handle = open(self.filename,"r+b")
            except IOError:
                message = "Cannot open file %s" % self.filename
                tkMessageBox.showerror("Cannot open file", message)
                return
        else:
            return
        # Clean breakpoints
        self.breakpoints = [ [], [], [], [] ]

        # Loop over the four startlocations in rom
        for index, maplocation in enumerate(self.mapstartlocations):
            yoffset = index*self.mapsizey # Offset in maparray depending on which map
            handle.seek(maplocation)
            # Read a byte at a time, decode to mapstring, until size == mapsizex*mapsizey
            # Also find breakpoints in map
            mapstring = ""
            prevterrain = ""
            prevcount = ""
            xcount = 0
            ycount = 0
            while len(mapstring) < self.mapsizex*self.mapsizey:
                rawmapdata = handle.read(1)
                # Convert rawmapdata to string 
                strmapdata = rawmapdata.encode("hex")

                #if index == 2:
                #    print strmapdata,

                # Calculate map data
                terraintype = strmapdata[1]
                terraincount = int(strmapdata[0], 16)+1
                # Keep track of coordinates in map 
                xcount += terraincount

                # Add to output_string
                for x in range(terraincount):
                    mapstring += terraintype

                # Find breakpoints 
                # A breakpoint can be identified by two bytes of the same terrain
                # and the the counting-part of the previous byte is not 16.
                # Also check that we are not on the edge of the map,
                # the encoding algorithm will place those breakpoints automatically
                if terraintype == prevterrain and prevcount != 16 and xcount-terraincount-1 >= 0: 
                    #sys.stdout.write("breakpoint! "+str(hex(prevcount-1)[2:])+str(prevterrain)+" "+str(hex(terraincount-1)[2:])+str(terraintype)+" "+str(xcount)+","+str(ycount)+"\n")
                    bp = [ xcount-terraincount, ycount ]
                    self.breakpoints[index].append(bp)
                prevterrain = terraintype
                prevcount = terraincount

                # If end of line, wrap around
                if xcount == 64:
                    xcount = 0
                    ycount += 1

            # Populate maparray with the decoded string
            y = 0+yoffset 
            x = 0
            for c in mapstring:
                self.maparray[x][y] = c
                x += 1
                if x == self.mapsizex:
                    y += 1
                    x = 0
                if y == self.mapsizey+yoffset:
                    break
            #print mapstring 

        # Read locations
        for i, _ in enumerate(self.maplocations):
            for j, _ in enumerate(self.maplocations[i]):
                handle.seek(int(self.maplocations[i][j][1], 16))
                self.maplocations[i][j][3] = int(handle.read(1).encode("hex"), 16)
                handle.seek(int(self.maplocations[i][j][2], 16))
                self.maplocations[i][j][4] = int(handle.read(1).encode("hex"), 16)

        # Close file
        handle.close()

        # Default to West Hyrule
        self.changemap(0)

        # Enable editing
        self.editenabled = 1
        self.mapmenu.entryconfig("West Hyrule", state="normal")
        self.mapmenu.entryconfig("Death Mountain", state="normal")
        self.mapmenu.entryconfig("East Hyrule", state="normal")
        self.mapmenu.entryconfig("Maze Island", state="normal")
        self.filemenu.entryconfig("Save", state="normal")

        # Not edited
        self.edited = 0

    def saveromfile(self):
        currentactivemap = self.activemap

        # open file handle in write binary mode
        try:
            handle = open(self.filename, "r+b")
        except IOError:
            print "Cannot open file for saving"

        # Loop over the four startlocations in rom
        for index, maplocation in enumerate(self.mapstartlocations):
            self.activemap = index
            yoffset = index*self.mapsizey # Offset in maparray depending on which map

            # Convert maparray to encoded string and save to correct location in romfile
            mapstring = ""
            for y in range(self.mapsizey):
                for x in range(self.mapsizex):
                    mapstring += str(self.maparray[x][y+yoffset])

            encodedstring = self.mapencode(mapstring)
            handle.seek(maplocation)

            # Read two characters, convert to a byte, write to file
            i = 0
            while i+1 < len(encodedstring):
                byte = encodedstring[i]+encodedstring[i+1]
                byte = byte.decode("hex")
                handle.write(byte)
                i += 2

        # Save locations
        for i, _ in enumerate(self.maplocations):
            for j, _ in enumerate(self.maplocations[i]):
                # Convert integer value to hex-string without 0x, and pad with 0 if needed
                x = hex(self.maplocations[i][j][3])[2:].zfill(2)
                y = hex(self.maplocations[i][j][4])[2:].zfill(2)
                # Convert string to binary value
                x = x.decode("hex")
                y = y.decode("hex")
                # Find address in romfile and write value
                handle.seek(int(self.maplocations[i][j][1], 16))
                handle.write(x) 
                handle.seek(int(self.maplocations[i][j][2], 16))
                handle.write(y)
                
                # Save offset for palace locations
                if self.maplocations[i][j][7] != 0:
                    offset_in_array = (self.maplocations[i][j][4]-self.maplocations[i][j][6]-30)*64+self.maplocations[i][j][3]
                    
                    offsetsum = 0
                    j = 0
                    bytecounter = 0
                    while j+1 < len(encodedstring):
                        offsetsum += int(encodedstring[j], 16)+1
                        j += 2
                        bytecounter += 1
                        if offsetsum == offset_in_array:
                            # Offset base is 0x7C00 (31744)
                            # Add offset to base, write as table at address
                            offsetstring = hex(j/2+31744)[2:].zfill(2)
                            byte1 = offsetstring[2:]
                            byte2 = offsetstring[:2]
                            byte1 = byte1.decode("hex")
                            byte2 = byte2.decode("hex")
                            handle.seek(int(self.maplocations[i][j][7], 16))
                            handle.write(byte1)
                            handle.write(byte2)
                            break

        handle.close()
        self.edited = 0
        self.activemap = currentactivemap

    def changemap(self, mapnumber):
        self.activemap = mapnumber
        self.drawmap()

        # Update sizelabel
        mapsize = self.mapsizeinbytes()
        self.updatemapsizelabel(mapsize)
        
    def mapencode(self, input_string):
        #print "mapencode"
        ycount = 0
        xcount = 0 # Encoding must stop at 64 tiles per line of map
        tilecount = 1
        prev = ''
        output_string = ""
        for character in input_string:
            pos = [xcount,ycount]
            if character != prev:
                if prev:
                    output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
                prev = character
                if (xcount > 63):
                    xcount = 0
                    ycount += 1
            elif (tilecount == 16):
                output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
                if (xcount > 63):
                    xcount = 0
                    ycount += 1
            elif (xcount > 63):
                output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
                xcount = 0
                ycount += 1
            elif (pos in self.breakpoints[self.activemap]):
                output_string += str(hex(tilecount-1)[2:])+prev
                tilecount = 1
            else:
                tilecount += 1
            xcount += 1
    
        output_string += str(hex(tilecount-1)[2:])+character
        #print output_string
        return output_string

    def drawlocations(self):
        # loop over locations, print square around
        for l in self.maplocations[self.activemap]:
            x = l[3]-l[5]
            y = l[4]-l[6]
            self.canvas.create_rectangle((x*16), ((y-30)*16), (x*16+16)-1, ((y-30)*16+16)-1, outline="blue", width=1)
            #self.canvas.create_rectangle((x*16)-1, ((y-30)*16)-1, (x*16+16)+1, ((y-30)*16+16)+1, outline="blue", width=2)


    def drawmap(self):
        canvasposx = 0
        canvasposy = 0

        for y in range(self.mapsizey):
            for x in range(self.mapsizex):
                self.drawtile(canvasposx,canvasposy)
                canvasposx+=1
                if canvasposx== 64:
                    canvasposx = 0
                    canvasposy+= 1

        self.drawlocations()
        self.drawbreakpoints()

    def drawtile(self, x, y):
        #print "drawtile"
        offset = self.activemap

        if self.maparray[x][y+(self.mapsizey*offset)] == "0":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_0)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "1":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_1)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "2":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_2)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "3":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_3)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "4":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_4)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "5":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_5)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "6":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_6)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "7":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_7)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "8":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_8)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "9":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_9)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "a":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_a)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "b":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_b)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "c":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_c)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "d":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_d)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "e":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_e)
        elif self.maparray[x][y+(self.mapsizey*offset)] == "f":
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.img_f)
        else:
            self.canvas.create_image(x*16,y*16, anchor=NW, image=self.error_img)

    def drawbreakpoints(self):
        #print "drawbreakpoints"
        for b in self.breakpoints[self.activemap]:
            #print "for b in self.breakpoints"
            x = b[0]
            y = b[1]
            self.canvas.create_line(((x-1)*16)+16, (y*16), ((x-1)*16)+16, (y*16)+16, fill="red", width=1)
            self.canvas.create_line(((x-1)*16)+13, (y*16), ((x-1)*16)+19, (y*16), fill="red", width=1)
            self.canvas.create_line(((x-1)*16)+13, (y*16)+15, ((x-1)*16)+19, (y*16)+15, fill="red", width=1)

    def quit(self):
        # Save before exit?
        if self.edited != 0:
            result = tkMessageBox.askyesnocancel("Zelda2MapEdit", "Save before exit?") 
            if result is True:
                self.saveromfile()
                self.master.destroy()
            elif result is False:
                self.master.destroy()
        else:
            self.master.destroy()

    def mousemove(self, event):
        #print "mousemove"
        if self.editenabled == 1:
            c = event.widget
            # Position on canvas
            x, y = c.canvasx(event.x), c.canvasy(event.y)
            # Calculate position on map
            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            offset = self.activemap

            # Make sure we are inside borders of the map
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0:
                # Y-axis seems to be offset with 30 on map compared to array
                #text = "(" + `x` + "," + `y+30` + ")"
                text = `self.maparray[x][y+(self.mapsizey*offset)]` + " (" + `x` + "," + `y+30` + ")"
                self.coordlabeltext.set(text)
   
                self.locationlabeltext.set("")
                for l in self.maplocations[self.activemap]:
                    if l[3]-l[5] == x and l[4]-l[6] == y+30:
                        text = l[0] + " (" + `l[3]-l[5]` + "," + `l[4]-l[6]` + ") (offset by: " + `l[5]` + "," + `l[6]` + ")"
                        self.locationlabeltext.set(text)
                        break

    def mapsizeinbytes(self):
        #print "mapsizeinbytes"
        yoffset = self.activemap*self.mapsizey
        # Generate mapstring
        mapstring = ""
        for y in range(self.mapsizey):
            for x in range(self.mapsizex):
                mapstring += str(self.maparray[x][y+yoffset])
        # Encode it
        encmapstring = self.mapencode(mapstring)

        # Return length/2 (BBF332 = 3 bytes)
        return len(encmapstring)/2

    def updatemapsizelabel(self,mapsize):
        #print "updatemapsizelabel"
        origmapsize = self.origmapsizes[self.activemap]

        text = `mapsize` + "/" + `origmapsize`
        self.mapsizelabeltext.set(text)

        # Change to red if larger then original mapsize
        if mapsize > origmapsize:
            self.mapsizelabel.config(fg="red")
        else:
            self.mapsizelabel.config(fg="black")

    def leftpress(self, event):
        #print "leftpress"
        yoffset = self.mapsizey*self.activemap

        if self.editenabled == 1:
            c = event.widget
            # Mouse down coordinates 
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            # Position in the map
            maparrayx = int(x)/16
            maparrayy = int(y)/16
            # Position to put breakpoint
            maparraybreakpointx = (abs(int(x)-8)/16)+1

            # Update maparray
            if self.selectedterrain == 'x':
                #Toggle breakpoint at location
                self.togglebreakpoint(maparraybreakpointx, maparrayy)
            else:
                # Update tile
                self.maparray[maparrayx][maparrayy+yoffset] = self.selectedterrain

            # Draw surrounding tiles, locations and breakpoints
            self.drawtile(maparrayx,maparrayy)
            self.drawtile(maparrayx-1,maparrayy)
            if maparrayx+1 < self.mapsizex: # Don't draw out of bounds
                self.drawtile(maparrayx+1,maparrayy)
            self.drawlocations()
            self.drawbreakpoints()

            # Edited
            self.edited = 1

    def leftmotion(self, event):
        #print "leftmotion"
        yoffset = self.mapsizey*self.activemap

        if self.editenabled == 1:
            c = event.widget
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            maparrayx = int(x)/16
            maparrayy = int(y)/16

            if self.selectedterrain != 'x':
                if self.maparray[maparrayx][maparrayy+yoffset] != self.selectedterrain:
                    self.maparray[maparrayx][maparrayy+yoffset] = self.selectedterrain
                    self.drawtile(maparrayx,maparrayy)
                    #self.drawlocations()
                    #self.drawbreakpoints()

    def leftrelease(self, event):
        #print "leftrelease"
        if self.editenabled == 1:
            # Calculate map size and update label
            mapsize = self.mapsizeinbytes()
            self.updatemapsizelabel(mapsize)
            self.drawlocations()
            self.drawbreakpoints()

    def rightpress(self, event):
        if self.editenabled == 1:
            c = event.widget
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            
            # Make sure we are inside borders of the map
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0:
                # Find a location to move

                for p, l in enumerate(self.maplocations[self.activemap]):
                    if l[3]-l[5] == x and l[4]-l[6] == y+30:
                        self.movelocation = p
                        self.movelocationprevx = x
                        self.movelocationprevy = y
                        break

    def rightmotion(self, event):
        if self.editenabled == 1:
            c = event.widget
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            
            # Make sure we are inside borders of the map, and we found a location to move
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0 and self.movelocation >= 0:
                self.drawtile(self.movelocationprevx,self.movelocationprevy)
                self.canvas.create_rectangle((x*16), ((y)*16), (x*16+16)-1, ((y)*16+16)-1, outline="red", width=1)
                self.movelocationprevx = x
                self.movelocationprevy = y

    def rightrelease(self, event):
        if self.editenabled == 1:
            c = event.widget
            x, y = c.canvasx(event.x), c.canvasy(event.y)

            x = int(self.round_down(x, 16))/16
            y = int(self.round_down(y, 16))/16
            
            # Make sure we are inside borders of the map, and we found a location to move
            if x < self.mapsizex and x >= 0 and y < self.mapsizey and y >= 0 and self.movelocation >= 0:
                self.maplocations[self.activemap][self.movelocation][3] = x+self.maplocations[self.activemap][self.movelocation][5]
                self.maplocations[self.activemap][self.movelocation][4] = y+30+self.maplocations[self.activemap][self.movelocation][6]

                self.movelocation = -1 
                self.drawmap()
                self.edited = 1

    def round_down(self, num, divisor):
        return num - (num%divisor)

    def togglebreakpoint(self, x, y):
        breakpoint = [x,y]
        #If breakpoint already exists at location, remove it. Otherwise add breakpoint
        if breakpoint in self.breakpoints[self.activemap]:
            self.breakpoints[self.activemap].remove(breakpoint) 
        else:
            self.breakpoints[self.activemap].append(breakpoint)

# End Class 

root = Tk()
app= Zelda2MapEdit(root)
root.mainloop()
