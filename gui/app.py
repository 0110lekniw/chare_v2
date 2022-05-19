import tkinter as tk
import pandas as pd
import numpy as np

from entities.database import DataBase
from gui.tables_types import Stakeholders, Needs, Requirements
from gui.record_view import RStakeholders, RNeeds, RRequirements

path_input_files = r'C:\GitHub\chare_v2\input_files\stakeholder_high_level.csv'

df = pd.read_csv(path_input_files, delimiter=';')
df = df.replace(np.nan, r' ', regex=True)
input_table = np.vstack((df.columns.to_numpy(), df.values))


class SampleApp(tk.Tk):
    def __init__(self, database: DataBase, *args, **kwargs):
        self.database = database
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('CHARE')
        self.iconbitmap(r'C:\GitHub\chare_v2\img\icon.ico')
        self.geometry('1120x600')

        container = tk.Frame(self)
        container.grid(row=2, column=0, columnspan=7, sticky='nsew')

        record_container = tk.Frame(self)
        record_container.grid(row=1, column=0, columnspan=7, sticky='nsew')

        self.frames = {}
        self.records = {}
        for F in (Stakeholders, Needs, Requirements):
            page_name = F.__name__
            frame = F(parent=container, controller=self, database=self.database)
            self.frames[page_name] = frame
            frame.grid(row=1, sticky="nsew")

        for FR in (RStakeholders, RNeeds, RRequirements):
            page_name = FR.__name__
            record = FR(record_parent=record_container, record_controller=self, database=self.database)
            self.records[page_name] = record
            record.grid(row=1, sticky="nsew")

        self.choices = {'Stakeholders', 'Needs', 'Requirements'}
        self.tkvar = tk.StringVar()
        self.tkvar.set('Stakeholders')
        self.popMenu = tk.OptionMenu(self, self.tkvar, *self.choices)
        self.popMenu.grid(row=0, column=0)
        self.show_frame()

        self.button1 = tk.Button(self, text="Go", command=lambda: self.show_frame())
        self.button1.grid(row=0, column=1)

    def show_frame(self):
        '''Show a frame for the given page name'''
        page_name = self.tkvar.get()
        frame = self.frames[page_name]
        frame.tkraise()
        '''Show a frame for the given page name'''
        page_name = self.tkvar.get()
        record_frame = self.records['R' + page_name]
        record_frame.tkraise()


