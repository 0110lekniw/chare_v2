import tkinter as tk
from abc import ABC

import numpy as np

from database import Query


class RecordSubLayer(tk.Frame):
    def __init__(self, record_parent, record_controller, database):
        tk.Frame.__init__(self, record_parent)
        self.controller = record_controller
        self.show_data(database)
        # An approach for creating the table

    def show_data(self, database):
        for widget in self.winfo_children():
            widget.destroy()

            # this will clear frame and frame will be empty
            # if you want to hide the empty panel then
            self.pack_forget()
        table = self.generateData(database, self.table_number)
        total_rows = table.shape[0]
        total_columns = table.shape[1]
        self.entries = {}
        if not self.entries:
            for entry in self.entries:
                self.entries[entry].grid_forget()
        for i in range(total_rows):
            for j in range(total_columns):
                print(i)
                if i == 0:
                    self.entry = tk.Entry(self, width=20, bg='LightSteelBlue')
                else:
                    self.entry = tk.Entry(self, width=20)

                self.entry.grid(row=i, column=j)
                self.entry.insert(tk.END, table[i][j])
        self.refresh_button = tk.Button(self, text="Refresh", command=lambda: self.show_data(database))
        self.refresh_button.grid(row=0, column=j+1)

        self.validate_button = tk.Button(self, text="Check", command=lambda: self.checkData(database))
        self.validate_button.grid(row=2, column=j + 1)
        del self.entries
        return

    def generateData(self, database, table_number):
        returned_data = Query(table_number, database)
        return returned_data

    def checkData(self, database):
        stakeholder_table = Query(0, database)[:, :]
        stakeholder_names = stakeholder_table[0, :]
        stakeholder_table = stakeholder_table[1:, :]

        need_table = Query(1, database)[:, :]
        needs_names = need_table[0, :]
        needs_table = need_table[1:, :]

        requirements_table = Query(2, database)[:, :]
        requirements_names = requirements_table[0, :]
        requirements_table = requirements_table[1:, :]

        stakeholders_required = [0, 1]
        #check if all required data are filled
        for scolumn in stakeholders_required:
            stake_holders_check = np.where(stakeholder_table[:, scolumn] == '')[0]
            if np.any(stake_holders_check):
                print(f"The stakeholders do not have defined {stakeholder_names[scolumn]} in: {stake_holders_check}")

        needs_required = [0, 1, 2, 3]
        for ncolumn in needs_required:
            needs_check = np.where(needs_table[:, ncolumn] == '')[0]
            if np.any(needs_check):
                print(f"The needs do not have defined {needs_names[ncolumn]} in: {needs_check}")

        requirements_required = [0, 1, 2, 3, 4, 5, 6]
        for rcolumn in requirements_required:
            requirements_check = np.where(requirements_table[:, rcolumn] == '')[0]
            if np.any(requirements_check):
                print(f"The requirements do not have defined {requirements_names[rcolumn]} in: {requirements_check}")
        element_number = 0
        requirements_source_check = []
        for element in requirements_table[:, 4]:
            if ',' in element:
                requirements_source_check.append(element_number)
            element_number+=1
        if np.any(requirements_source_check):
            print(f"The requirement has defined multiple sources in: {requirements_source_check}")
        print('checked')


class RStakeholders(RecordSubLayer, ABC):
    table_number = 0


class RNeeds(RecordSubLayer, ABC):
    table_number = 1


class RRequirements(RecordSubLayer, ABC):
    table_number = 2
