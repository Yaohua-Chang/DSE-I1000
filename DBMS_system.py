from database import Database
from table import Table
from attribute import Attribute
from database import Database

# Task I.a
def create_table():
    db = Database()
    table_name = input("Please input new table name:")
    attrs = []

    print("Please input at least one attribute. Input 'quit' at any time to stop.")

    while True:
        input_str = input("Please input the name and type (use , as delimiter) for one attribute:")
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
    db.add_table(new_table)
    print("The tabel " + table_name + " have created successfully!")
    print(new_table)

    return new_table

# Task I.b
def create_constraint(table):   
    print("Please input at least one constraint. Input 'quit' at any time to stop.")

    while True:
        input_str = input("Please input Boolean condition:")
        if input_str == "quit":
            break
        feedback = new_table.add_boolean_conditions(input_str.replace(" ",""))
        print(feedback)

    while True:

        input_str = input("Please input FD:")
        if input_str == "quit":
            break
        feedback = new_table.add_fd(input_str)
        print(feedback)

    while True:
        if len(new_table.fds) == 0:
            break
        else:
            new_table.print_fds()
        input_str = input("Do you want to remove some Fds(yes or no):")
        if input_str == "no":
            break
        else:
            input_str = input("Please input a Fd that you want to remove:")
            feedback = new_table.remove_fd(input_str)
            print(feedback)

    while True:

        input_str = input("Please input MVD:")
        if input_str == "quit":
            break

        feedback = new_table.add_mvd(input_str)
        print(feedback)

    return new_table

# Task I.c
def update_normal_form(table):
    if table.nf == "":
        table.get_normal_form()

    print("Currently this table has normal form: " + table.nf)

    if table.nf != "3NF" or table.nf != "BCNF":
        print("You can either delete this table or update its FD's.")
        decision = input("Either type \'del\' for deletion or \'u\' to update:")

        if decision == 'del':
            del table
        elif decision == 'u':
            done = False
            while not done:
                print("Current FD(s) in the table: " + str(table.fds) + "\n")
                input_str = input("Type \'a\' to add a new FD or \'d\' to delete a FD: ")
                if input_str == 'a':
                    new_fd = input("Add a new FD: ")
                    feedback = table.add_fd(new_fd.replace(" ",""))
                    print(feedback)
                    new_nf = table.get_normal_form()
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
                        new_nf = table.get_normal_form()
                        again = input("The table now has normal form " + table.nf + " would you like to continue (y/n)?")
                        if again == 'n':
                            done = True
                else:
                    print("That's not a valid decision!")

        else:
            print("That's not a valid decision!")

if __name__ == "__main__":
    # new_table = create_table()
    # new_table = create_constraint(new_table)
    # new_table.print_attributes()
    # new_table.print_boolean_conditions()

    # Adding attributes
    A = Attribute("A", "integer")
    B = Attribute("B", "integer")
    C = Attribute("C", "integer")
    D = Attribute("D", "string")
    E = Attribute("E", "integer")
    F = Attribute("F", "string")

    new_table = Table("test1", [A,B,C,D,E,F])
    db = Database()
    db.add_table(new_table)

    new_table.add_fd("A->B")

    update_normal_form(new_table)