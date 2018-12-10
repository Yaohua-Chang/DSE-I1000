import os, sys

class Database:

    def __init__(self):
        # map the tables in the database with keys as table names for quick access
        self.tables = {}

    def __repr__(self):
        for table_name in self.tables:
            print(self.tables[table_name])
            print("\n\r")
        return None

    def __str__(self):
        out = ""
        for _, table in self.tables.items():
            out += str(table)
        return out

    def add_table(self, table):
        decision = 'y'
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
            # check for cross-table dependency
            table_attributes = set(self.tables[name].attributes_names)
            for _, table in self.tables.items():
                if table == self.tables[name]:  # ignore table being deleted
                    continue
                if len(table_attributes.intersection(set(table.attributes_names))) > 0:
                    # table being deleted has attributes in the other table(s)
                    print("You cannot delete this table because its attributes are shared by " + table.name)
                    return False
            del self.tables[name]
            return True
        else:
            print("There is no table with the name " + name)
            return False

    def write_database(self, path = ""):
        f = open("database.txt", "w+")
        f.write(str(self))
        f.close()

    # TODO: read-in database from an ASCII text doc
    def read_database(self, path):
        pass

    def write_table(self, table, path = ""):
        f = open("table_" + table.name + ".txt", "w+")
        f.write(str(table))
        f.close()

    # TODO: read-in specific table to ASCII text doc (this might be difficult)
    def read_table(self, path):
        pass
