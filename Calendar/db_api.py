from PyQt5 import QtSql

class api():
    def __init__(self):
        # Connect to SQLite
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setConnectOptions("QSQLITE_ENABLE_SHARED_CACHE=1")
        self.db.setDatabaseName("test.db")
        self.db.open()

        """
        self.db.setHostName("geeksforgeeks")
        self.db.setUserName("geeks")
        self.db.setPassword("gfg")
        """

        if not self.db.open():
            print("Database failed to open")

    def select_all(self):
        # self.qry = "SELECT * FROM kitchens"
        # self.query = QtSql.QSqlQuery()
        # self.query.prepare(self.qry)
        # self.query.exec()

        query = QtSql.QSqlQuery()

        if query.exec_("SELECT * FROM kitchens"):

            # Loop through all rows
            while query.next():

                # Print columns by index
                print(
                    query.value(0),
                    query.value(1),
                    query.value(2)
                )

        else:
            print("Query failed")
            print(query.lastError().text())