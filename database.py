import os, sys

class Database:

    def __init__(self):
        # map the tables in the database with keys as table names for quick access
        self.tables = {}

    def add_table(self, table):
        decision == 'y'
        # check if table already in DB and warn user
        if table.name in self.tables:
            print("There is already a table named " + table.name + "\n")
            decision = input("Would you like to overwrite it (y/n)?")
        if decision == 'y':
            self.tables[table.name] = table
            table.parent_database = self
            return True
        else:
            return False

    def delete_table(self, name):
        if name in self.tables:
            del self.tables[name]
            return True
        else:
            print("There is no table with the name " + name)
            return False

    # TODO: write out the database (and all tables) to ASCII text doc
    def write_database(self, path = ""):
        pass

    # TODO: read-in database from an ASCII text doc
    def read_database(self, path):
        pass

    # TODO: write out specific table to ASCII text doc
    def write_table(self, table, path = ""):
        pass

    # TODO: read-in specific table to ASCII text doc
    def read_table(self, path):
        pass
