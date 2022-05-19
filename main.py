from gui.app import SampleApp
from entities.database import DataBase
import sqlite3
from database import CreateDataBase



if __name__ == "__main__":
    decision = input("Do you want to create the database? Y/N")
    main_db = DataBase(
        name="main_database.db",
        tables={
            "stakeholders": ['Name', 'Needs', 'Parent'],
            "needs": ['name', 'Description', 'Stakeholder', 'Requirements'],
            "requirements": ['Name', 'Description', 'Priority', 'Type', 'Source', 'Version', 'Author']}
    )
    if decision == "Y":
        CreateDataBase(main_db)

    app = SampleApp(main_db)

    app.mainloop()
