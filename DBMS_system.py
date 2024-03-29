from database import Database
from table import Table
from attribute import Attribute
from database import Database


def create_tables():
    table_name = input("Please input new table name:")
    attrs = []
    print("Please input at least one attribute. Input 'quit' at any time to stop.")

    while True:
        input_str = input("Please input the name and type (\'integer\'  or \'string\') for one attribute. Use \',\' as delimiter :")
        if input_str == "quit":
            if len(attrs) == 0:
                print("You need to input at least 1 attribute for the new table")
            else:
                break
        else:
            input_split = input_str.replace(" ","").split(",")
            if len(input_split) != 2 or input_split[1] == "":
                print("The input is not correct, please input again.")
            else:
                attrs.append(Attribute(input_split[0], input_split[1]))
                print("Successfully add a new attribute")

    new_table = Table(table_name, attrs)
    print("The tabel " + table_name + " have created successfully!")
    print(new_table)

    return new_table


def create_constraint(table, db):
    while True:
        input_str = input("Please input Boolean condition:")
        if input_str == "quit":
            break
        feedback = table.add_boolean_conditions(input_str.replace(" ",""))
        print(feedback)

    while True:

        input_str = input("Please input FD:").replace(" ","")
        if input_str == "quit":
            if len(table.fds) == 0:
                print("Please input at least one FD for the table.")
                continue
            else:
                break
        feedback = table.add_fd(input_str)
        print(feedback)

    while True:
        if len(table.fds) == 0:
            break
        else:
            table.print_fds()
        input_str = input("Do you want to remove some Fds(yes or no):")
        if input_str == "no":
            break
        else:
            input_str = input("Please input a Fd that you want to remove:").replace(" ","")
            feedback = table.remove_fd(input_str)
            print(feedback)

    while True:

        input_str = input("Please input MVD:").replace(" ","")
        if input_str == "quit":
            break

        feedback = table.add_mvd(input_str)
        print(feedback)

#     Remove this/ Not neccessary
#     while True:
#         input_str = input("Please input foreign key and its table(use , as delimiter):")
#         if input_str == "quit":
#             break
#         input_split = input_str.replace(" ","").split(",")
#         if len(input_split) != 2 or input_split[1] == "":
#             print("Invalid input, please input again!")
#             continue
#         if input_split[1] not in db.tables:
#             print("There is no such table!")
#             continue
#         else:
#             foregin_table = db.tables[input_split[1]]

#         result = foregin_table.get_keys().pop()
#         if not input_split[0] in result:
#             print("The key is not the key in the table " + input_split[1] + ".")
#             continue

#         table.add_foreign_key(input_str[0], foregin_table)
#         print("Add foreign key successfully")

    return table


def update_normal_form(db, table):
    if table.nf == "":
        table.get_normal_form()

    print("Currently this table [" + table.name + "] has normal form: " + table.nf)

    if not (table.nf == "3NF" or table.nf == "BCNF"):
        print("You can either delete this table or update its FD's.")
        decision = input("Either type \'del\' for deletion of the table or \'u\' to update:")

        if decision == 'del':
            input_str = input("Are you sure delete the table "+ table.name +"?(yea or no)")
            if input_str == "yes":
                db.delete_table(table.name)
                print("delete the tabel [" + table.name + "] successfuly")
                table = None
            else:
                update_normal_form(db, table)
        elif decision == 'u':
            done = False
            while not done:
                print("Current FD(s) in the table: " + str(table.fds) + "\n")
                input_str = input("Type \'a\' to add a new FD or \'d\' to delete a FD: ")
                if input_str == 'a':
                    new_fd = input("Add a new FD: ")
                    feedback = table.add_fd(new_fd.replace(" ",""))
                    print(feedback)
                    table.get_normal_form()
                    again = input("The table now has normal form " + table.nf + " would you like to continue (y/n)?")
                    if again == 'n':
                        done = True

                elif input_str == 'd':
                    del_fd = input("Enter FD to be deleted: ")
                    feedback = table.remove_fd(del_fd.replace(" ",""))
                    print(feedback)
                    if len(table.fds) == 0:
                        print("The table has no FD left! Please start again")
                        break

                    else:
                        table.get_normal_form()
                        again = input("The table now has normal form " + table.nf + " would you like to continue (y/n)?")
                        if again == 'n':
                            done = True
                else:
                    print("That's not a valid decision!")

        else:
            print("That's not a valid decision!")

    return table

def user_define_key(table):
    table.get_keys()
    print("Please define keys for the table [" + table.name + "].")
    table.user_define_key()

def fake_data():
    A = Attribute("A", "integer")
    B = Attribute("B", "integer")
    C = Attribute("C", "integer")
    D = Attribute("D", "string")
    E = Attribute("E", "integer")
    F = Attribute("F", "string")

    new_table1 = Table("test1", [A,B,C])
    new_table2 = Table("test2", [C,D,E])
    # new_table3 = Table("test3", [A,B,C,D,E,F])

    new_table1.add_fd("A->B")
    new_table1.add_fd("B->C")
    new_table1.master_key = "A"
    # new_table1.add_tuple((1,2,3,'4',5,'6'))
    # new_table1.add_tuple((11,12,13,14,15,'16'))

    new_table2.add_fd("DE->C")
    new_table2.master_key = "DE"

    # new_table3.add_fd("A->B")
    # new_table3.master_key = "ACDEF"

    db = Database()
    db.add_table(new_table1)
    db.add_table(new_table2)
    # db.add_table(new_table3)

    return db

if __name__ == "__main__":
    # db = Database()
    # Task I.a
    # Define new tables
    # while True:
    #     new_table = create_tables()
    #     db.add_table(new_table)
    #     is_add_new_table = input("Do you still want to define a new table(yes or no)?")
    #     if is_add_new_table == "no":
    #         break

    # Task I.b
    # Ask users to input possible constraints for each defined table
    # db = fake_data()
    # for table_name, table in db.tables.items():
    #     print("Please input constraint for the table [" + table.name + "]. Input 'quit' at any time to stop.")
    #     table = create_constraint(table, db)

    # Task I.c
    # Evaluate the NF category for the user defined DB
    # for table_name, table in db.tables.copy().items():
    #     table = update_normal_form(db, table)
    #     if table != None:
    #         db.tables[table_name] = table

    # Task I.d
    # Ask users to define keys for each table
    db = fake_data()
    for table_name, table in db.tables.items():
        user_define_key(table)

    # Task II.a
    # Input new tuples to all tables
    db = fake_data()
    while True:
        print("The tables in current db: \n")
        print(db)
        input_str = input("Please choose a table in order to input a new tuple into it(or quit to terminate): ")
        if input_str == 'quit':
            break
        if input_str in db.tables:
            table_to_add = db.tables[input_str]
            while True:
                in_tuple_str = input("Input a new tuple into " + input_str + " using \',\' as delimiter(or quit):")
                if in_tuple_str == "quit":
                    break
                in_tuple_as_list = list(in_tuple_str.split(','))
                type_list = [a.type for a in table_to_add.attributes]
                try:
                    for i, el in enumerate(in_tuple_as_list):
                        if type_list[i] == "integer":
                            in_tuple_as_list[i] = int(el)
                except:
                    print("Invalid tuple, please input again!")
                    continue
                # handle case of integer
                table_to_add.add_tuple(tuple(in_tuple_as_list))
        else:
            print("Invaild input, please input again!")

    # Task II.b
    # Delete a tuple based on key value
    while True:
        print("The tables in current db: \n", db)
        input_str = input("Would you like to delete a tuple from any table? (y/n)")
        if input_str == 'n':
            break
        else:
            table_name = input("Which table would you like to delete from?")
            table = db.tables[table_name]
            print("This the table you will be deleting from: \n", table)
            print("Which has the key: ", table.keys)
            key = input("Please provide the key for the tuple you'd like to delete: ")
            table.remove_tuple(key)

    # Task II.c
    # TODO: find tuples based on conditions

    # Group by attribute(s) in specific table
    while True:
        print("The tables in current db: \n", db)
        input_str = input("Would you like to group by any attributes from the tables (y/n)?")
        if input_str == 'n':
            break
        else:
            table_name = input("Which table would you like to group by in?")
            table = db.tables[table_name]
            attr_name = input("Which attribute would you like to group by?")
            table.group_by(attr_name)

    # TODO Task II.d
    # Choose to perform the operators for two tables

    # TODO Task II.e
    # Delete a table and ensure the across-table integrity
