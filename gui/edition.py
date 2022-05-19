import tkinter as tk

from database import submit, getRecord, update, deleteRecord
from get_list import getList


class BaseSubLayer(tk.Frame):
    def __init__(self, parent, controller, database):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.data_labels = getList(database.tables.values())[self.table_number]

        tk.Label(self, text="Entry Data", borderwidth=5).grid(row=0, column=2)
        tk.Label(self, text="Properity", borderwidth=5).grid(row=1, column=0)
        tk.Label(self, text="Value", borderwidth=5).grid(row=2, column=0)

        self.entries = []
        self.labels = []

        for i, data_label in enumerate(self.data_labels):
            self.labels.append(tk.Label(self, text=data_label, width=20))
            self.labels[i].grid(row=1, column=1 + i, sticky='we')
            self.entries.append(tk.Entry(self, width=10))
            self.entries[i].grid(row=2, column=1 + i, sticky='we')

        self.button_add = tk.Button(self, text="Add", command=lambda: self.add_record(database))
        self.button_add.grid(row=3, column=0)

        self.button_edit = tk.Button(self, text="Show", command=lambda: self.show_record(database))
        self.button_edit.grid(row=3, column=1)

        self.entry_show = tk.Entry(self, width=20)
        self.entry_show.grid(row=3, column=2)
        self.entry_show.insert(0, 'id')

        self.button_delete = tk.Button(self, text="Delete", command=lambda: self.delete_record(database))
        self.button_delete.grid(row=3, column=3)

        self.button_delete = tk.Button(self, text="Edit", command=lambda: self.edit_record(database))
        self.button_delete.grid(row=3, column=4)

        self.currently_showed = self.entry_show.get()

    def add_record(self, database):
        data_to_add = self.read_data()
        submit(self.table_number, database, data_to_add)
        self.reset_entries()
        return

    def edit_record(self, database):
        self.currently_showed = self.entry_show.get()
        data_to_edit = self.read_data()
        self.reset_entries()
        update(self.table_number, database, data_to_edit, current_oid=self.currently_showed)
        self.reset_id_entry()

    def delete_record(self, database):
        self.currently_showed = self.entry_show.get()
        self.reset_entries()
        deleteRecord(self.table_number, database, current_oid=self.currently_showed)
        self.reset_id_entry()

    def read_data(self):
        entry_data = {}
        i = 0
        reference_labels = self.data_labels
        if 'oid' in reference_labels: reference_labels.remove('oid')
        for data_label in reference_labels:
            entry_data[data_label] = self.entries[i].get()
            i += 1
        return entry_data

    def reset_entries(self):
        for entry in self.entries:
            entry.delete(0, tk.END)

    def show_record(self, database):
        self.reset_entries()
        self.currently_showed = self.entry_show.get()
        record = getRecord(self.table_number, database, self.currently_showed)
        i = 0
        for entry in self.entries:
            entry.insert(0, record[0][i])
            i += 1

    def reset_id_entry(self):
        self.entry_show.delete(0, tk.END)
        self.entry_show.insert(0, 'id')


