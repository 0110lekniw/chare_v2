import sqlite3
import numpy as np
from entities.database import DataBase
from get_list import getList


def Query(table_number, database: DataBase):
    conn = sqlite3.connect(database.name)
    table_name = getList(database.tables)[table_number]

    # creating cursor
    c = conn.cursor()
    # Insert Into Table
    c.execute(f"SELECT *, oid FROM {table_name}")
    # fetchone, fetchmany, fetchall
    records = c.fetchall()
    data = np.array(records)
    if len(np.shape(data)) == 1:
        data_labels = np.array(database.tables[table_name])
        returned_data = np.vstack((data_labels, np.zeros((4, len(data_labels)))))
    else:
        labels = database.tables[table_name]
        if len(labels) != data.shape[1]:
            labels.append("oid")
        data_labels = np.array(labels)
        returned_data = np.vstack((data_labels, data))
    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()
    return returned_data


def CreateDataBase(database: DataBase):
    conn = sqlite3.connect(database.name)
    # creating cursor
    c = conn.cursor()
    # Insert Into Table
    for table_name, values in database.tables.items():
        tables_description = ""
        for data_label in values:
            tables_description += f"{data_label} text,"
            if data_label == values[-1]:
                tables_description = tables_description[:-1]
        sql_command = f"CREATE TABLE {table_name}({tables_description})"
        c.execute(sql_command)
    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()


def submit(table_number, database: DataBase, data_to_add):
    conn = sqlite3.connect(database.name)
    table_name = getList(database.tables)[table_number]
    table_keys = getList(database.tables[table_name])
    # creating cursor
    c = conn.cursor()

    table_description = ""
    for name in table_keys:
        table_description += f":{name},"
        if name == table_keys[-1]:
            table_description = table_description[:-1]
    sql_command = f"INSERT INTO {table_name} VALUES ({table_description})"
    c.execute(sql_command, data_to_add)
    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()


def update(table_number, database: DataBase, data_to_update, current_oid):
    conn = sqlite3.connect(database.name)
    table_name = getList(database.tables)[table_number]
    table_keys = getList(database.tables[table_name])
    # creating cursor
    c = conn.cursor()
    new_update = {}
    i = 0
    for key in data_to_update:
        new_update[f"update{i}"]=data_to_update[key]
        i+=1
    new_update[f'update{i+1}'] = current_oid
    table_description = ""
    j = 0
    for key in data_to_update:
        if key == table_keys[-1]:
            table_description += f"{key} = :update{j} \n"
        else:
            table_description += f"{key} = :update{j}, \n"
        j+=1
    sql_command = f"UPDATE {table_name} SET \n {table_description} \n WHERE oid = :update{j+1}"
    c.execute(sql_command, new_update)
    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()

def getRecord(table_number, database: DataBase, current_oid):
    # Create a database or connect to one
    conn = sqlite3.connect(database.name)
    table_name = getList(database.tables)[table_number]
    # creating cursor
    c = conn.cursor()
    # Insert Into Table
    c.execute(f"SELECT * FROM {table_name} WHERE oid = {current_oid}" )
    # fetchone, fetchmany, fetchall
    records = np.array(c.fetchall())
    conn.close()
    return records

def deleteRecord(table_number, database: DataBase, current_oid):
    # Create a database or connect to one
    conn = sqlite3.connect(database.name)
    table_name = getList(database.tables)[table_number]
    # creating cursor
    c = conn.cursor()
    # Insert Into Table
    c.execute(f"DELETE FROM {table_name} WHERE oid = {current_oid}" )
    # Commit changes
    conn.commit()
    conn.close()
